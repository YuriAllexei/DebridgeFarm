from typing import TypedDict


class TokenInfo(TypedDict):
    address: str
    symbol: str
    decimals: int
    is_eip: bool
    name: str
