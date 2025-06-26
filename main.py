import os
import sys
import asyncio
from colorama import init, Fore, Style
import inquirer

# Khởi tạo colorama
init(autoreset=True)

# Độ rộng viền cố định
BORDER_WIDTH = 80

# Hàm hiển thị viền đẹp mắt
def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."  # Cắt dài và thêm "..."
    padded_text = f" {text} ".center(width - 2)
    print(f"{color}┌{'─' * (width - 2)}┐{Style.RESET_ALL}")
    print(f"{color}│{padded_text}│{Style.RESET_ALL}")
    print(f"{color}└{'─' * (width - 2)}┘{Style.RESET_ALL}")

# Hàm hiển thị banner
def _banner():
    banner = r"""


██████╗░██╗░██████╗███████╗  ████████╗███████╗░██████╗████████╗███╗░░██╗███████╗████████╗
██╔══██╗██║██╔════╝██╔════╝  ╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝████╗░██║██╔════╝╚══██╔══╝
██████╔╝██║╚█████╗░█████╗░░  ░░░██║░░░█████╗░░╚█████╗░░░░██║░░░██╔██╗██║█████╗░░░░░██║░░░
██╔══██╗██║░╚═══██╗██╔══╝░░  ░░░██║░░░██╔══╝░░░╚═══██╗░░░██║░░░██║╚████║██╔══╝░░░░░██║░░░
██║░░██║██║██████╔╝███████╗  ░░░██║░░░███████╗██████╔╝░░░██║░░░██║░╚███║███████╗░░░██║░░░
╚═╝░░╚═╝╚═╝╚═════╝░╚══════╝  ░░░╚═╝░░░╚══════╝╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝╚══════╝░░░╚═╝░░░


    """
    print(f"{Fore.GREEN}{banner:^80}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
    print_border("RISE TESTNET", Fore.GREEN)
    print(f"{Fore.YELLOW}│ {'Liên hệ / Contact'}: {Fore.CYAN}https://t.me/thog099{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│ {'Replit'}: {Fore.CYAN}Thog{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}│ {'Channel Telegram'}: {Fore.CYAN}https://t.me/thogairdrops{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")

# Hàm xóa màn hình
def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Lựa chọn ngôn ngữ
def select_language():
    while True:
        print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
        print_border("CHỌN NGÔN NGỮ / SELECT LANGUAGE", Fore.YELLOW)
        questions = [
            inquirer.List('language',
                          message=f"{Fore.CYAN}Vui lòng chọn / Please select:{Style.RESET_ALL}",
                          choices=[
                              ("1. Tiếng Việt", 'vi'),
                              ("2. English", 'en')
                          ],
                          carousel=True)
        ]
        answer = inquirer.prompt(questions)
        if answer and answer['language'] in ['vi', 'en']:
            return answer['language']
        print(f"{Fore.RED}❌ {'Lựa chọn không hợp lệ / Invalid choice':^76}{Style.RESET_ALL}")

# Định nghĩa hàm chạy cho từng script
async def run_sendtx(language: str):
    from scripts.sendtx import run_sendtx as sendtx_run
    await sendtx_run(language)

async def run_deploytoken(language: str):
    from scripts.deploytoken import run_deploytoken as deploytoken_run
    await deploytoken_run(language)

async def run_sendtoken(language: str):
    from scripts.sendtoken import run_sendtoken as sendtoken_run
    await sendtoken_run(language)

async def run_nftcollection(language: str):
    from scripts.nftcollection import run_nftcollection as nftcollection_run
    await nftcollection_run(language)

async def run_gaspump(language: str):
    from scripts.gaspump import run_gaspump as gaspump_run
    await gaspump_run(language)

async def run_clober(language: str):
    from scripts.clober import run_clober as clober_run
    await clober_run(language)

async def run_inari(language: str):
    from scripts.inari import run_inari as inari_run
    await inari_run(language)

async def run_wlgtx(language: str):
    from scripts.wlgtx import run_wlgtx as wlgtx_run
    await wlgtx_run(language)

async def run_wlnovadubs(language: str):
    from scripts.wlnovadubs import run_wlnovadubs as wlnovadubs_run
    await wlnovadubs_run(language)

async def run_conftnft(language: str):
    from scripts.conftnft import run_conftnft as conftnft_run
    await conftnft_run(language)

async def run_domain(language: str):
    from scripts.domain import run_domain as domain_run
    await domain_run(language)

    
# Danh sách script với ánh xạ trực tiếp
SCRIPT_MAP = {
    "sendtx": run_sendtx,
    "deploytoken": run_deploytoken,
    "sendtoken": run_sendtoken,
    "nftcollection": run_nftcollection,
    "gaspump": run_gaspump,
    "clober": run_clober,
    "inari": run_inari,
    "wlgtx": run_wlgtx,
    "wlnovadubs": run_wlnovadubs,
    "conftnft": run_conftnft,
    "domain": run_domain,
    "exit": lambda language: sys.exit(0)
}

def get_available_scripts(language):
    scripts = {
        'vi': [
            {"name": "1. Gửi TX ngẫu nhiên hoặc File (address.txt) | Rise Testnet", "value": "sendtx"},
            {"name": "2. Deploy Token smart-contract | Rise Testnet", "value": "deploytoken"},
            {"name": "3. Gửi Token ERC20 ngẫu nhiên hoặc File (addressERC20.txt) | Rise Testnet", "value": "sendtoken"},
            {"name": "4. Deploy NFT - Quản lí NFT [ Tạo | Đúc | Đốt ] | Rise Testnet", "value": "nftcollection"},

            {"name": "5. GasPump Swap | Rise Testnet", "value": "gaspump"},
            {"name": "6. Clober Swap [ ETH ↔ WETH ] | Rise Testnet", "value": "clober"},
            {"name": "7. Inari Finance [ Deposit | Withdraw ] | Rise Testnet", "value": "inari"},
            {"name": "8. WL GTX Dex | Rise Testnet", "value": "wlgtx"},
            {"name": "9. WL Novadubs | Rise Testnet", "value": "wlnovadubs"},
            {"name": "10. Mint ConftApp  Community Member of RISE │ Rise Testnet", "value": "conftnft", "locked": True},
            {"name": "11. Mint Domain │ Rise Testnet", "value": "domain", "locked": True},
            {"name": "12. Thoát", "value": "exit"},
        ],
        'en': [
            {"name": "1. Send Random TX or File (address.txt) | Rise Testnet", "value": "sendtx"},
            {"name": "2. Deploy Token Smart Contract | Rise Testnet", "value": "deploytoken"},
            {"name": "3. Send ERC20 Token Randomly or File (addressERC20.txt) | Rise Testnet", "value": "sendtoken"},
            {"name": "4. Deploy NFT - Manage NFT Collection [ Create | Mint | Burn ] | Rise Testnet", "value": "nftcollection"},

            {"name": "5. GasPump Swap | Rise Testnet", "value": "gaspump"},
            {"name": "6. Clober Swap [ ETH ↔ WETH ] | Rise Testnet", "value": "clober"},
            {"name": "7. Inari Finance [ Deposit | Withdraw ] | Rise Testnet", "value": "inari"},
            {"name": "8. WL GTX Dex | Rise Testnet", "value": "wlgtx"},
            {"name": "9. WL Novadubs | Rise Testnet", "value": "wlnovadubs"},
            {"name": "10. Mint ConftApp  Community Member of RISE │ Rise Testnet", "value": "conftnft", "locked": True},
            {"name": "11. Mint Domain │ Rise Testnet", "value": "domain", "locked": True},
            {"name": "12. Thoát", "value": "exit"},
        ]
    }
    return scripts[language]

def run_script(script_func, language):
    """Chạy script bất kể nó là async hay không."""
    if asyncio.iscoroutinefunction(script_func):
        asyncio.run(script_func(language))
    else:
        script_func(language)

def select_language():
    while True:
        _clear()
        _banner()
        print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
        print_border("CHỌN NGÔN NGỮ / SELECT LANGUAGE", Fore.YELLOW)
        questions = [
            inquirer.List('language',
                          message=f"{Fore.CYAN}Vui lòng chọn / Please select:{Style.RESET_ALL}",
                          choices=[("1. Tiếng Việt", 'vi'), ("2. English", 'en')],
                          carousel=True)
        ]
        answer = inquirer.prompt(questions)
        if answer and answer['language'] in ['vi', 'en']:
            return answer['language']
        print(f"{Fore.RED}❌ {'Lựa chọn không hợp lệ / Invalid choice':^76}{Style.RESET_ALL}")

def main():
    _clear()
    _banner()
    language = select_language()

    messages = {
        "vi": {
            "running": "Đang thực thi: {}",
            "completed": "Đã hoàn thành: {}",
            "error": "Lỗi: {}",
            "press_enter": "Nhấn Enter để tiếp tục...",
            "menu_title": "MENU CHÍNH",
            "select_script": "Chọn script để chạy",
            "locked": "🔒 Script này bị khóa! Vui lòng vào group hoặc Role Discord [ OG - Donate ] để mở khóa."
        },
        "en": {
            "running": "Running: {}",
            "completed": "Completed: {}",
            "error": "Error: {}",
            "press_enter": "Press Enter to continue...",
            "menu_title": "MAIN MENU",
            "select_script": "Select script to run",
            "locked": "🔒 This script is locked! Please join the discord group or role [ OG - Donate ] to unlock."
        }
    }

    while True:
        _clear()
        _banner()
        print(f"{Fore.YELLOW}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
        print_border(messages[language]["menu_title"], Fore.YELLOW)
        print(f"{Fore.CYAN}│ {messages[language]['select_script'].center(BORDER_WIDTH - 4)} │{Style.RESET_ALL}")

        available_scripts = get_available_scripts(language)
        questions = [
            inquirer.List('script',
                          message=f"{Fore.CYAN}{messages[language]['select_script']}{Style.RESET_ALL}",
                          choices=[script["name"] for script in available_scripts],
                          carousel=True)
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            continue

        selected_script_name = answers['script']
        selected_script = next(script for script in available_scripts if script["name"] == selected_script_name)
        selected_script_value = selected_script["value"]

        if selected_script.get("locked"):
            _clear()
            _banner()
            print_border("SCRIPT BỊ KHÓA / LOCKED", Fore.RED)
            print(f"{Fore.YELLOW}{messages[language]['locked']}")
            print('')
            print(f"{Fore.CYAN}→ Telegram: https://t.me/thogairdrops")
            print(f"{Fore.CYAN}→ Donate: https://buymecafe.vercel.app{Style.RESET_ALL}")
            print('')
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")
            continue

        script_func = SCRIPT_MAP.get(selected_script_value)
        if script_func is None:
            print(f"{Fore.RED}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(f"{'Chưa triển khai / Not implemented'}: {selected_script_name}", Fore.RED)
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")
            continue

        try:
            print(f"{Fore.CYAN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(messages[language]["running"].format(selected_script_name), Fore.CYAN)
            run_script(script_func, language)
            print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(messages[language]["completed"].format(selected_script_name), Fore.GREEN)
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")
        except Exception as e:
            print(f"{Fore.RED}{'═' * BORDER_WIDTH}{Style.RESET_ALL}")
            print_border(messages[language]["error"].format(str(e)), Fore.RED)
            print('')
            input(f"{Fore.YELLOW}⏎ {messages[language]['press_enter']}{Style.RESET_ALL:^76}")

if __name__ == "__main__":
    main()
