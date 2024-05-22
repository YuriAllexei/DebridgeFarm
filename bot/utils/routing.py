import json, itertools
from typing import Dict, List

from debridge_farm.Abstractions import Route


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


def route_checker(chain : str,routes_dict : Dict[str,List[Route]]):

