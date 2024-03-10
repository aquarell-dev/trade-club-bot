from dataclasses import dataclass


@dataclass
class Affiliate:
    user_id: str
    deposit: float
    trade_volume: float
