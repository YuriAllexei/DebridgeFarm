import json

from ..Abstractions import QuoteParam


def get_infura_url(quote_param: QuoteParam, infura_key: str) -> str:

    match quote_param["chain_info"]["chain_id"]:

        case 1:
            return f"https://mainnet.infura.io/v3/{infura_key}"
        case 10:
            return f"https://optimism-mainnet.infura.io/v3/{infura_key}"
        case 137:
            return f"https://polygon-mainnet.infura.io/v3/{infura_key}"
        case 42161:
            return f"https://arbitrum-mainnet.infura.io/v3/{infura_key}"
        case 59144:
            return f"https://linea-mainnet.infura.io/v3/{infura_key}"
