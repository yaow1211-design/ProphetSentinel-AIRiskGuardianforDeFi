"""
Sustainability scoring utilities.

This module provides a simple, deterministic sustainability score for a
protocol based on available metrics. It is intentionally lightweight so
the backend can run in environments without external data sources.
"""

from __future__ import annotations

from typing import Dict


def calculate_sustainability_score(metrics: Dict) -> int:
    """
    Compute a 0-100 sustainability score from protocol metrics.

    Heuristics (demo-friendly):
    - Lower holder concentration implies better decentralization (+)
    - Moderate liquidity change is healthier than extreme swings (+)
    - Fewer whale transfers suggests stability (+)

    The formula is bounded to 0..100.
    """
    volume_24h = float(metrics.get("volume_24h", 0.0))
    liquidity_change = float(metrics.get("liquidity_change", 0.0))  # -1..+1 scale
    whale_transfers = float(metrics.get("whale_transfers", 0))
    holder_concentration = float(metrics.get("holder_concentration", 0.5))  # 0..1

    # Base score derived from decentralization (lower concentration -> higher score)
    decentralization_score = (1.0 - max(0.0, min(1.0, holder_concentration))) * 60.0

    # Stability bonus: penalize extreme swings beyond +/- 20%
    swing = abs(liquidity_change)
    if swing <= 0.2:
        stability_bonus = 20.0
    elif swing <= 0.35:
        stability_bonus = 10.0
    else:
        stability_bonus = 0.0

    # Whale activity penalty: each whale transfer reduces score slightly (capped)
    whale_penalty = min(whale_transfers * 1.2, 20.0)

    # Activity bonus: very low activity can be unhealthy; moderate is fine
    # Simple clamp where any reasonable volume adds a tiny bonus
    activity_bonus = 0.0
    if volume_24h >= 5_000_000:
        activity_bonus = 5.0
    if volume_24h >= 50_000_000:
        activity_bonus = 8.0

    raw_score = decentralization_score + stability_bonus + activity_bonus - whale_penalty
    bounded = int(max(0, min(100, round(raw_score))))
    return bounded


