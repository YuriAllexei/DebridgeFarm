import itertools, time
from pprint import pprint
from threading import Lock
from typing import Dict, List

from .data_utils import query_chain_token_list

from debridge_farm.Abstractions import Route, User, ChainTokenMap
from debridge_farm.ApiUtils import (
    get_chain_info,
    chain_list_to_chain_map,
    get_chain_token_list,
    chain_token_map,
    pack_chain_token_info,
    get_quote,
    calculate_quote_metrics,
    create_transaction,
)

from debridge_farm.ChainInteractions import (
    get_infura_url,
    query_erc_20_balance,
    query_native_token_balance,
    send_dln_order,
)


def calculate_routes(params_dict: Dict) -> Dict[str, List[Route]]:

    routes: Dict[str, List[Route]] = {}

    for src_chain_iterator in params_dict["src_chains"]:
        routes[src_chain_iterator] = []
        src_chain_tokens = params_dict["src_chains"][src_chain_iterator]

        for dst_chain_iterator in params_dict["dst_chains"]:
            if src_chain_iterator != dst_chain_iterator:
                dst_chain_tokens = params_dict["dst_chains"][dst_chain_iterator]

                route_tokens_list = list(
                    itertools.product(*[src_chain_tokens, dst_chain_tokens])
                )

                for route_tokens in route_tokens_list:
                    routes[src_chain_iterator].append(
                        {
                            "dst_chain": dst_chain_iterator,
                            "dst_token": route_tokens[1],
                            "src_chain": src_chain_iterator,
                            "src_token": route_tokens[0],
                        }
                    )

    return routes


def route_checker(
    user: User,
    chain: str,
    routes_dict: Dict[str, List[Route]],
    chain_token_directory: Dict[str, ChainTokenMap],
    data_lock: Lock,
):

    amount = 2
    chain_list = get_chain_info()

    chain_map = chain_list_to_chain_map(chain_list=chain_list)

    src_chain_info = chain_map[chain]

    infura_url = get_infura_url(
        chain_id=src_chain_info["chain_id"],
        infura_key=user["infura_key"],
    )

    print(f"Infura url: {infura_url}")

    while True:

        for route in routes_dict[chain]:

            src_chain_name = route["src_chain"]
            src_chain_token = route["src_token"]
            dst_chain_name = route["dst_chain"]
            dst_chain_token = route["dst_token"]

            src_token_info = query_chain_token_list(
                data_lock=data_lock,
                chain_info=src_chain_info,
                chain_token_directory=chain_token_directory,
                token=src_chain_token,
            )

            if src_token_info is None:
                print(f"No token info for {src_chain_token} in {src_chain_name}")
                continue

            src_quote_param = pack_chain_token_info(
                chain_info=src_chain_info,
                token_info=src_token_info,
            )

            erc_20_balance = query_erc_20_balance(
                infura_url=infura_url,
                src_quote_param=src_quote_param,
                account_address=user["address"],
            )

            print(
                f"{src_quote_param['chain_info']['chain_name']} {src_quote_param['token_info']['name']} balance: {erc_20_balance}"
            )

            if erc_20_balance < amount:
                print(
                    f"Not enough {src_quote_param['token_info']} available for bridge"
                )
                continue

            native_token_balance = query_native_token_balance(
                infura_url=infura_url, account_address=user["address"]
            )

            print(
                f"{src_quote_param['chain_info']['chain_name']} native balance: {native_token_balance}"
            )

            dst_chain_info = chain_map[dst_chain_name]

            dst_token_info = query_chain_token_list(
                data_lock=data_lock,
                chain_info=dst_chain_info,
                chain_token_directory=chain_token_directory,
                token=dst_chain_token,
            )

            if dst_token_info is None:
                print(f"No token info for {src_chain_token} in {src_chain_name}")
                continue

            dst_quote_param = pack_chain_token_info(
                chain_info=dst_chain_info,
                token_info=dst_token_info,
            )

            quote = get_quote(
                src_quote_param=src_quote_param,
                dst_quote_param=dst_quote_param,
                amount=amount,
            )

            pprint(quote)

            fixed_fee = int(quote["fixed_fee"]) / (10**18)

            if native_token_balance <= fixed_fee:
                print(
                    f"Not enought native token balance to pay the fixed fee of {fixed_fee}"
                )

            print(
                f"Src chain: {src_chain_name} Src token: {src_chain_token}  Dst chain: {dst_chain_name} Dst token: {dst_chain_token}"
            )

            calculate_quote_metrics(quote_info=quote)

            tx = create_transaction(
                address=user["address"],
                quote_info=quote,
                src_param=src_quote_param,
                dst_param=dst_quote_param,
            )

            send_dln_order(
                infura_url=infura_url,
                address=user["address"],
                tx_data=tx,
                private_key=user["private_key"],
                chain_info=src_chain_info,
            )

            return
