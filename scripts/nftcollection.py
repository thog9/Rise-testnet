import os
import sys
import asyncio
from web3 import Web3
from eth_account import Account
from solcx import compile_source, install_solc, get_solc_version
from colorama import init, Fore, Style

# Khởi tạo colorama
init(autoreset=True)

# Độ rộng viền
BORDER_WIDTH = 80

# Constants
NETWORK_URLS = ['https://testnet.riselabs.xyz']
CHAIN_ID = 11155931
EXPLORER_URL = "https://explorer.testnet.riselabs.xyz"
SOLC_VERSION = "0.8.19"  # Phiên bản Solidity không dùng PUSH0

# NFT Contract Source Code
NFT_CONTRACT_SOURCE = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract NFTCollection {
    address public owner;
    string public name;
    string public symbol;
    uint256 public maxSupply;
    uint256 public totalSupply;

    mapping(uint256 => address) private _owners;
    mapping(address => uint256) private _balances;
    mapping(uint256 => string) private _tokenURIs;

    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event Mint(address indexed to, uint256 indexed tokenId, string tokenURI);
    event Burn(address indexed from, uint256 indexed tokenId);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }

    modifier tokenExists(uint256 tokenId) {
        require(_owners[tokenId] != address(0), "Token doesn't exist");
        _;
    }

    constructor(string memory _name, string memory _symbol, uint256 _maxSupply) {
        owner = msg.sender;
        name = _name;
        symbol = _symbol;
        maxSupply = _maxSupply;
        totalSupply = 0;
    }

    function mint(address to, uint256 tokenId, string memory tokenURI) public onlyOwner {
        require(to != address(0), "Cannot mint to zero address");
        require(_owners[tokenId] == address(0), "Token already exists");
        require(totalSupply < maxSupply, "Maximum supply reached");

        _owners[tokenId] = to;
        _balances[to]++;
        _tokenURIs[tokenId] = tokenURI;
        totalSupply++;

        emit Transfer(address(0), to, tokenId);
        emit Mint(to, tokenId, tokenURI);
    }

    function burn(uint256 tokenId) public tokenExists(tokenId) {
        address tokenOwner = _owners[tokenId];
        require(msg.sender == tokenOwner || msg.sender == owner, "Not authorized to burn");

        delete _tokenURIs[tokenId];
        delete _owners[tokenId];
        _balances[tokenOwner]--;
        totalSupply--;

        emit Transfer(tokenOwner, address(0), tokenId);
        emit Burn(tokenOwner, tokenId);
    }

    function tokenURI(uint256 tokenId) public view tokenExists(tokenId) returns (string memory) {
        return _tokenURIs[tokenId];
    }

    function ownerOf(uint256 tokenId) public view tokenExists(tokenId) returns (address) {
        return _owners[tokenId];
    }

    function balanceOf(address _owner) public view returns (uint256) {
        require(_owner != address(0), "Zero address has no balance");
        return _balances[_owner];
    }
}
"""

# Từ vựng song ngữ
LANG = {
    'vi': {
        'title': 'QUẢN LÝ NFT - RISE TESTNET',
        'info': 'Thông tin',
        'found': 'Tìm thấy',
        'wallets': 'ví',
        'processing_wallet': 'XỬ LÝ VÍ',
        'select_option': 'CHỌN HÀNH ĐỘNG',
        'option_deploy': '1. Tạo bộ sưu tập NFT (Deploy)',
        'option_mint': '2. Đúc NFT (Mint)',
        'option_burn': '3. Đốt NFT (Burn)',
        'choice_prompt': 'Nhập lựa chọn (1, 2 hoặc 3): ',
        'invalid_choice': 'Lựa chọn không hợp lệ',
        'enter_name': 'Nhập tên bộ sưu tập NFT (VD: Thog NFT): ',
        'enter_symbol': 'Nhập ký hiệu bộ sưu tập (VD: THOG): ',
        'enter_max_supply': 'Nhập tổng cung tối đa (VD: 999): ',
        'enter_contract': 'Nhập địa chỉ hợp đồng NFT: ',
        'enter_token_id': 'Nhập Token ID: ',
        'enter_token_uri': 'Nhập Token URI (VD: ipfs://...): ',
        'preparing_tx': 'Chuẩn bị giao dịch...',
        'sending_tx': 'Đang gửi giao dịch...',
        'deploy_success': 'Tạo bộ sưu tập thành công!',
        'mint_success': 'Đúc NFT thành công!',
        'burn_success': 'Đốt NFT thành công!',
        'failure': 'Thất bại',
        'address': 'Địa chỉ hợp đồng',
        'gas': 'Gas',
        'block': 'Khối',
        'error': 'Lỗi',
        'invalid_number': 'Vui lòng nhập số hợp lệ',
        'connect_success': 'Thành công: Đã kết nối mạng Rise Testnet',
        'connect_error': 'Không thể kết nối RPC',
        'web3_error': 'Kết nối Web3 thất bại',
        'pvkey_not_found': 'File pvkey.txt không tồn tại',
        'pvkey_empty': 'Không tìm thấy private key hợp lệ',
        'pvkey_error': 'Đọc pvkey.txt thất bại',
        'invalid_key': 'không hợp lệ, bỏ qua',
        'warning_line': 'Cảnh báo: Dòng',
        'completed': 'HOÀN THÀNH: {successful}/{total} GIAO DỊCH THÀNH CÔNG',
        'installing_solc': 'Đang cài đặt solc phiên bản {version}...',
        'solc_installed': 'Đã cài đặt solc phiên bản {version}',
        'no_balance': 'Số dư ví không đủ (cần ít nhất {required} ETH)',
        'estimating_gas': 'Đang ước lượng gas...'
    },
    'en': {
        'title': 'NFT MANAGEMENT - RISE TESTNET',
        'info': 'Info',
        'found': 'Found',
        'wallets': 'wallets',
        'processing_wallet': 'PROCESSING WALLET',
        'select_option': 'SELECT ACTION',
        'option_deploy': '1. Create NFT Collection (Deploy)',
        'option_mint': '2. Mint NFT',
        'option_burn': '3. Burn NFT',
        'choice_prompt': 'Enter choice (1, 2, or 3): ',
        'invalid_choice': 'Invalid choice',
        'enter_name': 'Enter NFT collection name (e.g., Thog NFT): ',
        'enter_symbol': 'Enter collection symbol (e.g., THOG): ',
        'enter_max_supply': 'Enter maximum supply (e.g., 999): ',
        'enter_contract': 'Enter NFT contract address: ',
        'enter_token_id': 'Enter Token ID: ',
        'enter_token_uri': 'Enter Token URI (e.g., ipfs://...): ',
        'preparing_tx': 'Preparing transaction...',
        'sending_tx': 'Sending transaction...',
        'deploy_success': 'NFT collection created successfully!',
        'mint_success': 'NFT minted successfully!',
        'burn_success': 'NFT burned successfully!',
        'failure': 'Failed',
        'address': 'Contract address',
        'gas': 'Gas',
        'block': 'Block',
        'error': 'Error',
        'invalid_number': 'Please enter a valid number',
        'connect_success': 'Success: Connected to Rise Testnet',
        'connect_error': 'Failed to connect to RPC',
        'web3_error': 'Web3 connection failed',
        'pvkey_not_found': 'pvkey.txt file not found',
        'pvkey_empty': 'No valid private keys found',
        'pvkey_error': 'Failed to read pvkey.txt',
        'invalid_key': 'is invalid, skipped',
        'warning_line': 'Warning: Line',
        'completed': 'COMPLETED: {successful}/{total} TRANSACTIONS SUCCESSFUL',
        'installing_solc': 'Installing solc version {version}...',
        'solc_installed': 'Installed solc version {version}',
        'no_balance': 'Insufficient balance (need at least {required} ETH)',
        'estimating_gas': 'Estimating gas...'
    }
}

# Hàm hiển thị viền đẹp mắt
def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."
    padded_text = f" {text} ".center(width - 2)
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│{padded_text}│{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

# Hàm hiển thị phân cách
def print_separator(color=Fore.MAGENTA):
    print(f"{color}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")

# Hàm kiểm tra private key hợp lệ
def is_valid_private_key(key: str) -> bool:
    key = key.strip()
    if not key.startswith('0x'):
        key = '0x' + key
    try:
        bytes.fromhex(key.replace('0x', ''))
        return len(key) == 66
    except ValueError:
        return False

# Hàm đọc private keys từ file pvkey.txt
def load_private_keys(file_path: str = "pvkey.txt", language: str = 'en') -> list:
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.RED}  ✖ {LANG[language]['pvkey_not_found']}{Style.RESET_ALL}")
            with open(file_path, 'w') as f:
                f.write("# Thêm private keys vào đây, mỗi key trên một dòng\n# Ví dụ: 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef\n")
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

# Hàm kết nối Web3
def connect_web3(language: str = 'en'):
    for url in NETWORK_URLS:
        try:
            w3 = Web3(Web3.HTTPProvider(url))
            if w3.is_connected():
                print(f"{Fore.GREEN}  ✔ {LANG[language]['connect_success']} | Chain ID: {w3.eth.chain_id} | RPC: {url}{Style.RESET_ALL}")
                return w3
            else:
                print(f"{Fore.YELLOW}  ⚠ {LANG[language]['connect_error']} at {url}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}  ⚠ {LANG[language]['web3_error']} at {url}: {str(e)}{Style.RESET_ALL}")
    
    print(f"{Fore.RED}  ✖ Failed to connect to any default RPC endpoint{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}  ℹ {'Vui lòng lấy RPC từ https://alchemy.com và nhập vào dưới đây' if language == 'vi' else 'Please obtain an RPC from https://alchemy.com and enter it below'}{Style.RESET_ALL}")
    custom_rpc = input(f"{Fore.YELLOW}  > {'Nhập RPC tùy chỉnh' if language == 'vi' else 'Enter custom RPC'}: {Style.RESET_ALL}").strip()

    if not custom_rpc:
        print(f"{Fore.RED}  ✖ {'Không có RPC được nhập, thoát chương trình' if language == 'vi' else 'No RPC provided, exiting program'}{Style.RESET_ALL}")
        sys.exit(1)

    try:
        w3 = Web3(Web3.HTTPProvider(custom_rpc))
        if w3.is_connected():
            print(f"{Fore.GREEN}  ✔ {LANG[language]['connect_success']} | Chain ID: {w3.eth.chain_id} | RPC: {custom_rpc}{Style.RESET_ALL}")
            return w3
        else:
            print(f"{Fore.RED}  ✖ {LANG[language]['connect_error']} at {custom_rpc}{Style.RESET_ALL}")
            sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}  ✖ {LANG[language]['web3_error']} at {custom_rpc}: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

# Hàm kiểm tra và cài đặt solc
def ensure_solc_installed(language: str = 'en'):
    try:
        current_version = get_solc_version()
        if current_version != SOLC_VERSION:
            raise Exception("Phiên bản solc không khớp")
    except Exception:
        print(f"{Fore.YELLOW}  ℹ {LANG[language]['installing_solc'].format(version=SOLC_VERSION)}{Style.RESET_ALL}")
        install_solc(SOLC_VERSION)
        print(f"{Fore.GREEN}  ✔ {LANG[language]['solc_installed'].format(version=SOLC_VERSION)}{Style.RESET_ALL}")

# Hàm biên dịch hợp đồng
def compile_contract(language: str = 'en'):
    ensure_solc_installed(language)
    compiled_sol = compile_source(NFT_CONTRACT_SOURCE, output_values=['abi', 'bin'], solc_version=SOLC_VERSION)
    contract_id, contract_interface = compiled_sol.popitem()
    return contract_interface['abi'], contract_interface['bin']

# Hàm triển khai hợp đồng NFT
async def deploy_nft(w3: Web3, private_key: str, wallet_index: int, name: str, symbol: str, max_supply: int, language: str = 'en'):
    account = Account.from_key(private_key)
    sender_address = account.address

    try:
        abi, bytecode = compile_contract(language)
        contract = w3.eth.contract(abi=abi, bytecode=bytecode)

        print(f"{Fore.CYAN}  > {LANG[language]['preparing_tx']}{Style.RESET_ALL}")
        nonce = w3.eth.get_transaction_count(sender_address)

        print(f"{Fore.CYAN}  > {LANG[language]['estimating_gas']}{Style.RESET_ALL}")
        # Fetch dynamic gas price
        gas_price = int(w3.eth.gas_price * 1.2)
        print(f"{Fore.YELLOW}  - Current gas price: {w3.from_wei(gas_price, 'gwei'):.2f} Gwei{Style.RESET_ALL}")

        tx = contract.constructor(name, symbol, max_supply).build_transaction({
            'from': sender_address,
            'nonce': nonce,
            'chainId': CHAIN_ID,
            'gasPrice': gas_price
        })

        try:
            estimated_gas = contract.constructor(name, symbol, max_supply).estimate_gas({'from': sender_address})
            gas_limit = int(estimated_gas * 1.2)
            tx['gas'] = gas_limit
            print(f"{Fore.YELLOW}  - Gas ước lượng: {estimated_gas} | Gas limit sử dụng: {gas_limit}{Style.RESET_ALL}")
        except Exception as e:
            tx['gas'] = 4000000
            print(f"{Fore.YELLOW}  ⚠ Không thể ước lượng gas: {str(e)}. Dùng gas mặc định: 4000000{Style.RESET_ALL}")

        balance = w3.from_wei(w3.eth.get_balance(sender_address), 'ether')
        required_balance = w3.from_wei(tx['gas'] * tx['gasPrice'], 'ether')
        if balance < required_balance:
            print(f"{Fore.RED}  ✖ {LANG[language]['no_balance'].format(required=required_balance)}{Style.RESET_ALL}")
            return None

        print(f"{Fore.CYAN}  > {LANG[language]['sending_tx']}{Style.RESET_ALL}")
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_link = f"{EXPLORER_URL}/tx/0x{tx_hash.hex()}"

        receipt = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300))

        if receipt.status == 1:
            contract_address = receipt['contractAddress']
            print(f"{Fore.GREEN}  ✔ {LANG[language]['deploy_success']} | Tx: {tx_link}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}    - {LANG[language]['address']}: {contract_address}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}    - {LANG[language]['gas']}: {receipt['gasUsed']}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}    - {LANG[language]['block']}: {receipt['blockNumber']}{Style.RESET_ALL}")
            return {'address': contract_address, 'abi': abi}
        else:
            print(f"{Fore.RED}  ✖ {LANG[language]['failure']} | Tx: {tx_link}{Style.RESET_ALL}")
            return None
    except Exception as e:
        print(f"{Fore.RED}  ✖ {LANG[language]['failure']}: {str(e)}{Style.RESET_ALL}")
        return None

# Hàm đúc NFT
async def mint_nft(w3: Web3, private_key: str, wallet_index: int, contract_address: str, token_id: int, token_uri: str, language: str = 'en'):
    account = Account.from_key(private_key)
    sender_address = account.address

    try:
        contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=compile_contract(language)[0])

        print(f"{Fore.CYAN}  > {LANG[language]['preparing_tx']}{Style.RESET_ALL}")
        nonce = w3.eth.get_transaction_count(sender_address)

        # Fetch dynamic gas price
        gas_price = int(w3.eth.gas_price * 1.2)
        print(f"{Fore.YELLOW}  - Current gas price: {w3.from_wei(gas_price, 'gwei'):.2f} Gwei{Style.RESET_ALL}")

        tx = contract.functions.mint(sender_address, token_id, token_uri).build_transaction({
            'from': sender_address,
            'nonce': nonce,
            'chainId': CHAIN_ID,
            'gasPrice': gas_price
        })

        print(f"{Fore.CYAN}  > {LANG[language]['estimating_gas']}{Style.RESET_ALL}")
        try:
            estimated_gas = contract.functions.mint(sender_address, token_id, token_uri).estimate_gas({'from': sender_address})
            gas_limit = int(estimated_gas * 1.2)
            tx['gas'] = gas_limit
            print(f"{Fore.YELLOW}  - Gas ước lượng: {estimated_gas} | Gas limit sử dụng: {gas_limit}{Style.RESET_ALL}")
        except Exception as e:
            tx['gas'] = 200000
            print(f"{Fore.YELLOW}  ⚠ Không thể ước lượng gas: {str(e)}. Dùng gas mặc định: 200000{Style.RESET_ALL}")

        balance = w3.from_wei(w3.eth.get_balance(sender_address), 'ether')
        required_balance = w3.from_wei(tx['gas'] * tx['gasPrice'], 'ether')
        if balance < required_balance:
            print(f"{Fore.RED}  ✖ {LANG[language]['no_balance'].format(required=required_balance)}{Style.RESET_ALL}")
            return False

        print(f"{Fore.CYAN}  > {LANG[language]['sending_tx']}{Style.RESET_ALL}")
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_link = f"{EXPLORER_URL}/tx/0x{tx_hash.hex()}"

        receipt = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180))

        if receipt.status == 1:
            print(f"{Fore.GREEN}  ✔ {LANG[language]['mint_success']} | Tx: {tx_link}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}    - Token ID: {token_id}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}    - {LANG[language]['gas']}: {receipt['gasUsed']}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}    - {LANG[language]['block']}: {receipt['blockNumber']}{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}  ✖ {LANG[language]['failure']} | Tx: {tx_link}{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}  ✖ {LANG[language]['failure']}: {str(e)}{Style.RESET_ALL}")
        return False

# Hàm đốt NFT
async def burn_nft(w3: Web3, private_key: str, wallet_index: int, contract_address: str, token_id: int, language: str = 'en'):
    account = Account.from_key(private_key)
    sender_address = account.address

    try:
        contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=compile_contract(language)[0])

        print(f"{Fore.CYAN}  > {LANG[language]['preparing_tx']}{Style.RESET_ALL}")
        nonce = w3.eth.get_transaction_count(sender_address)

        # Fetch dynamic gas price
        gas_price = int(w3.eth.gas_price * 1.2)
        print(f"{Fore.YELLOW}  - Current gas price: {w3.from_wei(gas_price, 'gwei'):.2f} Gwei{Style.RESET_ALL}")

        tx = contract.functions.burn(token_id).build_transaction({
            'from': sender_address,
            'nonce': nonce,
            'chainId': CHAIN_ID,
            'gasPrice': gas_price
        })

        print(f"{Fore.CYAN}  > {LANG[language]['estimating_gas']}{Style.RESET_ALL}")
        try:
            estimated_gas = contract.functions.burn(token_id).estimate_gas({'from': sender_address})
            gas_limit = int(estimated_gas * 1.2)
            tx['gas'] = gas_limit
            print(f"{Fore.YELLOW}  - Gas ước lượng: {estimated_gas} | Gas limit sử dụng: {gas_limit}{Style.RESET_ALL}")
        except Exception as e:
            tx['gas'] = 200000
            print(f"{Fore.YELLOW}  ⚠ Không thể ước lượng gas: {str(e)}. Dùng gas mặc định: 200000{Style.RESET_ALL}")

        balance = w3.from_wei(w3.eth.get_balance(sender_address), 'ether')
        required_balance = w3.from_wei(tx['gas'] * tx['gasPrice'], 'ether')
        if balance < required_balance:
            print(f"{Fore.RED}  ✖ {LANG[language]['no_balance'].format(required=required_balance)}{Style.RESET_ALL}")
            return False

        print(f"{Fore.CYAN}  > {LANG[language]['sending_tx']}{Style.RESET_ALL}")
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_link = f"{EXPLORER_URL}/tx/0x{tx_hash.hex()}"

        receipt = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180))

        if receipt.status == 1:
            print(f"{Fore.GREEN}  ✔ {LANG[language]['burn_success']} | Tx: {tx_link}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}    - Token ID: {token_id}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}    - {LANG[language]['gas']}: {receipt['gasUsed']}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}    - {LANG[language]['block']}: {receipt['blockNumber']}{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}  ✖ {LANG[language]['failure']} | Tx: {tx_link}{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}  ✖ {LANG[language]['failure']}: {str(e)}{Style.RESET_ALL}")
        return False

# Hàm chính
async def run(language: str = 'en'):
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

    # Chọn hành động
    print_border(LANG[language]['select_option'], Fore.YELLOW)
    print(f"{Fore.GREEN}    ├─ {LANG[language]['option_deploy']}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}    ├─ {LANG[language]['option_mint']}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}    └─ {LANG[language]['option_burn']}{Style.RESET_ALL}")
    choice = input(f"{Fore.YELLOW}  > {LANG[language]['choice_prompt']}{Style.RESET_ALL}").strip()

    successful_ops = 0
    total_ops = len(private_keys)

    if choice == '1':  # Deploy
        name = input(f"{Fore.YELLOW}  > {LANG[language]['enter_name']}{Style.RESET_ALL}").strip()
        symbol = input(f"{Fore.YELLOW}  > {LANG[language]['enter_symbol']}{Style.RESET_ALL}").strip() or "ETH"
        max_supply_input = input(f"{Fore.YELLOW}  > {LANG[language]['enter_max_supply']}{Style.RESET_ALL}").strip()
        try:
            max_supply = int(max_supply_input)
            if max_supply <= 0:
                raise ValueError
        except ValueError:
            print(f"{Fore.RED}  ✖ {LANG[language]['error']}: {LANG[language]['invalid_number']}{Style.RESET_ALL}")
            return

        for i, (profile_num, private_key) in enumerate(private_keys, 1):
            print_border(f"{LANG[language]['processing_wallet']} {profile_num} ({i}/{total_ops})", Fore.MAGENTA)
            result = await deploy_nft(w3, private_key, profile_num, name, symbol, max_supply, language)
            if result:
                successful_ops += 1
                with open('contractNFT.txt', 'a') as f:
                    f.write(f"{result['address']}\n")
            if i < total_ops:
                await asyncio.sleep(10)  # Delay cố định 10 giây
            print_separator()

    elif choice == '2':  # Mint
        contract_address = input(f"{Fore.YELLOW}  > {LANG[language]['enter_contract']}{Style.RESET_ALL}").strip()
        token_id_input = input(f"{Fore.YELLOW}  > {LANG[language]['enter_token_id']}{Style.RESET_ALL}").strip()
        token_uri = input(f"{Fore.YELLOW}  > {LANG[language]['enter_token_uri']}{Style.RESET_ALL}").strip()
        try:
            token_id = int(token_id_input)
            if token_id < 0:
                raise ValueError
        except ValueError:
            print(f"{Fore.RED}  ✖ {LANG[language]['error']}: {LANG[language]['invalid_number']}{Style.RESET_ALL}")
            return

        for i, (profile_num, private_key) in enumerate(private_keys, 1):
            print_border(f"{LANG[language]['processing_wallet']} {profile_num} ({i}/{total_ops})", Fore.MAGENTA)
            if await mint_nft(w3, private_key, profile_num, contract_address, token_id, token_uri, language):
                successful_ops += 1
            if i < total_ops:
                await asyncio.sleep(10)  # Delay cố định 10 giây
            print_separator()

    elif choice == '3':  # Burn
        contract_address = input(f"{Fore.YELLOW}  > {LANG[language]['enter_contract']}{Style.RESET_ALL}").strip()
        token_id_input = input(f"{Fore.YELLOW}  > {LANG[language]['enter_token_id']}{Style.RESET_ALL}").strip()
        try:
            token_id = int(token_id_input)
            if token_id < 0:
                raise ValueError
        except ValueError:
            print(f"{Fore.RED}  ✖ {LANG[language]['error']}: {LANG[language]['invalid_number']}{Style.RESET_ALL}")
            return

        for i, (profile_num, private_key) in enumerate(private_keys, 1):
            print_border(f"{LANG[language]['processing_wallet']} {profile_num} ({i}/{total_ops})", Fore.MAGENTA)
            if await burn_nft(w3, private_key, profile_num, contract_address, token_id, language):
                successful_ops += 1
            if i < total_ops:
                await asyncio.sleep(10)  # Delay cố định 10 giây
            print_separator()

    else:
        print(f"{Fore.RED}  ✖ {LANG[language]['invalid_choice']}{Style.RESET_ALL}")
        return

    print()
    print_border(f"{LANG[language]['completed'].format(successful=successful_ops, total=total_ops)}", Fore.GREEN)
    print()

if __name__ == "__main__":
    asyncio.run(run_nftcollection('vi'))  # Ngôn ngữ mặc định là tiếng Việt
