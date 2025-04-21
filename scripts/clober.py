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
WETH_ADDRESS = Web3.to_checksum_address("0x4200000000000000000000000000000000000006")

# ABI definitions
WETH_ABI = [
    {"constant": False, "inputs": [], "name": "deposit", "outputs": [], "payable": True, "stateMutability": "payable", "type": "function"},
    {"constant": False, "inputs": [{"name": "wad", "type": "uint256"}], "name": "withdraw", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": False, "inputs": [{"name": "spender", "type": "address"}, {"name": "value", "type": "uint256"}], "name": "approve", "outputs": [{"name": "", "type": "bool"}], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": True, "inputs": [{"name": "owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [{"name": "owner", "type": "address"}, {"name": "spender", "type": "address"}], "name": "allowance", "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"}
]

# Bilingual vocabulary
LANG = {
    'vi': {
        'title': 'CLOBER SWAP - RISE TESTNET',
        'info': 'Thông tin',
        'found': 'Tìm thấy',
        'wallets': 'ví',
        'processing_wallet': 'ĐANG XỬ LÝ VÍ',
        'checking_balance': 'Đang kiểm tra số dư...',
        'insufficient_balance': 'Số dư không đủ',
        'preparing_action': 'Đang chuẩn bị hành động...',
        'sending_tx': 'Đang gửi giao dịch...',
        'success': 'Thành công: {action}',
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
        'action_prompt': 'Chọn hành động [1-2]',
        'invalid_choice': 'Lựa chọn không hợp lệ, vui lòng chọn từ 1-2',
        'amount_prompt': 'Nhập số lượng',
        'invalid_amount': 'Số lượng không hợp lệ, vui lòng nhập số lớn hơn 0',
        'times_prompt': 'Nhập số lần thực hiện',
        'invalid_times': 'Số không hợp lệ, vui lòng nhập số nguyên dương',
        'approve_needed': 'Cần phê duyệt token',
        'approve_success': 'Phê duyệt thành công',
        'approve_failed': 'Phê duyệt thất bại',
        'actions': {
            1: 'Swap ETH → WETH',
            2: 'Swap WETH → ETH'
        }
    },
    'en': {
        'title': 'CLOBER SWAP - RISE TESTNET',
        'info': 'Info',
        'found': 'Found',
        'wallets': 'wallets',
        'processing_wallet': 'PROCESSING WALLET',
        'checking_balance': 'Checking balance...',
        'insufficient_balance': 'Insufficient balance',
        'preparing_action': 'Preparing action...',
        'sending_tx': 'Sending transaction...',
        'success': 'Success: {action}',
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
        'action_prompt': 'Select action [1-2]',
        'invalid_choice': 'Invalid choice, please select from 1-2',
        'amount_prompt': 'Enter amount',
        'invalid_amount': 'Invalid amount, please enter a number greater than 0',
        'times_prompt': 'Enter number of transactions',
        'invalid_times': 'Invalid number, please enter a positive integer',
        'approve_needed': 'Token approval needed',
        'approve_success': 'Approval successful',
        'approve_failed': 'Approval failed',
        'actions': {
            1: 'Swap ETH → WETH',
            2: 'Swap WETH → ETH'
        }
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

def check_balance(w3: Web3, address: str, token_address: str, decimals: int, language: str = 'en') -> float:
    if token_address == "native":
        try:
            balance = w3.eth.get_balance(address)
            return float(w3.from_wei(balance, 'ether'))
        except Exception as e:
            print(f"{Fore.YELLOW}  ⚠ {LANG[language]['error']}: {str(e)}{Style.RESET_ALL}")
            return -1
    else:
        token_abi = WETH_ABI
        checksum_address = Web3.to_checksum_address(token_address)
        contract = w3.eth.contract(address=checksum_address, abi=token_abi)
        try:
            balance = contract.functions.balanceOf(address).call()
            return balance / (10 ** decimals)
        except Exception as e:
            print(f"{Fore.YELLOW}  ⚠ {LANG[language]['error']}: {str(e)}{Style.RESET_ALL}")
            return -1

def display_token_balances(w3: Web3, address: str, language: str = 'en'):
    print_border(f"{LANG[language]['balance']}", Fore.CYAN)
    eth_balance = check_balance(w3, address, "native", 18, language)
    weth_balance = check_balance(w3, address, WETH_ADDRESS, 18, language)
    print(f"{Fore.YELLOW}  - ETH: {eth_balance:.6f}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  - WETH: {weth_balance:.6f}{Style.RESET_ALL}")

async def approve_token(w3: Web3, private_key: str, token_address: str, spender: str, amount: int, language: str = 'en', nonce: int = None):
    account = Account.from_key(private_key)
    token_contract = w3.eth.contract(address=Web3.to_checksum_address(token_address), abi=WETH_ABI)
    if nonce is None:
        nonce = w3.eth.get_transaction_count(account.address, 'pending')
    gas_price = int(w3.eth.gas_price * random.uniform(1.03, 1.1))
    
    try:
        tx = token_contract.functions.approve(Web3.to_checksum_address(spender), amount).build_transaction({
            'nonce': nonce,
            'from': account.address,
            'chainId': CHAIN_ID,
            'gasPrice': gas_price
        })
        tx['gas'] = w3.eth.estimate_gas(tx) if w3.eth.estimate_gas(tx) else 100000
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180))
        if receipt.status == 1:
            print(f"{Fore.GREEN}  ✔ {LANG[language]['approve_success']}{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}  ✖ {LANG[language]['approve_failed']}{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}  ✖ {LANG[language]['approve_failed']}: {str(e)}{Style.RESET_ALL}")
        return False

async def execute_action(w3: Web3, private_key: str, wallet_index: int, action: int, amount_in: float, times: int, language: str = 'en'):
    account = Account.from_key(private_key)
    sender_address = account.address
    successful_txs = 0
    
    nonce = w3.eth.get_transaction_count(sender_address, 'pending')
    
    weth_contract = w3.eth.contract(address=WETH_ADDRESS, abi=WETH_ABI)
    
    for i in range(times):
        print_border(f"Transaction {i+1}/{times}: {LANG[language]['actions'][action]}", Fore.YELLOW)
        print(f"{Fore.CYAN}  > {LANG[language]['checking_balance']}{Style.RESET_ALL}")
        
        eth_balance = check_balance(w3, sender_address, "native", 18, language)
        weth_balance = check_balance(w3, sender_address, WETH_ADDRESS, 18, language)
        
        amount_wei = int(amount_in * 10 ** 18)
        
        if eth_balance < 0.000001:
            print(f"{Fore.RED}  ✖ {LANG[language]['insufficient_balance']}: {eth_balance:.4f} ETH < 0.000001 ETH{Style.RESET_ALL}")
            break
        
        if action == 1 and eth_balance < amount_in:
            print(f"{Fore.RED}  ✖ {LANG[language]['insufficient_balance']}: {eth_balance:.6f} ETH{Style.RESET_ALL}")
            break
        elif action == 2 and weth_balance < amount_in:
            print(f"{Fore.RED}  ✖ {LANG[language]['insufficient_balance']}: {weth_balance:.6f} WETH{Style.RESET_ALL}")
            break
        
        print(f"{Fore.CYAN}  > {LANG[language]['preparing_action']}{Style.RESET_ALL}")
        gas_price = int(w3.eth.gas_price * random.uniform(1.03, 1.1))
        
        try:
            if action == 1:  # Swap ETH → WETH
                tx = weth_contract.functions.deposit().build_transaction({
                    'nonce': nonce,
                    'from': sender_address,
                    'value': amount_wei,
                    'chainId': CHAIN_ID,
                    'gasPrice': gas_price
                })
                tx['gas'] = w3.eth.estimate_gas(tx) if w3.eth.estimate_gas(tx) else 100000
            else:  # Swap WETH → ETH
                if not await approve_token(w3, private_key, WETH_ADDRESS, WETH_ADDRESS, amount_wei, language, nonce):
                    break
                nonce += 1
                tx = weth_contract.functions.withdraw(amount_wei).build_transaction({
                    'nonce': nonce,
                    'from': sender_address,
                    'chainId': CHAIN_ID,
                    'gasPrice': gas_price
                })
                tx['gas'] = w3.eth.estimate_gas(tx) if w3.eth.estimate_gas(tx) else 100000
            
            print(f"{Fore.YELLOW}    Gas estimated: {tx['gas']}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}  > {LANG[language]['sending_tx']}{Style.RESET_ALL}")
            signed_tx = w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            tx_link = f"{EXPLORER_URL}{tx_hash.hex()}"
            
            receipt = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180))
            
            if receipt.status == 1:
                successful_txs += 1
                eth_balance_after = check_balance(w3, sender_address, "native", 18, language)
                weth_balance_after = check_balance(w3, sender_address, WETH_ADDRESS, 18, language)
                print(f"{Fore.GREEN}  ✔ {LANG[language]['success'].format(action=LANG[language]['actions'][action])} │ Tx: {tx_link}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}    {LANG[language]['address']:<12}: {sender_address}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}    {LANG[language]['block']:<12}: {receipt['blockNumber']}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}    {LANG[language]['gas']:<12}: {receipt['gasUsed']}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}    {LANG[language]['balance']:<12}: {eth_balance_after:.6f} ETH | WETH: {weth_balance_after:.6f}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}  ✖ {LANG[language]['failure']} │ Tx: {tx_link}{Style.RESET_ALL}")
                break
            
            nonce += 1
            if i < times - 1:
                delay = random.uniform(30, 60)
                print(f"{Fore.YELLOW}    {LANG[language]['pausing']} {delay:.2f} {LANG[language]['seconds']}{Style.RESET_ALL}")
                await asyncio.sleep(delay)
        
        except Exception as e:
            print(f"{Fore.RED}  ✖ {LANG[language]['failure']}: {str(e)}{Style.RESET_ALL}")
            break
    
    return successful_txs

async def run_clober(language: str = 'en'):
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

    total_txs = 0
    successful_txs = 0

    random.shuffle(private_keys)
    for i, (profile_num, private_key) in enumerate(private_keys, 1):
        print_border(f"{LANG[language]['processing_wallet']} {profile_num} ({i}/{len(private_keys)})", Fore.MAGENTA)
        account = Account.from_key(private_key)
        print(f"{Fore.YELLOW}  {LANG[language]['address']}: {account.address}{Style.RESET_ALL}")
        display_token_balances(w3, account.address, language)
        print_separator()

        # Hiển thị danh sách hành động
        print(f"{Fore.CYAN}{LANG[language]['action_prompt']}{Style.RESET_ALL}")
        for idx in range(1, 3):
            print(f"{Fore.YELLOW}  {idx}. {LANG[language]['actions'][idx]}{Style.RESET_ALL}")

        print()
        while True:
            print(f"{Fore.CYAN}Select action [1-2]:{Style.RESET_ALL}")
            try:
                action = int(input(f"{Fore.GREEN}  > {Style.RESET_ALL}"))
                if 1 <= action <= 2:
                    break
                print(f"{Fore.RED}  ✖ {LANG[language]['invalid_choice']}{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}  ✖ {LANG[language]['invalid_choice']}{Style.RESET_ALL}")

        # Kiểm tra số dư tối đa
        eth_balance = check_balance(w3, account.address, "native", 18, language)
        weth_balance = check_balance(w3, account.address, WETH_ADDRESS, 18, language)
        max_amount = eth_balance if action == 1 else weth_balance

        print()
        while True:
            print(f"{Fore.CYAN}{LANG[language]['amount_prompt']} {Fore.YELLOW}(Max: {max_amount:.4f} {'ETH' if action == 1 else 'WETH'}){Style.RESET_ALL}")
            try:
                amount_input = float(input(f"{Fore.GREEN}  > {Style.RESET_ALL}"))
                if amount_input > 0 and amount_input <= max_amount:
                    break
                print(f"{Fore.RED}  ✖ {LANG[language]['invalid_amount']} or exceeds balance{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}  ✖ {LANG[language]['invalid_amount']}{Style.RESET_ALL}")

        print()
        while True:
            print(f"{Fore.CYAN}{LANG[language]['times_prompt']}:{Style.RESET_ALL}")
            try:
                times = int(input(f"{Fore.GREEN}  > {Style.RESET_ALL}"))
                if times > 0:
                    break
                print(f"{Fore.RED}  ✖ {LANG[language]['invalid_times']}{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}  ✖ {LANG[language]['invalid_times']}{Style.RESET_ALL}")

        print()
        txs = await execute_action(w3, private_key, profile_num, action, amount_input, times, language)
        successful_txs += txs
        total_txs += times

        if i < len(private_keys):
            delay = random.uniform(10, 30)
            print(f"{Fore.YELLOW}  ℹ {LANG[language]['pausing']} {delay:.2f} {LANG[language]['seconds']}{Style.RESET_ALL}")
            await asyncio.sleep(delay)
        print_separator()
    
    print()
    print_border(f"{LANG[language]['completed'].format(successful=successful_txs, total=total_txs)}", Fore.GREEN)
    print()

if __name__ == "__main__":
    asyncio.run(run_clober('en'))
