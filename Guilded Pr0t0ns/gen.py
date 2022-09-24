import ctypes, requests, random, string, threading, colorama, json, os
from os import system, name
from datetime import datetime
from colorama import init, Fore
init()
lock = threading.Lock()
width = os.get_terminal_size().columns
with open("data/config.json") as conf:
    data = json.load(conf)
    show_stats = data['Display_Stats']
    del data

def clear():
    if name == 'nt':
        return system('cls')
    else:
        return system('clear')

class Log:
    @staticmethod
    def success(message):
        now = datetime.now().strftime("%H:%M:%S")
        lock.acquire()
        print(f"[{Fore.LIGHTGREEN_EX}{now}{Fore.RESET}] [+]: {message}")
        return lock.release()

    @staticmethod
    def error(message):
        now = datetime.now().strftime("%H:%M:%S")
        lock.acquire()
        print(f"[{Fore.LIGHTRED_EX}{now}{Fore.RESET}] [-]: {message}")
        return lock.release()

    @staticmethod
    def normal(message):
        now = datetime.now().strftime("%H:%M:%S")
        lock.acquire()
        print(f"[{Fore.LIGHTYELLOW_EX}{now}{Fore.RESET}] [/]: {message}")
        return lock.release()

    @staticmethod
    def caution(message):
        now = datetime.now().strftime("%H:%M:%S")
        lock.acquire()
        print(f"[{Fore.LIGHTBLUE_EX}{now}{Fore.RESET}] [=]: {message}")
        return lock.release()

