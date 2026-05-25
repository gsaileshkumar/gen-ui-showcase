"""The five DHL tools the agent can call.

Each is a thin wrapper that delegates to dhl.client, which picks mock vs live
based on DHL_MODE. Tool docstrings are the agent-visible descriptions — keep
them tight and accurate.
"""

from __future__ import annotations

from typing import Any

from langchain_core.tools import tool

from dhl.client import dhl_client


@tool
def track_shipment(tracking_number: str) -> dict[str, Any]:
    """Look up the live status and event timeline for a DHL shipment by
    tracking number. Returns origin, destination, current status, ETA, and
    a chronological events array suitable for a tracking timeline UI."""
    return dhl_client().track_shipment(tracking_number)


@tool
def get_rates(
    origin_country: str,
    destination_country: str,
    weight_kg: float,
    length_cm: float = 30,
    width_cm: float = 20,
    height_cm: float = 10,
) -> dict[str, Any]:
    """Quote DHL shipping rates between two countries for a parcel of the
    given weight and dimensions. Returns multiple service products
    (Express, Economy, etc.) with price, transit days, and breakdown."""
    return dhl_client().get_rates(
        origin_country=origin_country,
        destination_country=destination_country,
        weight_kg=weight_kg,
        dimensions_cm=(length_cm, width_cm, height_cm),
    )


@tool
def calc_duty(
    origin_country: str,
    destination_country: str,
    declared_value: float,
    currency: str = "USD",
    product_category: str = "general",
) -> dict[str, Any]:
    """Calculate import duty and tax for a cross-border shipment. Returns
    duty rate, tax rate, total landed cost, and a line-item breakdown."""
    return dhl_client().calc_duty(
        origin_country=origin_country,
        destination_country=destination_country,
        declared_value=declared_value,
        currency=currency,
        product_category=product_category,
    )


@tool
def find_locations(
    country_code: str,
    postal_code: str,
    radius_km: float = 5,
) -> dict[str, Any]:
    """Find DHL service points (lockers, drop-off shops, ServicePoints) near
    a postal code. Returns up to 10 locations with name, address, lat/lng,
    opening hours, and supported services."""
    return dhl_client().find_locations(
        country_code=country_code,
        postal_code=postal_code,
        radius_km=radius_km,
    )


@tool
def visualize_route(tracking_number: str) -> dict[str, Any]:
    """Fetch the geographic route data for a shipment — origin, destination,
    waypoints with lat/lng, and per-leg timestamps — for use in a bespoke
    animated SVG visualization."""
    return dhl_client().visualize_route(tracking_number)


ALL_TOOLS = [track_shipment, get_rates, calc_duty, find_locations, visualize_route]
