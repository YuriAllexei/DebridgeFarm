from pprint import pprint

from .chain_utils import send_dln_order
from .infura_utils import get_infura_url

from ApiUtils import (
    get_chain_info,
    get_chain_token_list,
    chain_list_to_chain_map,
    chain_token_map,
    pack_chain_token_info,
    get_quote,
    calculate_quote_metrics,
    create_transaction,
)


if __name__ == "__main__":

    address = "0xCf9f2c90De197d63b98b2F2dC4f095D19954010B"

    chain_list = get_chain_info()

    chain_map = chain_list_to_chain_map(chain_list=chain_list)

    arbitrum_chain_info = chain_map["Arbitrum"]

    arbitrum_chain_tokens = get_chain_token_list(chain_info=arbitrum_chain_info)

    arbitrum_token_map = chain_token_map(
        chain_info=arbitrum_chain_info, tokens=arbitrum_chain_tokens
    )

    arbitrum_usdc_quote_param = pack_chain_token_info(
        chain_info=arbitrum_chain_info, token_info=arbitrum_token_map["tokens"]["USDC"]
    )

    optimism_chain_info = chain_map["Optimism"]

    optimism_chain_tokens = get_chain_token_list(chain_info=optimism_chain_info)

    optimism_token_map = chain_token_map(
        chain_info=optimism_chain_info, tokens=optimism_chain_tokens
    )

    optimism_usdc_quote_param = pack_chain_token_info(
        chain_info=optimism_chain_info, token_info=optimism_token_map["tokens"]["USDC"]
    )

    print("Source Quote params:\n")
    pprint(arbitrum_usdc_quote_param)

    print("Destiny Quote Params:\n")
    pprint(optimism_usdc_quote_param)

    print("Quote:\n\n")

    quote = get_quote(
        src_quote_param=arbitrum_usdc_quote_param,
        dst_quote_param=optimism_usdc_quote_param,
        amount=10,
    )

    pprint(quote)

    calculate_quote_metrics(quote_info=quote)

    tx = create_transaction(
        address=address,
        quote_info=quote,
        src_param=arbitrum_usdc_quote_param,
        dst_param=optimism_usdc_quote_param,
    )

    infura_url = get_infura_url(
        quote_param=arbitrum_usdc_quote_param,
        infura_key="9e13214a449b4aaa903ec565642b91c0",
    )
    print(tx)

    # send_dln_order(
    #     infura_url=infura_url,
    #     address=address,
    #     tx_data=tx,
    #     private_key="738862141af6ea6ebac73a1545548e40745be4085e38d64c7c3c15b4db7d1fcf",
    # )
