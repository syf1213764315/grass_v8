#!/usr/bin/env python3

import asyncio
import aiohttp
import time
from colorama import Fore, Style, init

init(autoreset=True)

async def test_proxy(proxy_url, timeout=10):
    """Test if a proxy is working by making a simple request"""
    try:
        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=timeout)) as session:
            async with session.get('https://httpbin.org/ip', proxy=proxy_url) as response:
                if response.status == 200:
                    return True, "Working"
                elif response.status == 407:
                    return False, "407 Proxy Authentication Required"
                else:
                    return False, f"Status {response.status}"
    except Exception as e:
        error_msg = str(e)
        if "407" in error_msg or "Proxy Authentication Required" in error_msg:
            return False, "407 Proxy Authentication Required"
        else:
            return False, f"Error: {error_msg}"

async def clean_proxies(proxy_file="proxy.txt", max_concurrent=50):
    """Clean up bad proxies from the proxy file"""
    print(f"{Fore.YELLOW}🧹 Starting proxy cleanup...{Style.RESET_ALL}")
    
    # Read all proxies
    try:
        with open(proxy_file, 'r') as f:
            proxies = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}✖ Proxy file {proxy_file} not found{Style.RESET_ALL}")
        return
    
    print(f"{Fore.CYAN}📊 Testing {len(proxies)} proxies...{Style.RESET_ALL}")
    
    # Test proxies in batches
    working_proxies = []
    bad_proxies = []
    
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def test_with_semaphore(proxy):
        async with semaphore:
            return await test_proxy(proxy)
    
    # Process proxies in batches
    batch_size = 100
    for i in range(0, len(proxies), batch_size):
        batch = proxies[i:i+batch_size]
        print(f"{Fore.BLUE}🔄 Testing batch {i//batch_size + 1}/{(len(proxies)-1)//batch_size + 1}...{Style.RESET_ALL}")
        
        tasks = [test_with_semaphore(proxy) for proxy in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for proxy, result in zip(batch, results):
            if isinstance(result, Exception):
                bad_proxies.append((proxy, str(result)))
            else:
                is_working, message = result
                if is_working:
                    working_proxies.append(proxy)
                    print(f"{Fore.GREEN}✅ {proxy}: {message}{Style.RESET_ALL}")
                else:
                    bad_proxies.append((proxy, message))
                    if "407" in message:
                        print(f"{Fore.RED}❌ {proxy}: {message}{Style.RESET_ALL}")
    
    # Save working proxies
    if working_proxies:
        backup_file = f"{proxy_file}.backup.{int(time.time())}"
        with open(backup_file, 'w') as f:
            f.write('\n'.join(proxies))
        print(f"{Fore.YELLOW}💾 Original proxy file backed up to {backup_file}{Style.RESET_ALL}")
        
        with open(proxy_file, 'w') as f:
            f.write('\n'.join(working_proxies))
        
        print(f"{Fore.GREEN}✅ Cleaned proxy file saved: {len(working_proxies)} working proxies{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ No working proxies found!{Style.RESET_ALL}")
    
    # Show summary
    print(f"\n{Fore.CYAN}📊 Summary:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✅ Working proxies: {len(working_proxies)}{Style.RESET_ALL}")
    print(f"{Fore.RED}❌ Bad proxies: {len(bad_proxies)}{Style.RESET_ALL}")
    
    # Show 407 errors specifically
    auth_errors = [proxy for proxy, msg in bad_proxies if "407" in msg]
    if auth_errors:
        print(f"{Fore.RED}🔐 Proxies with 407 Authentication errors: {len(auth_errors)}{Style.RESET_ALL}")
        for proxy in auth_errors[:5]:  # Show first 5
            print(f"  {Fore.RED}• {proxy}{Style.RESET_ALL}")
        if len(auth_errors) > 5:
            print(f"  {Fore.RED}... and {len(auth_errors) - 5} more{Style.RESET_ALL}")

def remove_auth_proxies(proxy_file="proxy.txt"):
    """Remove proxies with authentication credentials from the file"""
    print(f"{Fore.YELLOW}🔧 Removing proxies with authentication credentials...{Style.RESET_ALL}")
    
    try:
        with open(proxy_file, 'r') as f:
            proxies = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}✖ Proxy file {proxy_file} not found{Style.RESET_ALL}")
        return
    
    # Filter out proxies with authentication
    clean_proxies = []
    auth_proxies = []
    
    for proxy in proxies:
        if '@' in proxy and ':' in proxy.split('@')[0]:
            # This looks like it has authentication (username:password@host:port)
            auth_proxies.append(proxy)
        else:
            clean_proxies.append(proxy)
    
    if auth_proxies:
        # Backup original file
        backup_file = f"{proxy_file}.backup.{int(time.time())}"
        with open(backup_file, 'w') as f:
            f.write('\n'.join(proxies))
        print(f"{Fore.YELLOW}💾 Original proxy file backed up to {backup_file}{Style.RESET_ALL}")
        
        # Save clean proxies
        with open(proxy_file, 'w') as f:
            f.write('\n'.join(clean_proxies))
        
        print(f"{Fore.GREEN}✅ Removed {len(auth_proxies)} proxies with authentication{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✅ Kept {len(clean_proxies)} clean proxies{Style.RESET_ALL}")
    else:
        print(f"{Fore.GREEN}✅ No proxies with authentication found{Style.RESET_ALL}")

async def main():
    print(f"{Fore.CYAN}🛠️ Proxy Cleaner Tool{Style.RESET_ALL}")
    print(f"{Fore.CYAN}════════════════════{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}1. Remove proxies with authentication credentials{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}2. Test all proxies and remove bad ones{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}3. Exit{Style.RESET_ALL}")
    
    choice = input(f"{Fore.CYAN}Select option (1-3): {Style.RESET_ALL}").strip()
    
    if choice == '1':
        remove_auth_proxies()
    elif choice == '2':
        await clean_proxies()
    elif choice == '3':
        print(f"{Fore.GREEN}👋 Goodbye!{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}❌ Invalid choice{Style.RESET_ALL}")

if __name__ == '__main__':
    asyncio.run(main())