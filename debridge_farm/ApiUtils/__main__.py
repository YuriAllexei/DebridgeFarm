from pprint import pprint

from .fetchers import get_chain_info


if __name__ == "__main__":
    info = get_chain_info()
    pprint(info)
