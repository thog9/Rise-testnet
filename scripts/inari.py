import os
import sys
import asyncio
import random
from web3 import Web3
from eth_account import Account
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Border width
BORDER_WIDTH = 80

# Constants
NETWORK_URL = "https://testnet.riselabs.xyz"
CHAIN_ID = 11155931
EXPLORER_URL = "https://explorer.testnet.riselabs.xyz/tx/0x"
INARI_ADDRESS = Web3.to_checksum_address("0x81edb206Fd1FB9dC517B61793AaA0325c8d11A23")

# ABI definitions
INARI_ABI = [
    {
        "type": "function",
        "name": "supply",
        "inputs": [
            {"name": "asset", "type": "address", "internalType": "address"},
            {"name": "amount", "type": "uint256", "internalType": "uint256"},
            {"name": "onBehalfOf", "type": "address", "internalType": "address"},
            {"name": "referralCode", "type": "uint16", "internalType": "uint16"}
        ],
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

ERC20_ABI = [
    {
        "type": "function",
        "name": "allowance",
        "stateMutability": "view",
        "inputs": [
            {"name": "owner", "type": "address", "internalType": "address"},
            {"name": "spender", "type": "address", "internalType": "address"}
        ],
        "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}]
    },
    {
        "type": "function",
        "name": "approve",
        "inputs": [
            {"name": "spender", "type": "address", "internalType": "address"},
            {"name": "value", "type": "uint256", "internalType": "uint256"}
        ],
        "outputs": [{"name": "", "type": "bool", "internalType": "bool"}]
    },
    {
        "type": "function",
        "name": "balanceOf",
        "stateMutability": "view",
        "inputs": [
            {"name": "owner", "type": "address", "internalType": "address"}
        ],
        "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}]
    },
    {
        "type": "function",
        "name": "decimals",
        "stateMutability": "view",
        "inputs": [],
        "outputs": [{"name": "", "type": "uint8", "internalType": "uint8"}]
    }
]

# Token configurations
TOKENS = [
    ("WBTC", "0xF32D39ff9f6Aa7a7A64d7a4F00a54826Ef791a55", "0x81edb206Fd1FB9dC517B61793AaA0325c8d11A23"),
    ("USDC", "0x8A93d247134d91e0de6f96547cB0204e5BE8e5D8", "0x81edb206Fd1FB9dC517B61793AaA0325c8d11A23"),
    ("USDT", "0x40918ba7f132e0acba2ce4de4c4baf9bd2d7d849", "0x81edb206Fd1FB9dC517B61793AaA0325c8d11A23"),
    ("WETH", "0x4200000000000000000000000000000000000006", "0x81edb206Fd1FB9dC517B61793AaA0325c8d11A23"),
]

# Bilingual vocabulary
LANG = {
    'vi': {
        'title': '🌸 INARI BANK - RISE TESTNET 🌸',
        'info': 'Thông tin',
        'found': 'Tìm thấy',
        'wallets': 'ví',
        'wallet_balances': 'Số dư ví',
        'processing_wallet': 'ĐANG XỬ LÝ VÍ',
        'checking_balance': 'Đang kiểm tra số dư...',
        'insufficient_balance': 'Số dư không đủ',
        'no_tokens': 'Không đủ số dư cho token {token}',
        'preparing_action': 'Đang chuẩn bị hành động...',
        'approving_token': 'Đang phê duyệt {token}...',
        'supplying_token': 'Đang gửi {amount:.6f} {token} vào Inari Bank...',
        'success': 'Thành công: Gửi {amount:.6f} {token} vào Inari Bank',
        'failure': 'Giao dịch thất bại',
        'address': 'Địa chỉ',
        'amount': 'Số lượng',
        'gas': 'Gas',
        'block': 'Khối',
        'balance': 'Số dư',
        'pausing': 'Tạm dừng',
        'seconds': 'giây',
        'completed': 'HOÀN THÀNH: {successful}/{total} GIAO DỊCH THÀNH CÔNG',
        'error': 'Lỗi',
        'connect_success': 'Thành công: Đã kết nối với mạng Rise Testnet',
        'connect_error': 'Không thể kết nối với RPC',
        'web3_error': 'Kết nối Web3 thất bại',
        'pvkey_not_found': 'Không tìm thấy tệp pvkey.txt',
        'pvkey_empty': 'Không tìm thấy khóa riêng hợp lệ',
        'pvkey_error': 'Không thể đọc pvkey.txt',
        'invalid_key': 'không hợp lệ, đã bỏ qua',
        'warning_line': 'Cảnh báo: Dòng',
        'token_prompt': 'Chọn token để deposit [1-4]',
        'invalid_token': 'Token không hợp lệ, vui lòng chọn từ 1-4',
        'amount_prompt': 'Nhập số lượng {token} (Chọn "0" ngẫu nhiên hoặc nhập số lượng, mặc định ngẫu nhiên)',
        'invalid_amount': 'Số lượng không hợp lệ, vui lòng nhập số lớn hơn hoặc bằng 0',
        'times_prompt': 'Nhập số lần thực hiện',
        'invalid_times': 'Số không hợp lệ, vui lòng nhập số nguyên dương',
    },
    'en': {
        'title': '🌸 INARI BANK - RISE TESTNET 🌸',
        'info': 'Info',
        'found': 'Found',
        'wallets': 'wallets',
        'wallet_balances': 'Wallet Balances',
        'processing_wallet': 'PROCESSING WALLET',
        'checking_balance': 'Checking balance...',
        'insufficient_balance': 'Insufficient balance',
        'no_tokens': 'Insufficient balance for token {token}',
        'preparing_action': 'Preparing action...',
        'approving_token': 'Approving {token}...',
        'supplying_token': 'Supplying {amount:.6f} {token} to Inari Bank...',
        'success': 'Success: Supplied {amount:.6f} {token} to Inari Bank',
        'failure': 'Transaction failed',
        'address': 'Address',
        'amount': 'Amount',
        'gas': 'Gas',
        'block': 'Block',
        'balance': 'Balance',
        'pausing': 'Pausing',
        'seconds': 'seconds',
        'completed': 'COMPLETED: {successful}/{total} TRANSACTIONS SUCCESSFUL',
        'error': 'Error',
        'connect_success': 'Success: Connected to Rise Testnet',
        'connect_error': 'Failed to connect to RPC',
        'web3_error': 'Web3 connection failed',
        'pvkey_not_found': 'pvkey.txt file not found',
        'pvkey_empty': 'No valid private keys found',
        'pvkey_error': 'Failed to read pvkey.txt',
        'invalid_key': 'is invalid, skipped',
        'warning_line': 'Warning: Line',
        'token_prompt': 'Select token to deposit [1-4]',
        'invalid_token': 'Invalid token, please select from 1-4',
        'amount_prompt': 'Enter {token} amount (Select "0" randomly or enter quantity, default random)',
        'invalid_amount': 'Invalid amount, please enter a number greater than or equal to 0',
        'times_prompt': 'Enter number of transactions',
        'invalid_times': 'Invalid number, please enter a positive integer',
    }
}

# Display functions
def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."
    padded_text = f" {text} ".center(width - 2)
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│{padded_text}│{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

def print_separator(color=Fore.MAGENTA):
    print(f"{color}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")

# Utility functions
def is_valid_private_key(key: str) -> bool:
    key = key.strip()
    if not key.startswith('0x'):
        key = '0x' + key
    try:
        bytes.fromhex(key.replace('0x', ''))
        return len(key) == 66
    except ValueError:
        return False

def load_private_keys(file_path: str = "pvkey.txt", language: str = 'en') -> list:
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.RED}  ✖ {LANG[language]['pvkey_not_found']}{Style.RESET_ALL}")
            with open(file_path, 'w') as f:
                f.write("# Add private keys here, one per line\n# Example: 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef\n")
            sys.exit(1)
        
        valid_keys = []
        with open(file_path, 'r') as f:
            for i, line in enumerate(f, 1):
                key = line.strip()
                if key and not key.startswith('#'):
                    if is_valid_private_key(key):
                        if not key.startswith('0x'):
                            key = '0x' + key
                        valid_keys.append((i, key))
                    else:
                        print(f"{Fore.YELLOW}  ⚠ {LANG[language]['warning_line']} {i} {LANG[language]['invalid_key']}: {key}{Style.RESET_ALL}")
        
        if not valid_keys:
            print(f"{Fore.RED}  ✖ {LANG[language]['pvkey_empty']}{Style.RESET_ALL}")
            sys.exit(1)
        
        return valid_keys
    except Exception as e:
        print(f"{Fore.RED}  ✖ {LANG[language]['pvkey_error']}: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

def connect_web3(language: str = 'en'):
    try:
        w3 = Web3(Web3.HTTPProvider(NETWORK_URL))
        if not w3.is_connected():
            print(f"{Fore.RED}  ✖ {LANG[language]['connect_error']}{Style.RESET_ALL}")
            sys.exit(1)
        print(f"{Fore.GREEN}  ✔ {LANG[language]['connect_success']} │ Chain ID: {w3.eth.chain_id}{Style.RESET_ALL}")
        return w3
    except Exception as e:
        print(f"{Fore.RED}  ✖ {LANG[language]['web3_error']}: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

def check_balance(w3: Web3, address: str, token: str, token_address: str = None, language: str = 'en') -> float:
    if token == "ETH":
        try:
            balance = w3.eth.get_balance(address)
            return float(w3.from_wei(balance, 'ether'))
        except Exception as e:
            print(f"{Fore.YELLOW}  ⚠ {LANG[language]['error']}: {str(e)}{Style.RESET_ALL}")
            return -1
    else:
        try:
            contract = w3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
            balance = contract.functions.balanceOf(address).call()
            decimals = contract.functions.decimals().call()
            return balance / (10 ** decimals)
        except Exception as e:
            print(f"{Fore.YELLOW}  ⚠ {LANG[language]['error']}: {token} balance fetch failed{Style.RESET_ALL}")
            return 0

def display_wallet_balances(w3: Web3, private_keys: list, language: str = 'en'):
    print_border(f"{LANG[language]['wallet_balances']}", Fore.CYAN)
    for i, (profile_num, private_key) in enumerate(private_keys, 1):
        account = Account.from_key(private_key)
        address = account.address
        print(f"{Fore.YELLOW}  Wallet {profile_num} ({address[:8]}...{address[-8:]}):{Style.RESET_ALL}")
        eth_balance = check_balance(w3, address, "ETH", None, language)
        print(f"{Fore.YELLOW}    - ETH : {eth_balance:.6f}{Style.RESET_ALL}")
        for token_name, token_address, _ in TOKENS:
            token_balance = check_balance(w3, address, token_name, token_address, language)
            print(f"{Fore.YELLOW}    - {token_name:<4}: {token_balance:.6f}{Style.RESET_ALL}")
    print_separator()

async def approve_token(w3: Web3, private_key: str, token: tuple, amount_wei: int, language: str = 'en') -> bool:
    account = Account.from_key(private_key)
    address = account.address
    token_name, token_address, spender = token
    contract = w3.eth.contract(address=Web3.to_checksum_address(token_address), abi=ERC20_ABI)
    
    try:
        allowance = contract.functions.allowance(address, Web3.to_checksum_address(spender)).call()
        if amount_wei <= allowance:
            return True
        
        print(f"{Fore.CYAN}  > {LANG[language]['approving_token'].format(token=token_name)}{Style.RESET_ALL}")
        tx = contract.functions.approve(
            Web3.to_checksum_address(spender),
            2**256 - 1
        ).build_transaction({
            'from': address,
            'nonce': w3.eth.get_transaction_count(address, 'pending'),
            'gasPrice': int(w3.eth.gas_price * random.uniform(1.03, 1.1)),
            'chainId': CHAIN_ID
        })
        tx['gas'] = w3.eth.estimate_gas(tx) if w3.eth.estimate_gas(tx) else 100000
        
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180))
        
        if receipt.status == 1:
            print(f"{Fore.GREEN}  ✔ Approved {token_name}{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}  ✖ Approval failed{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}  ✖ Approval failed: {str(e)}{Style.RESET_ALL}")
        return False

async def execute_action(w3: Web3, private_key: str, wallet_index: int, token: tuple, amount_in: float, times: int, language: str = 'en'):
    account = Account.from_key(private_key)
    address = account.address
    successful_txs = 0
    token_name, token_address, spender = token
    
    for i in range(times):
        print_border(f"Transaction {i+1}/{times}: Supply {token_name} to Inari Bank (Wallet {wallet_index})", Fore.YELLOW)
        print(f"{Fore.CYAN}  > {LANG[language]['checking_balance']}{Style.RESET_ALL}")
        
        eth_balance = check_balance(w3, address, "ETH", None, language)
        if eth_balance < 0.000001:
            print(f"{Fore.RED}  ✖ {LANG[language]['insufficient_balance']}: {eth_balance:.6f} ETH < 0.000001 ETH{Style.RESET_ALL}")
            break
        
        token_balance = check_balance(w3, address, token_name, token_address, language)
        if token_balance <= 0:
            print(f"{Fore.RED}  ✖ {LANG[language]['no_tokens'].format(token=token_name)}{Style.RESET_ALL}")
            break
        
        amount_wei = 0
        amount = 0
        if amount_in == 0:
            amount = token_balance * random.uniform(0.2, 0.4)
            amount_wei = int(amount * 10**18)
        else:
            amount = amount_in
            amount_wei = int(amount * 10**18)
            if amount > token_balance:
                print(f"{Fore.RED}  ✖ {LANG[language]['insufficient_balance']}: {amount:.6f} {token_name} (Available: {token_balance:.6f}){Style.RESET_ALL}")
                break
        
        print(f"{Fore.CYAN}  > {LANG[language]['preparing_action']}{Style.RESET_ALL}")
        
        # Approve token if needed
        if not await approve_token(w3, private_key, token, amount_wei, language):
            break
        
        # Supply token
        try:
            contract = w3.eth.contract(address=INARI_ADDRESS, abi=INARI_ABI)
            print(f"{Fore.CYAN}  > {LANG[language]['supplying_token'].format(amount=amount, token=token_name)}{Style.RESET_ALL}")
            tx = contract.functions.supply(
                Web3.to_checksum_address(token_address),
                amount_wei,
                address,
                0
            ).build_transaction({
                'from': address,
                'nonce': w3.eth.get_transaction_count(address, 'pending'),
                'gasPrice': int(w3.eth.gas_price * random.uniform(1.03, 1.1)),
                'chainId': CHAIN_ID
            })
            tx['gas'] = w3.eth.estimate_gas(tx) if w3.eth.estimate_gas(tx) else 200000
            
            signed_tx = w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            tx_link = f"{EXPLORER_URL}{tx_hash.hex()}"
            
            receipt = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180))
            
            if receipt.status == 1:
                successful_txs += 1
                print(f"{Fore.GREEN}  ✔ {LANG[language]['success'].format(amount=amount, token=token_name)} │ Tx: {tx_link}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}    {LANG[language]['address']:<12}: {address[:8]}...{address[-8:]}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}    {LANG[language]['block']:<12}: {receipt['blockNumber']}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}    {LANG[language]['gas']:<12}: {receipt['gasUsed']}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}    {LANG[language]['balance']:<12}: {Style.RESET_ALL}", end="")
                eth_balance = check_balance(w3, address, "ETH", None, language)
                token_balance = check_balance(w3, address, token_name, token_address, language)
                print(f"{Fore.YELLOW} {eth_balance:.6f} ETH | {Fore.YELLOW}{token_name}: {token_balance:.6f}")
            else:
                print(f"{Fore.RED}  ✖ {LANG[language]['failure']} │ Tx: {tx_link}{Style.RESET_ALL}")
                break
            
            if i < times - 1:
                delay = random.uniform(30, 60)
                print(f"{Fore.YELLOW}    {LANG[language]['pausing']} {delay:.2f} {LANG[language]['seconds']}{Style.RESET_ALL}")
                await asyncio.sleep(delay)
        
        except Exception as e:
            print(f"{Fore.RED}  ✖ {LANG[language]['failure']}: {str(e)}{Style.RESET_ALL}")
            break
    
    return successful_txs

