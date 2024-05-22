import json

from pprint import pprint

from bot.utils.routing import calculate_routes


def main():
    params_file = open("params.json", mode="r")

    params_dict = json.load(params_file)

    params_file.close()

    routes = calculate_routes(params_dict=params_dict)
    pprint(routes)


if __name__ == "__main__":

    main()
