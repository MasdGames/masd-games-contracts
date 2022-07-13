import time
from brownie import *


def main():
    erc721 = Contract.from_abi("ERC721", "0xEaF8E1DaE061724557cD7Cd9f013211f588A4dAA", MASD_ERC721.abi)
    print(f'{erc721.tokenURI(42)=}')
