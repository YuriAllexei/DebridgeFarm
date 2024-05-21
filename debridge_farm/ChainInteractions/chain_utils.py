import json
from web3 import Web3

from Abstractions import TxData


def send_dln_order(infura_url: str, address: str, private_key: str, tx_data: TxData):

    web3_object = Web3(Web3.HTTPProvider(infura_url))
    eth_address = Web3.to_checksum_address(value=address)

    transaction = {
        "to": tx_data["to"],
        "value": int(tx_data["value"]),
        "gas": 3000000,  # Adjust the gas limit as needed
        "gasPrice": web3_object.eth.gas_price,
        "nonce": web3_object.eth.get_transaction_count(eth_address),
        "data": tx_data["data"],
    }
    signed_txn = web3_object.eth.account.sign_transaction(transaction, private_key)

    tx_hash = web3_object.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f"Transaction sent. Hash: {tx_hash.hex()}")

    tx_receipt = web3_object.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Transaction receipt: {tx_receipt}")