class Guildedgg:
    def __init__(self) -> None:
        self.created_accounts = 0; self.errors = 0; self.banned_proxies = 0
        self.proxies = []
        self.bios = []
        self.server_names = ["Lounge", "Palace", "Chatting Center", "Center", "Hangout"]
        self.start_time = datetime.now()
        with open("data/proxies.txt", 'r+') as data:
            data = data.readlines()
            for proxy in data:
                self.proxies.append(proxy)
        with open('data/bios.txt', 'r+') as bioo:
            data = bioo.readlines()
            if data == "":
                pass
            else:
                for bio in data:
                    bio = bio.replace("\n", "")
                    self.bios.append(bio)
        with open("data/config.json") as conf:
            data = json.load(conf)
            self.Log_data = data['Log_all_register_data']
            self.get_usernames = data['get_usernames_from_file']
            self.remove_proxies = data['remove_banned_proxies']
            self.use_watermark = data['add_username_watermark']
            self.use_t_lock = data['use_threading_lock']
            self.show_errors = data['display_errors']
            self.use_refferal = data['use_refferal_code']
            self.email_code = data['verify_email']
            self.setup_acct = data['setup_account_oncreation']
            self.set_bio = data['set_account_bio']
            del data
        self.headers = {
            'content-type': 'application/json',
            "guilded-client-id": "95977cbe-1ed3-4fe3-84c9-446213195776",
            "guilded-stag": "ac7a68ac3d8230f3185880b74e5ef607",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.42",
            "x-requested-with": "XMLHttpRequest"
        }

    def update_stats(self):
        while True:
            ctypes.windll.kernel32.SetConsoleTitleW(f'[FREE] Pr0t0n x Adylan Guilded.gg Generator | Accounts Created: {self.created_accounts} | Banned Proxies: {self.banned_proxies} | Errors: {self.errors} | Time: {datetime.now() - self.start_time}')

    @staticmethod
    def gen_username():
        return ''.join(random.choice(string.ascii_letters) for x in range(random.randint(8, 12)))

    @staticmethod
    def gen_email():
        return ''.join(random.choice(string.ascii_letters) for x in range(random.randint(8, 14))) + random.choice(["@hcaptchasolver.online", "@satan-is.art"])

    @staticmethod
    def gen_pass():
        return ''.join(random.choice(string.ascii_letters) for x in range(random.randint(10, 14))) + random.choice(['!', "?", "@", "%"])

    def send_email(self, mid, ipah, hmac, gk, email, proxy):
        url = 'https://www.guilded.gg/api/email/verify'
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "cookie": f'guilded_mid={mid}; guilded_ipah={ipah}; hmac_signed_session={hmac}; authenticated=true; gk={gk}',
            "guilded-client-id": "65b66632-5f71-4cd3-8e4e-8c309974dd3a",
            "guilded-viewer-platform": "desktop",
            "origin": "https://www.guilded.gg",
            "referer": "https://www.guilded.gg/teams/dlOKrxVl",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        data = requests.post(url, headers=headers, proxies=proxies)
        Log.success("Sent Verification Code!")
        return self.register_account()
    def register_account(self, next=None):
        proxy = random.choice(self.proxies)
        proxy = proxy.replace("\n", "")
        proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        email = self.gen_email()
        password = self.gen_pass()
        if self.get_usernames == False:
            usern = self.gen_username()
        else:
            try:
                f = open('data/username.txt', 'r+')
                userns = f.readlines()
                usernamess = []
                for username in userns:
                    usernamess.append(username)
                usern = random.choice(usernamess)
            except Exception:
                lock.acquire()
                input("No Usernames found in data/username.txt! Click enter to continue")
                lock.release()
                exit(0)
        usern = usern.replace("\n", "")
        email = f"{usern[:random.randint(2, 10)]}{random.randint(1, 10000)}@hcaptchasolver.online"
        if self.use_watermark != "":
            usern = f"{self.use_watermark} | {usern}"
        if len(usern) >= 25:
            usern = self.gen_username()
        payload = {"extraInfo":{"platform":"desktop"},"name": usern,"email": email,"password": password,"fullName": self.gen_username()}
        try:
            if self.use_refferal == "":
                data = requests.post('https://www.guilded.gg/api/users?type=email', headers=self.headers, json=payload, proxies=proxies)
            else:
                data = requests.post('https://www.guilded.gg/api/users?type=email', headers=self.headers, json={"extraInfo":{"platform":"desktop", "referrerId": self.use_refferal},"name": usern,"email": email,"password": password,"fullName": self.gen_username()}, proxies=proxies)
        except requests.exceptions.ProxyError:
            if self.show_errors == True:
                Log.error(f"Proxy Error ({proxy})!")
            self.errors += 1
            return self.register_account()
        except requests.exceptions.SSLError:
            if self.show_errors == True:
                Log.error(f"SSL Error ({proxy})!")
            self.errors += 1
            return self.register_account()
        except Exception:
            if self.show_errors == True:
                Log.error("Unknown Requests Error!")
            self.errors += 1
            return self.register_account()
        if "You have been banned" in data.text:
            if self.remove_proxies == True:
                if self.show_errors == True:
                    Log.error(f'Proxy Banned from Guilded removing from list ({proxy})!')
                self.proxies.remove(proxy)
            else:
                if self.show_errors == True:
                    Log.error(f"Proxy Banned from Guilded ({proxy})!")
            self.banned_proxies += 1
            return self.register_account()
        elif "TooManyRequestsError" in data.text:
            if self.remove_proxies == True:
                if self.show_errors == True:
                    Log.caution(f'Proxy Ratelimited from Guilded removing from list Proxy Error ({proxy})!')
                self.proxies.remove(proxy)
            else:
                if self.show_errors == True:
                    Log.caution(f"Proxy Ratelimited from Guilded ({proxy})!")
            self.banned_proxies += 1
            return self.register_account()   
        try:
            uid = data.json()['user']['id']
        except KeyError:
            if self.show_errors == True:
                Log.error(f"Unexpected Error Creating Account! ({data.text})")
            self.errors += 1
            return self.register_account()
        except Exception:
            if self.show_errors == True:
                Log.error(f"Error while Decoding Response data!")
            self.errors += 1
            return self.register_account()
        acct_cookies = data.cookies.get_dict()
        hmac = acct_cookies.get('hmac_signed_session')
        gk = acct_cookies.get('gk')
        guilded_mid = acct_cookies.get('guilded_mid')
        guilded_ipah = acct_cookies.get('guilded_ipah')
        usern = usern.replace("\n", "")
        Log.success(f'Created Account ({Fore.LIGHTBLUE_EX}{usern}{Fore.RESET})')
        self.created_accounts += 1
        if self.setup_acct == True:
            url = 'https://www.guilded.gg/api/teams'
            headers = {
                "accept": "application/json, text/javascript, */*; q=0.01",
                "content-type": "application/json",
                "cookie": f"guilded_mid={guilded_mid}; guilded_ipah={guilded_ipah}; hmac_signed_session={hmac}; authenticated=true; gk={gk}",
                "guilded-client-id": "a8c1d21f-c2db-43e2-ba93-712535b343c0",
                "guilded-viewer-platform": "desktop",
                "origin": "https://www.guilded.gg",
                "referer": "https://www.guilded.gg/teams",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                "x-requested-with": "XMLHttpRequest"
            }
            payload = {"extraInfo":{"platform":"desktop"},"userId": uid,"teamName": f"{usern}'s {random.choice(self.server_names)}"}
            try:
                resp = requests.post(url, headers=headers, json=payload, proxies=proxies)
            except Exception:
                if self.show_errors:
                    Log.error(f"Proxy Error ({proxy})!")
                self.errors += 1
                return self.register_account()
            acct_cookies = resp.cookies.get_dict()
            gk = acct_cookies.get('gk')
            try:
                team_id = resp.json()['team']['id']
            except Exception:
                if self.show_errors:
                    Log.error("Error Setting up Server For account!")
                self.errors += 1
                return self.register_account()
            headers = {
                "accept": "application/json, text/javascript, */*; q=0.01",
                "content-type": "application/json",
                "cookie": f"guilded_mid={guilded_mid}; guilded_ipah={guilded_ipah}; hmac_signed_session={hmac}; authenticated=true; gk={gk}",
                "guilded-client-id": "a8c1d21f-c2db-43e2-ba93-712535b343c0",
                "guilded-viewer-platform": "desktop",
                "origin": "https://www.guilded.gg",
                "referer": "https://www.guilded.gg/teams",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                "x-requested-with": "XMLHttpRequest"
            }
            url = f'https://www.guilded.gg/api/teams/{team_id}/games'
            payload = {"gameIds":["220044"],"createGroupsForGames": True}
            try:
                resp2 = requests.post(url, headers=headers, json=payload, proxies=proxies)
            except Exception:
                if self.show_errors:
                    Log.error(f"Proxy Error ({proxy})!")
                self.errors += 1
                return self.register_account()
            if int(resp2.status_code) == 200:
                pass
            else:
                if self.show_errors:
                    Log.error("Error Adding Game To user profile For account!")
                self.errors += 1
                return self.register_account()
            acct_cookies = resp2.cookies.get_dict()
            gk = acct_cookies.get('gk')
            headers = {
                "accept": "application/json, text/javascript, */*; q=0.01",
                "content-type": "application/json",
                "cookie": f"guilded_mid={guilded_mid}; guilded_ipah={guilded_ipah}; hmac_signed_session={hmac}; authenticated=true; gk={gk}",
                "guilded-client-id": "a8c1d21f-c2db-43e2-ba93-712535b343c0",
                "guilded-viewer-platform": "desktop",
                "origin": "https://www.guilded.gg",
                "referer": "https://www.guilded.gg/teams",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                "x-requested-with": "XMLHttpRequest"
            }
            url = f'https://www.guilded.gg/api/teams/{team_id}/invites'
            payload = {"teamId": team_id,"gameId": None}
            try:
                resp3 = requests.post(url, headers=headers, json=payload, proxies=proxies)
            except Exception:
                if self.show_errors:
                    Log.error(f"Proxy Error ({proxy})!")
                self.errors += 1
                return self.register_account()
            try:
                invite_code = resp3.json()['invite']['id']
            except Exception:
                if self.show_errors:
                    Log.error(f"Error Creating Server on Account ({Fore.LIGHTBLUE_EX}{usern}{Fore.RESET})")
                self.errors += 1
                return self.register_account()
            Log.success(f"Configured Server & Settings on Account ({Fore.LIGHTBLUE_EX}{usern}{Fore.RESET})")
        file = open("data/accounts.txt", 'a+')
        acct_cookies = data.cookies.get_dict()
        hmac = acct_cookies.get('hmac_signed_session')
        gk = acct_cookies.get('gk')
        guilded_mid = acct_cookies.get('guilded_mid')
        guilded_ipah = acct_cookies.get('guilded_ipah')

        if self.set_bio:
            bio = random.choice(self.bios)
            payload = {"content":{"object":"value","document":{"object":"document","data":{},"nodes":[{"object":"block","type":"paragraph","data":{},"nodes":[{"object":"text","leaves":[{"object":"leaf","text": bio,"marks":[]}]}]}]}},"customReactionId": random.randint(90001573, 90002573),"expireInMs":0}
            headers = {
                "accept": "application/json, text/javascript, */*; q=0.01",
                "content-type": "application/json",
                "cookie": f"guilded_mid={guilded_mid}; guilded_ipah={guilded_ipah}; hmac_signed_session={hmac}; authenticated=true; gk={gk}",
                "guilded-client-id": "a8c1d21f-c2db-43e2-ba93-712535b343c0",
                "guilded-viewer-platform": "desktop",
                "origin": "https://www.guilded.gg",
                "referer": "https://www.guilded.gg/teams",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                "x-requested-with": "XMLHttpRequest"
            }
            url = 'https://www.guilded.gg/api/users/me/status'
            try:
                data = requests.post(url, headers=headers, json=payload, proxies=proxies)
            except Exception:
                if self.show_errors:
                    Log.error(f"Proxy Error ({proxy})!")
                self.errors += 1
                return self.register_account()
            if data.text == "{}":
                Log.success(f"Added bio to account ({Fore.LIGHTBLUE_EX}{usern}{Fore.RESET})")
                acct_cookies = data.cookies.get_dict()
                hmac = acct_cookies.get('hmac_signed_session')
                gk = acct_cookies.get('gk')
                guilded_mid = acct_cookies.get('guilded_mid')
                guilded_ipah = acct_cookies.get('guilded_ipah')
                pass
            else:
                if self.show_errors:
                    Log.error(f"Error Adding Bio to account ({Fore.LIGHTBLUE_EX}{usern}{Fore.RESET})!")
                self.errors += 1
                return self.register_account()
        if self.email_code:
            self.send_email(guilded_mid, guilded_ipah, hmac, gk, email, proxy)
        if self.Log_data:
            if self.use_t_lock:
                lock.acquire()
                file.write(f"{email}:{password}:{hmac}:{guilded_mid}:{guilded_ipah}\n")
                lock.release()
            else:
                file.write(f"{email}:{password}:{hmac}:{guilded_mid}:{guilded_ipah}\n")
        else:
            if self.use_t_lock:
                lock.acquire()
                file.write(f"{email}:{password}\n")
                lock.release()
            else:
                file.write(f"{email}:{password}\n")
        file.close()
        return self.register_account()

