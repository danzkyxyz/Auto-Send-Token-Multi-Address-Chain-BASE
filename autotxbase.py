import time
from web3 import Web3

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"File {filename} not found!")
        exit()

rpc_url = "https://mainnet.base.org"
web3 = Web3(Web3.HTTPProvider(rpc_url))

if not web3.is_connected():
    print("Failed to connect to the Base network!")
    exit()

token_contract_address = read_file('contract.txt')
private_key = read_file('pvkey.txt')
sender_address = web3.eth.account.from_key(private_key).address
recipients_file = 'account.txt'

def read_recipients(file):
    try:
        with open(file, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"File {file} not found!")
        exit()

recipients = read_recipients(recipients_file)

token_contract_abi = [
    {
        "constant": True,
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "recipient", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

token_contract = web3.eth.contract(address=token_contract_address, abi=token_contract_abi)

def send_token(sender, private_key, to_address, amount):
    balance = token_contract.functions.balanceOf(sender).call()
    if balance < web3.to_wei(amount, 'ether'):
        print(f"Sender's balance is insufficient to send tokens to {to_address}")
        return None

    nonce = web3.eth.get_transaction_count(sender, "pending")
    gas_price = web3.to_wei(0.015, 'gwei')
    gas_limit = 100000

    transaction = {
        'to': token_contract_address,
        'data': token_contract.encodeABI(fn_name='transfer', args=[to_address, web3.to_wei(amount, 'ether')]),
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': nonce,
        'chainId': 8453
    }

    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    return web3.to_hex(tx_hash)

try:
    amount_per_user = float(input("Enter the amount of tokens to distribute per user: "))
except ValueError:
    print("Invalid token amount. Please enter a valid number.")
    exit()

for recipient in recipients:
    tx_id = send_token(sender_address, private_key, recipient, amount_per_user)
    if tx_id:
        print(f"Transaction successful for {recipient} with TX ID: {tx_id}")
    time.sleep(2)

print("All token transactions have been sent.")
