import json, time
from threading import Lock, Thread
from typing import Dict
from pprint import pprint
from dotenv import dotenv_values

from debridge_farm.Abstractions import User, ChainTokenMap
from bot.utils.routing import calculate_routes, route_checker


def main():

    env_values = dotenv_values(".env")

    user: User = {
        "address": env_values["ADDRESS"],
        "infura_key": env_values["INFURA_KEY"],
        "private_key": env_values["PRIVATE_KEY"],
    }

    params_file = open("params.json", mode="r")

    params_dict = json.load(params_file)

    params_file.close()

    routes = calculate_routes(params_dict=params_dict)

    chain_token_directory: Dict[str, ChainTokenMap] = {}

    data_lock: Lock = Lock()

    for chain in routes.keys():
        print(f"Initializing thread for {chain}")
        Thread(
            target=route_checker,
            args=(user, chain, routes, chain_token_directory, data_lock),
            daemon=True,
            name=f"{chain}-Thread",
        ).start()

    while True:
        time.sleep(500)


if __name__ == "__main__":

    main()
