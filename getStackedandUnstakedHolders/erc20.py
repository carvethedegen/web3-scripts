from web3 import Web3
import json

abi = json.loads(open("abi.json").read())
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/API-HERE'))

token_abi = abi  
token_address = '0xE4e3A5Fc669F43C23857d180e173e73e3b0Ffa14' 

contract = w3.eth.contract(address=Web3.toChecksumAddress(token_address), abi=token_abi)

def getErc20():
    transfer_event = contract.events.Transfer.createFilter(fromBlock=0, toBlock='latest')

    events = transfer_event.get_all_entries()

    token_holders = set()
    for event in events:
        token_holders.add(event['args']['from'])
        token_holders.add(event['args']['to'])

    token_holders.discard(w3.toChecksumAddress('0x0000000000000000000000000000000000000000'))

    holder_balances = {}
    for holder in token_holders:
        balance = contract.functions.balanceOf(holder).call()
        if balance > 0:
            holder_balances[holder] = w3.fromWei(balance, 'ether')
    print(holder_balances)
    return holder_balances
# if __name__ == "__main__":
#     holder_balances = getErc20()
#     print(len(holder_balances))
#     for holder, balance in holder_balances.items():
#         print(f"{holder}: {balance} tokens")