async def run_inari(language: str = 'en'):
    print()
    print_border(LANG[language]['title'], Fore.CYAN)
    print()

    private_keys = load_private_keys('pvkey.txt', language)
    print(f"{Fore.YELLOW}  ℹ {LANG[language]['info']}: {LANG[language]['found']} {len(private_keys)} {LANG[language]['wallets']}{Style.RESET_ALL}")
    print()

    if not private_keys:
        return

    w3 = connect_web3(language)
    print()

    # Display wallet balances before input
    display_wallet_balances(w3, private_keys, language)

    # Chọn token
    print(f"{Fore.CYAN}{LANG[language]['token_prompt']}{Style.RESET_ALL}")
    for idx, (token_name, _, _) in enumerate(TOKENS, 1):
        print(f"{Fore.YELLOW}  {idx}. {token_name}{Style.RESET_ALL}")
    print()
    while True:
        print(f"{Fore.CYAN}Select token [1-4]:{Style.RESET_ALL}")
        try:
            token_idx = int(input(f"{Fore.GREEN}  > {Style.RESET_ALL}"))
            if 1 <= token_idx <= len(TOKENS):
                selected_token = TOKENS[token_idx - 1]
                break
            print(f"{Fore.RED}  ✖ {LANG[language]['invalid_token']}{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}  ✖ {LANG[language]['invalid_token']}{Style.RESET_ALL}")

    # Nhập số lượng
    print()
    while True:
        print(f"{Fore.CYAN}{LANG[language]['amount_prompt'].format(token=selected_token[0])}{Style.RESET_ALL}:")
        try:
            amount_input = float(input(f"{Fore.GREEN}  > {Style.RESET_ALL}"))
            if amount_input >= 0:
                break
            print(f"{Fore.RED}  ✖ {LANG[language]['invalid_amount']}{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}  ✖ {LANG[language]['invalid_amount']}{Style.RESET_ALL}")

    # Nhập số lần thực hiện
    print()
    while True:
        print(f"{Fore.CYAN}{LANG[language]['times_prompt']}{Style.RESET_ALL}:")
        try:
            times = int(input(f"{Fore.GREEN}  > {Style.RESET_ALL}"))
            if times > 0:
                break
            print(f"{Fore.RED}  ✖ {LANG[language]['invalid_times']}{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}  ✖ {LANG[language]['invalid_times']}{Style.RESET_ALL}")

    total_txs = 0
    successful_txs = 0

    random.shuffle(private_keys)
    for i, (profile_num, private_key) in enumerate(private_keys, 1):
        print_border(f"{LANG[language]['processing_wallet']} {profile_num} ({Account.from_key(private_key).address[:8]}...{Account.from_key(private_key).address[-8:]})", Fore.MAGENTA)
        successful = await execute_action(w3, private_key, profile_num, selected_token, amount_input, times, language)
        successful_txs += successful
        total_txs += times

    print()
    print_border(f"{LANG[language]['completed'].format(successful=successful_txs, total=total_txs)}", Fore.GREEN)
    print()

if __name__ == "__main__":
    asyncio.run(run_inari('en'))
