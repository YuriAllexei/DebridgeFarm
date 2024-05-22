import json
from web3 import Web3
from eth_abi import encode, decode

from ..Abstractions import TxData, QuoteParam, ChainInfo


def send_dln_order(
    infura_url: str,
    address: str,
    private_key: str,
    tx_data: TxData,
    chain_info: ChainInfo,
):

    web3_object = Web3(Web3.HTTPProvider(infura_url))
    eth_address = Web3.to_checksum_address(value=address)

    transaction = {
        "from": eth_address,
        "to": tx_data["to"],
        "value": int(tx_data["value"]),
        "gas": 3000000,  # Adjust the gas limit as needed
        "gasPrice": web3_object.eth.gas_price,
        "nonce": web3_object.eth.get_transaction_count(eth_address),
        "data": tx_data["data"],
        "chainId": chain_info["chain_id"],
    }
    signed_txn = web3_object.eth.account.sign_transaction(transaction, private_key)

    tx_hash = web3_object.eth.send_raw_transaction(
        transaction=signed_txn.rawTransaction
    )
    print(f"Transaction sent. Hash: {tx_hash.hex()}")

    tx_receipt = web3_object.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction receipt: {tx_receipt}")


def query_erc_20_balance(
    infura_url: str, src_quote_param: QuoteParam, account_address: str
) -> float:

    web3 = Web3(Web3.HTTPProvider(infura_url))

    contract_checksum_address = Web3.to_checksum_address(
        value=src_quote_param["token_info"]["address"]
    )

    function_signature = Web3.keccak(text="balanceOf(address)")[0:4].hex()
    encoded_params = encode(["address"], [account_address]).hex()

    result = web3.eth.call(
        {"to": contract_checksum_address, "data": function_signature + encoded_params}
    )

    decoded_result = decode(["uint256"], result)[0]

    return decoded_result / (10 ** src_quote_param["token_info"]["decimals"])


def query_native_token_balance(infura_url: str, account_address: str) -> float:
    web3 = Web3(Web3.HTTPProvider(infura_url))
    balance_wei = web3.eth.get_balance(account=account_address)
    balance_ether = web3.from_wei(balance_wei, "ether")
    return balance_ether
