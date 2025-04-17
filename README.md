# Rise Testnet Scripts

This repository contains a collection of Python scripts designed to interact with the **Rise Testnet**, a high-performance blockchain test network. These scripts enable users to perform various actions such as sending transactions, deploying ERC20 token and NFT smart contracts, managing tokens/NFTs, and interacting with decentralized applications (dApps) on the Rise Testnet using its RPC. Each script is built with the `web3.py` library and offers bilingual support (English and Vietnamese) for user interaction.

Faucet: [Rise Testnet Faucet](https://portal.risechain.com/)

## Features Overview

### General Features

- **Multi-Account Support**: Reads private keys from `pvkey.txt` to perform actions across multiple accounts.
- **Colorful CLI**: Uses `colorama` for visually appealing output with colored text and borders.
- **Asynchronous Execution**: Built with `asyncio` for efficient blockchain interactions.
- **Error Handling**: Comprehensive error catching for blockchain transactions and RPC issues.
- **Bilingual Support**: Supports both English and Vietnamese output based on user selection.

### Included Scripts

1. **sendtx.py**: Send random TEA transactions or to addresses from `address.txt` on Rise Testnet.
2. **deploytoken.py**: Deploy an ERC20 token smart contract on Rise Testnet.
3. **sendtoken.py**: Send ERC20 tokens to random addresses or from `addressERC20.txt` on Rise Testnet.
4. **nftcollection.py**: Deploy and manage an NFT smart contract (Create, Mint, Burn) on Rise Testnet.
5. **gaspump.py**: Perform GasPump swap operations on Rise Testnet.
6. **clober.py**: Execute Clober swaps (ETH ↔ WETH) on Rise Testnet.
7. **inari.py**: Manage Inari Finance operations (Deposit, Withdraw) on Rise Testnet.
8. **wlgtx.py**: Interact with WL GTX Dex on Rise Testnet.
9. **wlnovadubs.py**: Interact with WL Novadubs on Rise Testnet.

## Prerequisites

Before running the scripts, ensure you have the following installed:

- Python 3.8+
- `pip` (Python package manager)
- **Dependencies**: Install via `pip install -r requirements.txt` (ensure `web3.py`, `colorama`, `asyncio`, `eth-account`, and `inquirer` are included).
- **pvkey.txt**: Add private keys (one per line) for wallet automation.
- Access to the Rise Testnet RPC (e.g., https://testnet.riselabs.xyz).
- **address.txt / addressERC20.txt**: Optional files for specifying recipient addresses.

## Installation

1. **Clone this repository:**
- Open cmd or Shell, then run the command:
```sh
git clone https://github.com/thog9/Rise-testnet.git
```
```sh
cd Rise-testnet
```
2. **Install Dependencies:**
- Open cmd or Shell, then run the command:
```sh
pip install -r requirements.txt
```
3. **Prepare Input Files:**
- Open the `pvkey.txt`: Add your private keys (one per line) in the root directory.
```sh
nano pvkey.txt 
```
- Open the `address.txt`(optional): Add recipient addresses (one per line) for `sendtx.py`, `deploytoken.py`, `sendtoken.py`,`nftcollection.py`, `wlgtx.py`, `wlnovadubs.py`.
```sh
nano address.txt 
```
```sh
nano addressERC20.txt
```
```sh
nano contractERC20.txt
```
```sh
nano contractNFT.txt
```
```sh
nano mail.txt
```
4. **Run:**
- Open cmd or Shell, then run command:
```sh
python main.py
```
- Choose a language (Vietnamese/English).

## Contact

- **Telegram**: [thog099](https://t.me/thog099)
- **Channel**: [CHANNEL](https://t.me/thogairdrops)
- **Group**: [GROUP CHAT](https://t.me/thogchats)
- **X**: [Thog](https://x.com/thog099) 
