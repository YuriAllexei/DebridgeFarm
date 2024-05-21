from typing import TypedDict
from Abstractions.ChainInfo import ChainInfo
from Abstractions.TokenInfo import TokenInfo


class QuoteParam(TypedDict):
    chain_info: ChainInfo
    token_info: TokenInfo
