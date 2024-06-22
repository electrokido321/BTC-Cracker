# Bitcoin Wallet Recovery Tool

Its free so maybe an donation?
All the way 👇 

https://discord.com/invite/yyBgY7pGqX

I am @Coding_Kido

## Overview

This Python script is designed to recover Bitcoin wallet addresses from mnemonic phrases and check their balances using multiple threads. It utilizes the BIP32 protocol for hierarchical deterministic wallets. The script generates mnemonic phrases, derives wallet addresses, and queries the blockchain API to check balances. If a non-zero balance is found, it logs the details to a file named "wallet.txt".

## Disclaimer
âš ï¸ Disclaimer âš ï¸

This script is developed for educational and research purposes only.

By using this code, you agree to the following:

- You will not use this code, in whole or in part, for malicious intent, including but not limited to unauthorized mining on third-party systems.
- You will seek explicit permission from any and all system owners before running or deploying this code.
- You understand the implications of running mining software on hardware, including the potential for increased wear and power consumption.
- The creator of this script cannot and will not be held responsible for any damages, repercussions, or any negative outcomes that result from using this script.
- If you do not agree to these terms, please do not use or distribute this code.


## Features

- **Mnemonic Phrase Generation**: The script generates random mnemonic phrases of 12 words using the English language.
- **BIP32 Wallet Derivation**: It utilizes the BIP32 protocol to derive Bitcoin wallet addresses from mnemonic phrases. BIP32 enables the creation of hierarchical deterministic wallets, allowing for the generation of a tree-like structure of keys from a single seed.
- **Balance Checking**: The script queries the blockchain.info API to check the Bitcoin balance of derived wallet addresses.
- **Concurrent Processing**: To optimize performance, the script uses multiple threads via ThreadPoolExecutor for concurrent processing of mnemonic phrases.
- **Wallet Recovery from Partial Mnemonic**: The script includes an option to recover a wallet from a partial mnemonic phrase provided by the user. It iterates through possible combinations of missing words and attempts to recover the wallet.


## Installation

I will provide Everything needed

## How to use

2. Follow the on-screen prompts to choose between recovering a wallet from a partial mnemonic or checking random wallets.
3. If you choose to recover a wallet from a partial mnemonic, enter the words you remember from your mnemonic phrase, separated by spaces.
4. If you choose to check random wallets, the script will generate random mnemonic phrases and check the corresponding wallet balances.
5. If a wallet with a non-zero balance is found, the script will log the mnemonic phrase, wallet address, and balance to the `wallet.txt` file.

## How to Open the Discovered Wallet

For assistance with accessing the wallet, reach out to me on Discord ( username: **@Coding_Kido** ). I will personally help you!


# can send a donation to the following addresses:

BTC: bc1qr5hcejg2nkclzgm8xrdzpcf36rngchmtuawnnw

## Star ðŸŒŸ

Don't forget to star and watch the repo for updates. Your support is greatly appreciated!
