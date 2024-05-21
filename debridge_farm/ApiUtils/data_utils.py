from typing import List, Dict

from Abstractions import ChainInfo, QuoteInfo, QuoteParam, TokenInfo, ChainTokenMap


def pack_chain_token_info(chain_info: ChainInfo, token_info: TokenInfo) -> QuoteParam:

    return {"chain_info": chain_info, "token_info": token_info}


def retrieve_quote_info(response_dict: dict) -> QuoteInfo:

    estimation_dict = response_dict["estimation"]

    quote_info: QuoteInfo = {}

    quote_info["total_src_amount"] = estimation_dict["srcChainTokenIn"]["amount"]
    quote_info["src_decimals"] = estimation_dict["srcChainTokenIn"]["decimals"]
    quote_info["src_operating_expense"] = estimation_dict["srcChainTokenIn"][
        "approximateOperatingExpense"
    ]
    quote_info["dst_decimals"] = estimation_dict["dstChainTokenOut"]["decimals"]
    quote_info["dst_recommended_amount"] = estimation_dict["dstChainTokenOut"][
        "recommendedAmount"
    ]
    quote_info["points"] = response_dict["userPoints"]

    return quote_info


def chain_token_map(chain_info: ChainInfo, tokens: List[TokenInfo]) -> ChainTokenMap:

    c_t_m: ChainTokenMap = {
        "chain_id": chain_info["chain_id"],
        "chain_name": chain_info["chain_name"],
        "tokens": {},
    }

    for token_info in tokens:
        c_t_m["tokens"][token_info["symbol"]] = token_info

    return c_t_m


def chain_list_to_chain_map(chain_list: List[ChainInfo]) -> Dict[str, ChainInfo]:

    chain_map: Dict[str, ChainInfo] = {}

    for chain_info in chain_list:

        chain_map[chain_info["chain_name"]] = chain_info

    return chain_map
