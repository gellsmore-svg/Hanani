"""Geopolitical factor taxonomy."""

from __future__ import annotations

FACTORS: list[dict[str, str]] = [
    {"id": "troop-movements", "label": "Troop movements and force disposition"},
    {"id": "logistics", "label": "Logistics and supply lines"},
    {"id": "ammunition", "label": "Ammunition consumption and resupply"},
    {"id": "industrial-production", "label": "Industrial and defence production"},
    {"id": "sanctions", "label": "Sanctions and economic pressure"},
    {"id": "diplomatic-signalling", "label": "Diplomatic signalling"},
    {"id": "satellite-imagery", "label": "Satellite imagery and OSINT"},
    {"id": "historical-precedent", "label": "Historical precedents"},
    {"id": "economic-indicators", "label": "Economic indicators"},
    {"id": "political-incentives", "label": "Political incentives"},
    {"id": "military-doctrine", "label": "Military doctrine"},
    {"id": "propaganda-signals", "label": "Propaganda and narrative framing"},
]


def list_factors() -> list[dict[str, str]]:
    return list(FACTORS)