Guildedgg = Guildedgg()

def logo():
    ctypes.windll.kernel32.SetConsoleTitleW(f"Pr0t0n X Adylan Guilded.gg Botter - https://satan-is.art/discord - https://github.com/Pr0t0ns")
    print("  _____       _ _     _          _ ".center(width))
    print(" / ____|     (_) |   | |        | |".center(width))
    print("| |  __ _   _ _| | __| | ___  __| |".center(width))
    print("| | |_ | | | | | |/ _` |/ _ \/ _` |".center(width))
    print("| |__| | |_| | | | (_| |  __/ (_| |".center(width))
    print(" \_____|\__,_|_|_|\__,_|\___|\__,_|.gg".center(width))
    print(" ".center(width))

def main():
    clear()
    logo()
    print(f"({Fore.GREEN}1{Fore.RESET}) Create Accounts")
    print(" ".center(width))
    choice = int(input(f"[{Fore.LIGHTBLUE_EX}?{Fore.RESET}] Choice: "))
    clear()
    logo()
    threads = int(input(f"[{Fore.LIGHTBLUE_EX}?{Fore.RESET}] Threads: "))
    clear()
    if choice == 1:
        for i in range(threads):
            threading.Thread(target=Guildedgg.register_account).start()
        if show_stats == True:
            threading.Thread(target=Guildedgg.update_stats).start()
    else:
        input("Invalid Choice click enter to continute")
        return main()


if __name__ == "__main__":
    main()
