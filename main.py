import json
from pprint import pprint
from dotenv import dotenv_values

from debridge_farm.Abstractions import User
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

    route_checker(user=user, chain="Arbitrum", routes_dict=routes)


if __name__ == "__main__":

    main()
