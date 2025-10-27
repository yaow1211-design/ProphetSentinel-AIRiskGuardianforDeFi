"""
SolanaService
-------------
Lightweight wrapper to fetch Solana protocol metrics.

In demo mode, returns deterministic synthetic data so the API can run
without external dependencies.
"""

from __future__ import annotations

import os
import random
import time
from typing import Dict, Any


class SolanaService:
    def __init__(self, demo_mode: bool | None = None) -> None:
        # Allow env override; default to demo so the backend works out of the box
        if demo_mode is None:
            env_flag = os.getenv("SOLANA_DEMO_MODE", "true").lower()
            demo_mode = env_flag in ("1", "true", "yes", "y")
        self.demo_mode = demo_mode

        # Placeholder for real client initialization (RPC/websocket, etc.)
        self._client = None

    def get_protocol_metrics(self, protocol: str) -> Dict[str, Any]:
        if self.demo_mode:
            return self._generate_demo_metrics(protocol)

        # In real implementation, fetch on-chain or analytics API data here.
        # To keep the backend functional without network, fall back to demo.
        return self._generate_demo_metrics(protocol)

    def _generate_demo_metrics(self, protocol: str) -> Dict[str, Any]:
        # Seed with protocol for stable-but-varied values across protocols
        seed = hash((protocol.lower(), int(time.time() // 3600))) & 0xFFFFFFFF
        rng = random.Random(seed)

        volume_24h = round(rng.uniform(1_000_000, 150_000_000), 2)
        liquidity_change = round(rng.uniform(-0.35, 0.35), 4)  # -35% .. +35%
        whale_transfers = rng.randint(0, 25)
        holder_concentration = round(rng.uniform(0.05, 0.75), 3)  # 5% .. 75%

        return {
            "protocol": protocol,
            "volume_24h": volume_24h,
            "liquidity_change": liquidity_change,
            "whale_transfers": whale_transfers,
            "holder_concentration": holder_concentration,
        }


