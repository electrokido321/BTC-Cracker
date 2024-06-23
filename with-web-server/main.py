import subprocess
import sys
import mnemonic
import bip32utils
import requests
import logging
import time
import os
import itertools
from licensing.models import *
from licensing.methods import Key, Helpers
from colorama import Fore, Style, init
from flask import Flask, request, render_template_string

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

packages = [
    'mnemonic',
    'bip32utils',
    'requests',
    'licensing',
    'colorama',
    'flask'
]

pre_installed = {
    'logging',
    'time',
    'os',
    'itertools',
    'sys'
}

# Install required packages
for package in packages:
    try:
        __import__(package)
    except ImportError:
        install(package)

# ANSI escape code for green text
GREEN = "\033[92m"
RESET = "\033[0m"

# Save the original stdout.write method
original_write = sys.stdout.write

# Define a new write method that adds the green color to all output
def green_write(text):
    original_write(f"{GREEN}{text}{RESET}")

# Override the default stdout.write method
sys.stdout.write = green_write

def generate_mnemonic():
    mnemo = mnemonic.Mnemonic("english")
    return mnemo.generate(strength=128)

def recover_wallet_from_mnemonic(mnemonic_phrase):
    seed = mnemonic.Mnemonic.to_seed(mnemonic_phrase)
    root_key = bip32utils.BIP32Key.fromEntropy(seed)
    child_key = root_key.ChildKey(44 | bip32utils.BIP32_HARDEN).ChildKey(0 | bip32utils.BIP32_HARDEN).ChildKey(0 | bip32utils.BIP32_HARDEN).ChildKey(0).ChildKey(0)
    address = child_key.Address()
    balance = check_BTC_balance(address)
    return mnemonic_phrase, balance, address

def recover_wallet_from_partial_mnemonic(partial_mnemonic):
    partial_mnemonic_words = partial_mnemonic.split()
    if len(partial_mnemonic_words) >= 12:
        logging.error("Provided mnemonic phrase should contain less than 12 words.")
        return None, 0, None

    provided_words = len(partial_mnemonic_words)
    missing_words = 12 - provided_words
    logging.info(f"Attempting to recover wallet from {provided_words} words. Missing {missing_words} words.")

    wordlist = mnemonic.Mnemonic("english").wordlist
    for guess in itertools.product(wordlist, repeat=missing_words):
        full_mnemonic = ' '.join(partial_mnemonic_words + list(guess))
        mnemonic_phrase, balance, address = recover_wallet_from_mnemonic(full_mnemonic)
        logging.info(f"Trying mnemonic phrase: {full_mnemonic}")
        logging.info(f"Wallet Address: {address}, Balance: {balance} BTC")
        if balance > 0:
            logging.info(f"Found wallet with non-zero balance: {balance} BTC")
            logging.info(f"Mnemonic Phrase: {mnemonic_phrase}")
            with open("wallet.txt", "a") as f:
                f.write(f"Mnemonic Phrase: {mnemonic_phrase}\n")
                f.write(f"Wallet Address: {address}\n")
                f.write(f"Balance: {balance} BTC\n\n")
            return mnemonic_phrase, balance, address

    logging.info("No wallet found with the provided partial mnemonic phrase.")
    return None, 0, None

def check_BTC_balance(address, retries=3, delay=5):
    for attempt in range(retries):
        try:
            response = requests.get(f"https://blockchain.info/balance?active={address}", timeout=10)
            response.raise_for_status()
            data = response.json()
            balance = data[address]["final_balance"]
            return balance / 100000000
        except requests.RequestException as e:
            if attempt < retries - 1:
                logging.error(f"Error checking balance, retrying in {delay} seconds: {str(e)}")
                time.sleep(delay)
            else:
                logging.error("Error checking balance: %s", str(e))
    return 0

# Create Flask app
app = Flask(__name__)
workers = {}

@app.route('/')
def index():
    return render_template_string('''
        <form method="post" action="/add_worker">
            Worker Name: <input type="text" name="worker_name"><br>
            Mnemonic Phrase: <input type="text" name="partial_mnemonic"><br>
            <input type="submit" value="Recover Wallet">
        </form>
        <form method="post" action="/generate_wallets">
            <input type="submit" value="Check Random Wallets">
        </form>
        <hr>
        <h2>Worker Data</h2>
        <ul>
        {% for worker, data in workers.items() %}
            <li>
                <strong>{{ worker }}</strong><br>
                Mnemonic Phrase: {{ data.mnemonic_phrase }}<br>
                Address: {{ data.address }}<br>
                Balance: {{ data.balance }} BTC
            </li>
        {% endfor %}
        </ul>
    ''', workers=workers)

@app.route('/add_worker', methods=['POST'])
def add_worker():
    worker_name = request.form['worker_name']
    partial_mnemonic = request.form['partial_mnemonic']
    mnemonic_phrase, balance, address = recover_wallet_from_partial_mnemonic(partial_mnemonic)
    workers[worker_name] = {'mnemonic_phrase': mnemonic_phrase, 'balance': balance, 'address': address}
    return 'Worker added successfully!<br><a href="/">Back to Home</a>'

@app.route('/generate_wallets', methods=['POST'])
def generate_wallets():
    worker_name = "RandomWorker"
    mnemonic_count = 0
    while mnemonic_count < 10:  # Limit to 10 attempts for demonstration
        mnemonic_phrase = generate_mnemonic()
        mnemonic_phrase, balance, address = recover_wallet_from_mnemonic(mnemonic_phrase)
        logging.info(f"Mnemonic Phrase: {mnemonic_phrase}")
        logging.info(f"Wallet Address: {address}")
        if balance > 0:
            logging.info(f"Found wallet with non-zero balance: {balance} BTC")
            with open("wallet.txt", "a") as f:
                f.write(f"Mnemonic Phrase: {mnemonic_phrase}\n")
                f.write(f"Wallet Address: {address}\n")
                f.write(f"Balance: {balance} BTC\n\n")
            workers[worker_name + str(mnemonic_count)] = {'mnemonic_phrase': mnemonic_phrase, 'balance': balance, 'address': address}
        mnemonic_count += 1
    return 'Generated random wallets!<br><a href="/">Back to Home</a>'

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Start Flask server
    app.run(debug=True)
