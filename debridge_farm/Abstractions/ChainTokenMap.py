from typing import TypedDict, List, Dict

from .TokenInfo import TokenInfo


class ChainTokenMap(TypedDict):

    chain_id: int
    chain_name: str
    tokens: Dict[str, TokenInfo]
