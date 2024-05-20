import requests
from typing import List


from Abstractions.ChainInfo import ChainInfo


def get_chain_info() -> List[ChainInfo]:

    data = requests.get("https://api.dln.trade/v1.0/supported-chains-info").json()

    chain_info: List[ChainInfo] = []

    for info in data["chains"]:
        chain_info.append(
            {"chain_id": info["chainId"], "chain_name": info["chainName"]}
        )

    return chain_info
