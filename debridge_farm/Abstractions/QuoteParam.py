from typing import TypedDict
from .ChainInfo import ChainInfo
from .TokenInfo import TokenInfo


class QuoteParam(TypedDict):
    chain_info: ChainInfo
    token_info: TokenInfo
