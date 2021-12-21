import json
from web3 import Web3
from solcx import compile_standard, install_solc
import os
import pickle

with open("./contract.sol", "r") as file:
    contract_raw = file.read()

install_solc("0.6.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"contract.sol": {"content": contract_raw}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

bytecode = compiled_sol["contracts"]["contract.sol"]["Crop_Assister"]["evm"][
    "bytecode"
]["object"]

abi = json.loads(
    compiled_sol["contracts"]["contract.sol"]["Crop_Assister"]["metadata"]
)["output"]["abi"]

# For connecting to ganache

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x0b71E13F73365c274575c52DF1ad6Bba1c8e4Adb" #please change the address here accordingly
private_key = "1755838bd5e2f490497c3a808f1dc10556d593b4edc4f0a725550eb60bfb0a52" #please change the private key accordingly


contract= w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(my_address)
transaction = contract.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

with open("blockchain_data/txn_receipt.txt", "wb") as text_file:
    pickle.dump(tx_receipt,text_file)

with open("blockchain_data/abi.txt", "wb") as text_file:
    pickle.dump(abi,text_file)
