from web3 import Web3

from Abstractions import TxData


def send_dln_order(infura_url: str, address: str, private_key: str, tx_data: TxData):

    w3 = Web3(Web3.HTTPProvider(infura_url))

    eth_address = Web3.to_checksum_address(value=address)

    gas_estimate = w3.eth.estimate_gas(tx_data)

    transaction = {
        "to": tx_data["to"],
        "value": int(tx_data["value"]),
        "gas": gas_estimate,
        "gasPrice": w3.eth.gas_price,
        "nonce": w3.eth.get_transaction_count(eth_address),
        "data": tx_data["data"],
    }
    signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    print(f"Transaction sent. Hash: {tx_hash.hex()}")
    print(f"Transaction receipt: {tx_receipt}")
