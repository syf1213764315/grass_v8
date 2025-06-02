import os
import sys

BOLD = "\033[1m"
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
BLUE = "\033[94m"

BANNER = f"""
{GREEN}{BOLD}
╔═════════════════════════════════════════════════╗
║               🛠️ SCRIPT MENU TOOL                ║
╠═════════════════════════════════════════════════╣
║ {CYAN}1 - Run The Script{GREEN}                              ║
║ {CYAN}2 - Delete Logs (free space){GREEN}                    ║
║ {CYAN}3 - Enter Proxy (manual input){GREEN}                  ║
║ {CYAN}4 - Download Free Proxy List{GREEN}                    ║
║ {CYAN}5 - Exit{GREEN}                                        ║
╚═════════════════════════════════════════════════╝

{YELLOW}🔄 Never Pay Full Price Again!{RESET}
Use {BOLD}FOREST15{RESET} on {BLUE}https://youproxy.io/{RESET} 💸
Get {GREEN}15% OFF{RESET} on all proxy plans — even renewals!
✅ Fast & secure private proxies
✅ Works perfectly on {CYAN}GRASS{RESET}
📺 Review: {YELLOW}https://youtu.be/KxsfcL26Sjw{RESET}
📘 GitHub: {BLUE}https://github.com/itsmesatyavir/Airdrop/blob/main/YOUPROXY.md{RESET}

{GREEN}{BOLD}
╔═════════════════════════════════════════════════╗
║ 🔰 FORESTARMY Community                         ║
║ 🔗 https://t.me/forestarmy                      ║
╚═════════════════════════════════════════════════╝
{RESET}
"""

def run_script():
    print(f"\n{YELLOW}[🚀] Running main script...{RESET}\n")
    os.system("python3.10 test")

def delete_logs():
    print(f"\n{YELLOW}[🧹] Deleting logs...{RESET}\n")
    os.system("python log")

def enter_proxy():
    print(f"\n{CYAN}[✍️] Enter proxy manually (one per line). Type 'done' to finish.{RESET}\n")
    proxies = []
    while True:
        proxy = input("Proxy: ").strip()
        if proxy.lower() == 'done':
            break
        if proxy:
            proxies.append(proxy)
    with open("proxy.txt", "w") as f:
        f.write("\n".join(proxies))
    print(f"\n{GREEN}[✅] Saved {len(proxies)} proxies to proxy.txt{RESET}")

def download_free_proxy():
    print(f"\n{CYAN}[🌐] Downloading free proxy list...{RESET}\n")
    os.system("curl -s https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt -o proxy.txt")
    print(f"{GREEN}[✅] Proxy list downloaded to proxy.txt{RESET}")

def main():
    while True:
        print(BANNER)
        choice = input(f"{BOLD}Select an option (1-5): {RESET}").strip()
        if choice == '1':
            run_script()
        elif choice == '2':
            delete_logs()
        elif choice == '3':
            enter_proxy()
        elif choice == '4':
            download_free_proxy()
        elif choice == '5':
            print(f"\n{YELLOW}[👋] Exiting. Have a great day!{RESET}\n")
            sys.exit()
        else:
            print(f"{RED}[❌] Invalid choice. Please select 1-5.{RESET}\n")

if __name__ == "__main__":
    main()
