from pprint import pprint

from .fetchers import (
    get_chain_info,
    get_chain_token_list,
    get_quote,
    create_transaction,
)
from .data_utils import pack_chain_token_info
from .calculation_utils import calculate_quote_metrics

if __name__ == "__main__":

    wallet_address = "0xCf9f2c90De197d63b98b2F2dC4f095D19954010B"

    chains_info = get_chain_info()
    pprint(chains_info)

    chain = chains_info[0]

    print(
        f"Querying tokens available for chain: {chain['chain_name']} with id: {chain['chain_id']}"
    )

    tokens = get_chain_token_list(chain_info=chain)

    print(tokens[:5])

    src_chain_info = chains_info[1]
    src_chain_tokens_info = get_chain_token_list(chain_info=src_chain_info)

    dst_chain_info = chains_info[5]
    dst_chain_tokens_info = get_chain_token_list(chain_info=dst_chain_info)

    src_quote_param = pack_chain_token_info(
        chain_info=src_chain_info, token_info=src_chain_tokens_info[1]
    )
    dst_quote_param = pack_chain_token_info(
        chain_info=dst_chain_info, token_info=dst_chain_tokens_info[2]
    )

    print("Source Quote params:\n")
    pprint(src_quote_param)

    print("Destiny Quote Params:\n")
    pprint(dst_quote_param)

    print("Quote:\n\n")

    quote = get_quote(
        src_quote_param=src_quote_param, dst_quote_param=dst_quote_param, amount=100
    )

    pprint(quote)

    calculate_quote_metrics(quote_info=quote)

    create_transaction(
        address=wallet_address,
        quote_info=quote,
        src_param=src_quote_param,
        dst_param=dst_quote_param,
    )
