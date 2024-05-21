from typing import TypedDict, List, Dict

from Abstractions import TokenInfo


class ChainTokenMap(TypedDict):

    chain_id: int
    chain_name: str
    tokens: Dict[str, TokenInfo]
