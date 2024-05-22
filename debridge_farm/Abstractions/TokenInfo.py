from typing import TypedDict, Optional


class TokenInfo(TypedDict):
    address: str
    symbol: str
    decimals: int
    is_eip: Optional[bool]
    name: str
