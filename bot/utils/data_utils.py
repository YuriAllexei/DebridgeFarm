from threading import Lock
from typing import Dict, Optional

from debridge_farm.Abstractions import ChainTokenMap, TokenInfo, ChainInfo
from debridge_farm.ApiUtils import get_chain_token_list, chain_token_map


def query_chain_token_list(
    data_lock: Lock,
    chain_token_directory: Dict[str, ChainTokenMap],
    chain_info: ChainInfo,
    token: str,
) -> Optional[TokenInfo]:

    with data_lock:

        if chain_info["chain_name"] not in chain_token_directory:

            chain_token_list = get_chain_token_list(chain_info=chain_info)

            c_t_m = chain_token_map(chain_info=chain_info, tokens=chain_token_list)

            chain_token_directory[chain_info["chain_name"]] = c_t_m

            return chain_token_directory[chain_info["chain_name"]]["tokens"][token]

        else:
            return chain_token_directory[chain_info["chain_name"]]["tokens"][token]
