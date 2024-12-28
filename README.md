# Auto-Send-Token-Multi-Address-Chain-BASE
This script automates the process of sending tokens to multiple addresses on the Base network. It reads recipient addresses from a file, checks the sender's balance, and sends the specified amount of tokens to each recipient.

Prerequisites
Python: Install Python 3.10

Install Dependencies: ```pip install web3```

Files Required
Place the following files in the same directory as the script:
1. pvkey.txt: Contains the private key of the sender's wallet (one line).
2. contract.txt: Contains the address of the token contract (one line).
3. account.txt: Contains the recipient addresses (one address per line).

Run Script Command:
```python autotxbase.py```

Output
The script will:
1. Connect to the Base network.
2. Validate the sender's token balance.
3. Send tokens to each recipient one by one, waiting 10 seconds between transactions.
4. Print the transaction hash (TX ID) for each successful transfer.

Important Notes!
1. Ensure the private key has sufficient gas fees in the wallet.
2. Test the script in a testnet before deploying it on the mainnet.
