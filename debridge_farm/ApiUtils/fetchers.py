import requests
from typing import List, Optional

from ..Abstractions import ChainInfo, TokenInfo, QuoteParam, QuoteInfo, TxData


from .data_utils import retrieve_quote_info


def get_chain_info() -> List[ChainInfo]:

    data = requests.get("https://api.dln.trade/v1.0/supported-chains-info").json()

    chain_info: List[ChainInfo] = []

    for info in data["chains"]:
        chain_info.append(
            {"chain_id": info["chainId"], "chain_name": info["chainName"]}
        )

    return chain_info


def get_chain_token_list(chain_info: ChainInfo) -> List[TokenInfo]:

    token_info: List[TokenInfo] = []

    data = requests.get(
        f"https://api.dln.trade/v1.0/token-list?chainId={chain_info['chain_id']}"
    ).json()

    for info in data["tokens"]:
        inner = data["tokens"][info]
        token_info.append(
            {
                "address": inner["address"],
                "decimals": inner["decimals"],
                "is_eip": inner["eip2612"],
                "symbol": inner["symbol"],
                "name": inner["name"],
            }
        )

    return token_info


def get_quote(
    src_quote_param: QuoteParam, dst_quote_param: QuoteParam, amount: float
) -> Optional[QuoteInfo]:

    token_in_amount = int(amount * (10 ** src_quote_param["token_info"]["decimals"]))
    print(f"Token amount in decimals: {token_in_amount}")
    data = requests.get(
        f"https://api.dln.trade/v1.0/dln/order/quote?srcChainId={src_quote_param['chain_info']['chain_id']}&srcChainTokenIn={src_quote_param['token_info']['address']}&srcChainTokenInAmount={token_in_amount}&dstChainId={dst_quote_param['chain_info']['chain_id']}&dstChainTokenOut={dst_quote_param['token_info']['address']}&dstChainTokenOutAmount=auto&prependOperatingExpenses=true"
    ).json()

    try:

        return retrieve_quote_info(response_dict=data)

    except:
        return None


def create_transaction(
    address: str, quote_info: QuoteInfo, src_param: QuoteParam, dst_param: QuoteParam
) -> TxData:

    data = requests.get(
        f"https://api.dln.trade/v1.0/dln/order/create-tx?srcChainId={src_param['chain_info']['chain_id']}&srcChainTokenIn={src_param['token_info']['address']}&srcChainTokenInAmount={quote_info['total_src_amount']}&dstChainId={dst_param['chain_info']['chain_id']}&dstChainTokenOut={dst_param['token_info']['address']}&dstChainTokenOutAmount={quote_info['dst_recommended_amount']}&dstChainTokenOutRecipient={address}&srcChainOrderAuthorityAddress={address}&dstChainOrderAuthorityAddress={address}"
    ).json()

    return data["tx"]
