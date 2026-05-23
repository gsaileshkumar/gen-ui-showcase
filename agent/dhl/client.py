"""Hybrid DHL client.

DHL_MODE=mock (default) → return fixtures from dhl/mock/*.json, with a small
artificial delay so streaming looks real on stage.
DHL_MODE=live           → call developer.dhl.com endpoints (see live.py).

Fixture shapes match the real DHL Developer Portal schemas so flipping the env
flag changes nothing in the UI.
"""

from __future__ import annotations

import json
import os
import time
from functools import lru_cache
from pathlib import Path
from typing import Any, Protocol

MOCK_DIR = Path(__file__).parent / "mock"
ARTIFICIAL_DELAY_S = 0.4  # streams feel alive without padding the demo


class DhlClient(Protocol):
    def track_shipment(self, tracking_number: str) -> dict[str, Any]: ...
    def get_rates(
        self,
        origin_country: str,
        destination_country: str,
        weight_kg: float,
        dimensions_cm: tuple[float, float, float],
    ) -> dict[str, Any]: ...
    def calc_duty(
        self,
        origin_country: str,
        destination_country: str,
        declared_value: float,
        currency: str,
        product_category: str,
    ) -> dict[str, Any]: ...
    def find_locations(
        self,
        country_code: str,
        postal_code: str,
        radius_km: float,
    ) -> dict[str, Any]: ...
    def visualize_route(self, tracking_number: str) -> dict[str, Any]: ...


def _load(name: str) -> dict[str, Any]:
    with (MOCK_DIR / name).open() as f:
        return json.load(f)


class MockDhlClient:
    """Returns fixtures matching real DHL Developer Portal schemas."""

    def track_shipment(self, tracking_number: str) -> dict[str, Any]:
        time.sleep(ARTIFICIAL_DELAY_S)
        data = _load("tracking.json")
        # Echo the requested tracking number into the response so the UI binds correctly.
        for shipment in data.get("shipments", []):
            shipment["id"] = tracking_number
        return data

    def get_rates(
        self,
        origin_country: str,
        destination_country: str,
        weight_kg: float,
        dimensions_cm: tuple[float, float, float],
    ) -> dict[str, Any]:
        time.sleep(ARTIFICIAL_DELAY_S)
        data = _load("rates.json")
        data["request"] = {
            "originCountry": origin_country,
            "destinationCountry": destination_country,
            "weightKg": weight_kg,
            "dimensionsCm": list(dimensions_cm),
        }
        return data

    def calc_duty(
        self,
        origin_country: str,
        destination_country: str,
        declared_value: float,
        currency: str,
        product_category: str,
    ) -> dict[str, Any]:
        time.sleep(ARTIFICIAL_DELAY_S)
        data = _load("duty.json")
        data["request"] = {
            "originCountry": origin_country,
            "destinationCountry": destination_country,
            "declaredValue": declared_value,
            "currency": currency,
            "productCategory": product_category,
        }
        # Scale the breakdown roughly to the requested value so the UI looks live.
        ratio = declared_value / max(data.get("declaredValue", 1), 1)
        for line in data.get("breakdown", []):
            line["amount"] = round(line["amount"] * ratio, 2)
        data["declaredValue"] = declared_value
        data["currency"] = currency
        return data

    def find_locations(
        self,
        country_code: str,
        postal_code: str,
        radius_km: float,
    ) -> dict[str, Any]:
        time.sleep(ARTIFICIAL_DELAY_S)
        data = _load("locations.json")
        data["request"] = {
            "countryCode": country_code,
            "postalCode": postal_code,
            "radiusKm": radius_km,
        }
        return data

    def visualize_route(self, tracking_number: str) -> dict[str, Any]:
        time.sleep(ARTIFICIAL_DELAY_S)
        data = _load("route.json")
        data["trackingNumber"] = tracking_number
        return data


@lru_cache(maxsize=1)
def dhl_client() -> DhlClient:
    mode = os.getenv("DHL_MODE", "mock").lower()
    if mode == "live":
        from dhl.live import LiveDhlClient  # local import; only loaded in live mode

        return LiveDhlClient()
    return MockDhlClient()
