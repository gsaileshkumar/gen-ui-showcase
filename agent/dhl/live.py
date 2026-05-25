"""Live DHL Developer Portal client.

Stubbed: implemented in Step 8 of the build plan. For now, raise loudly if
DHL_MODE=live so we never silently fall back to mocks in production rehearsal.
"""

from __future__ import annotations

import os
from typing import Any


class LiveDhlClient:
    BASE_URL = "https://api-eu.dhl.com"

    def __init__(self) -> None:
        self.api_key = os.getenv("DHL_API_KEY", "")
        if not self.api_key:
            raise RuntimeError(
                "DHL_MODE=live but DHL_API_KEY is not set. "
                "Add it to .env or switch DHL_MODE back to mock."
            )

    def _not_implemented(self, method: str) -> Any:
        raise NotImplementedError(
            f"LiveDhlClient.{method} is not wired yet. "
            "It's scheduled for Step 8 of the build plan. "
            "Use DHL_MODE=mock for now."
        )

    def track_shipment(self, tracking_number: str) -> dict[str, Any]:
        return self._not_implemented("track_shipment")

    def get_rates(self, **kwargs: Any) -> dict[str, Any]:
        return self._not_implemented("get_rates")

    def calc_duty(self, **kwargs: Any) -> dict[str, Any]:
        return self._not_implemented("calc_duty")

    def find_locations(self, **kwargs: Any) -> dict[str, Any]:
        return self._not_implemented("find_locations")

    def visualize_route(self, tracking_number: str) -> dict[str, Any]:
        return self._not_implemented("visualize_route")
