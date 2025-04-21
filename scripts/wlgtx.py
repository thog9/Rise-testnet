import os
import re
import random
import time
import requests
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Border width
BORDER_WIDTH = 80

# API URL
API_URL = "https://gtxdex.xyz/api/subscribe"

# Bilingual vocabulary
LANG = {
    'vi': {
        'title': '🌸 ĐĂNG KÝ WAITLIST GTXDEX 🌸',
        'info': 'Thông tin',
        'found': 'Tìm thấy',
        'emails': 'email',
        'valid': 'hợp lệ',
        'invalid': 'không hợp lệ',
        'processing_email': 'ĐANG XỬ LÝ EMAIL',
        'success': 'Thành công: {email} đã đăng ký!',
        'failure': 'Thất bại: {email} - Mã trạng thái: {code}',
        'error': 'Lỗi khi gửi {email}: {error}',
        'invalid_email': 'Bỏ qua email không hợp lệ: {email}',
        'file_not_found': 'Không tìm thấy file: {file}',
        'no_emails': 'Không có email nào để xử lý',
        'completed': 'HOÀN THÀNH: {successful}/{total} EMAIL ĐĂNG KÝ THÀNH CÔNG'
    },
    'en': {
        'title': '🌸 GTXDEX WAITLIST REGISTRATION 🌸',
        'info': 'Info',
        'found': 'Found',
        'emails': 'emails',
        'valid': 'valid',
        'invalid': 'invalid',
        'processing_email': 'PROCESSING EMAIL',
        'success': 'Success: {email} registered!',
        'failure': 'Failed: {email} - Status code: {code}',
        'error': 'Error sending {email}: {error}',
        'invalid_email': 'Skipped invalid email: {email}',
        'file_not_found': 'File not found: {file}',
        'no_emails': 'No emails to process',
        'completed': 'COMPLETED: {successful}/{total} EMAILS REGISTERED SUCCESSFULLY'
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
def is_valid_email(email: str) -> bool:
    # Regex for basic email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))

def read_emails_from_file(filename: str = "mail.txt", language: str = 'en') -> list:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            emails = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return emails
    except FileNotFoundError:
        print(f"{Fore.RED}  ✖ {LANG[language]['file_not_found'].format(file=filename)}{Style.RESET_ALL}")
        with open(filename, 'w', encoding="utf-8") as f:
            f.write("# Add email addresses here, one per line\n# Example: example@domain.com\n")
        return []
    except Exception as e:
        print(f"{Fore.RED}  ✖ {LANG[language]['error'].format(email=filename, error=str(e))}{Style.RESET_ALL}")
        return []

def join_waitlist(email: str, language: str = 'en') -> bool:
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Origin": "https://gtxdex.xyz",
        "Referer": "https://gtxdex.xyz/waitlist",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }
    data = {"email": email}

    try:
        response = requests.post(API_URL, json=data, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"{Fore.GREEN}  ✔ {LANG[language]['success'].format(email=email)}{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}  ✖ {LANG[language]['failure'].format(email=email, code=response.status_code)}{Style.RESET_ALL}")
            print(f"{Fore.RED}    ↳ {response.text}{Style.RESET_ALL}")
            return False
    except Exception as e:
        print(f"{Fore.RED}  ✖ {LANG[language]['error'].format(email=email, error=str(e))}{Style.RESET_ALL}")
        return False

async def run_wlgtx(language: str = 'en'):
    print()
    print_border(LANG[language]['title'], Fore.CYAN)
    print()

    emails = read_emails_from_file('mail.txt', language)
    if not emails:
        print(f"{Fore.RED}  📭 {LANG[language]['no_emails']}{Style.RESET_ALL}")
        return

    valid_emails = [email for email in emails if is_valid_email(email)]
    invalid_emails = [email for email in emails if not is_valid_email(email)]
    
    print(f"{Fore.YELLOW}  ℹ {LANG[language]['info']}: {LANG[language]['found']} {len(emails)} {LANG[language]['emails']} ({len(valid_emails)} {LANG[language]['valid']}, {len(invalid_emails)} {LANG[language]['invalid']}){Style.RESET_ALL}")
    print()

    if invalid_emails:
        print_border("Invalid Emails", Fore.YELLOW)
        for email in invalid_emails:
            print(f"{Fore.YELLOW}  ⚠ {LANG[language]['invalid_email'].format(email=email)}{Style.RESET_ALL}")
        print_separator()

    if not valid_emails:
        print(f"{Fore.RED}  📭 {LANG[language]['no_emails']}{Style.RESET_ALL}")
        return

    print_border(f"Processing {len(valid_emails)} Valid Emails", Fore.CYAN)
    successful = 0
    for i, email in enumerate(valid_emails, 1):
        print_border(f"{LANG[language]['processing_email']} {i}/{len(valid_emails)}: {email}", Fore.MAGENTA)
        if join_waitlist(email, language):
            successful += 1
        if i < len(valid_emails):
            delay = random.uniform(1.5, 3.0)
            print(f"{Fore.YELLOW}    Pausing {delay:.2f} seconds{Style.RESET_ALL}")
            time.sleep(delay)
        print_separator()

    print()
    print_border(f"{LANG[language]['completed'].format(successful=successful, total=len(valid_emails))}", Fore.GREEN)
    print()

if __name__ == "__main__":
    asyncio.run(run_wlgtx('en'))
