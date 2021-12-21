import pickle
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

with open("blockchain_data/txn_receipt.txt", "rb") as text_file:
	tx_receipt=pickle.load(text_file)

with open("blockchain_data/abi.txt","rb") as for_abi:
	abi=pickle.load(for_abi)

'''
my_address="0x0b71E13F73365c274575c52DF1ad6Bba1c8e4Adb"
private_key="1755838bd5e2f490497c3a808f1dc10556d593b4edc4f0a725550eb60bfb0a52"
'''
my_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

def transact(transaction,private_key):
	signed_txn = w3.eth.account.sign_transaction(
	    transaction, private_key=private_key
	)
	tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
	tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

def initial_fund(my_address,private_key,value): 
	nonce = w3.eth.getTransactionCount(my_address)
	transaction = my_contract.functions.fund().buildTransaction(
	    {
	        "chainId": w3.eth.chainId,
	        "gasPrice": w3.eth.gas_price,
	        "from": my_address,
	        "value":value,
	        "nonce": nonce ,
	    }
	)
	transact(transaction,private_key)


def add_to_network(my_address,private_key,disease_id,before,after,text):
	nonce = w3.eth.getTransactionCount(my_address)
	transaction = my_contract.functions.addSolution(disease_id,before,after,text).buildTransaction(
	    {
	        "chainId": w3.eth.chainId,
	        "gasPrice": w3.eth.gas_price,
	        "from": my_address,
	        "value":0,
	        "nonce": nonce ,
	    }
	)
	transact(transaction,private_key)

def pay_ml(my_address,private_key):
	nonce = w3.eth.getTransactionCount(my_address)
	transaction = my_contract.functions.pay_ml().buildTransaction(
	    {
	        "chainId": w3.eth.chainId,
	        "gasPrice": w3.eth.gas_price,
	        "from": my_address,
	        "value":10**17,
	        "nonce": nonce ,
	    }
	)
	transact(transaction,private_key)

def pay_for_solution(my_address,private_key):
	nonce = w3.eth.getTransactionCount(my_address)
	transaction = my_contract.functions.pay_for_solution().buildTransaction(
	    {
	        "chainId": w3.eth.chainId,
	        "gasPrice": w3.eth.gas_price,
	        "from": my_address,
	        "value":10**18,
	        "nonce": nonce ,
	    }
	)
	transact(transaction,private_key)

def give_incentive(my_address,private_key,to):
	nonce = w3.eth.getTransactionCount(my_address)
	transaction = my_contract.functions.giveIncentive(to).buildTransaction(
	    {
	        "chainId": w3.eth.chainId,
	        "gasPrice": w3.eth.gas_price,
	        "from": my_address,
	        "value":0,
	        "nonce": nonce ,
	    }
	)
	transact(transaction,private_key)

def access_solution(disease_id):
	return my_contract.functions.returnSolutions(disease_id).call()


#initial_fund(my_address,private_key,2*10**18)
#print(address_test("0x360676Fe812909036dcBda5b6478a90F4E20Fc5B"))

#add_to_network(my_address,private_key,1,"b","a","t")
#initial_fund(my_address,private_key,10**18)
#print(access_solution(1))
#add_to_network(my_address,private_key,1,"b","a","t")
#print(f"Current Balance is {my_contract.functions.getContractBalance().call()}")
