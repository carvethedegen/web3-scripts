import requests
from web3 import Web3
from collections import defaultdict
from pprint import pprint
from erc20 import getErc20
INFURA_API_KEY = 'rawr'
ETHERSCAN_API_KEY = 'lmeow'

erc1155_token_address = '0xfe190723a465c99293c4f035045c0a6880d25dbe'
erc1155_owners = {}
w3 = Web3(Web3.HTTPProvider(f'https://mainnet.infura.io/v3/{INFURA_API_KEY}'))

def getErc115Owners():
    offset = 0
    end = False
    while not end:
        url = "https://api.reservoir.tools/owners/v2?token=TOKENHERE%3A1&offset=" + str(offset) + "&limit=500" 
        response = requests.request("GET", url)
        resp = response.json()["owners"]
        if resp == []:
            print("Reached end")
            return
        for i in resp:
            if i['ownership']["tokenCount"] != 0:
                if i['address'] not in erc1155_owners:
                    erc1155_owners[i['address']] = i['ownership']["tokenCount"]
                else:
                    erc1155_owners[i['address']] += i['ownership']["tokenCount"]
        offset += len(resp)

def main():
    print("Getting ERC20 owners")
    erc20 = getErc20()
    print("Got ERC20 owners\nGetting ERC1155 owners")
    getErc115Owners()
    print("Got ERC1155 owners\nCombining ERC20 and ERC1155 owners")
    for (k, v) in erc20.items():
        if k not in list(erc1155_owners.keys()):
            erc1155_owners[k] = v
        else:
            erc1155_owners[k] += v
    print("Combined ERC20 and ERC1155 owners\nWriting to file")
    with open("owners.txt", "a") as f:
        for (k, v) in erc1155_owners.items():
            f.write(f"{k}: {v} tokens\n")
    print("Wrote to file")
main()
