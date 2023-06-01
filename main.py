import asyncio
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import threading
import concurrent.futures

def get_proxies_from_source(url, scheme_type, user_agent):
    try:
        headers = {"User-Agent": user_agent.random}
        soup = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")
        proxies = []
        for row in soup.find("tbody").find_all("tr"):
            td = row.find_all("td")
            if td:
                ip = td[0].text.strip()
                port = td[1].text.strip()
                proxy = f"{scheme_type}://{ip}:{port}"
                proxies.append(proxy)
        print(f"Collected {len(proxies)} proxies from {url}")
        return proxies
    except Exception as e:
        print(f"Failed to collect proxies from {url} due to: {str(e)}")
        return []

def get_proxies(sources):
    proxies = []
    user_agent = UserAgent()
    NUM_THREADS = int(input("Enter number of threads: "))
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        future_to_url = {executor.submit(get_proxies_from_source, source["url"], source["scheme"], user_agent): source for source in sources}
        for future in concurrent.futures.as_completed(future_to_url):
            proxies.extend(future.result())
    return proxies

async def check_proxy(session, proxy):
    url = 'http://example.com'
    try:
        async with session.get(url, proxy=proxy, timeout=15) as response:
            if response.status == 200:
                with open('http.txt', 'a') as f:
                    f.write(proxy + '\n')
                return proxy
    except:
        return None

async def check_proxies(proxies):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for proxy in proxies:
            task = check_proxy(session, proxy)
            tasks.append(task)
        working_proxies = await asyncio.gather(*tasks)
        return [proxy for proxy in working_proxies if proxy]

def main():
    sources = [
        {"url": "https://sslproxies.org/", "scheme": "https"},
        {"url": "https://free-proxy-list.net/", "scheme": "http"},
        {"url": "https://www.us-proxy.org/", "scheme": "http"},
        {"url": "https://www.socks-proxy.net/", "scheme": "http"},
        {"url": "https://www.proxy-list.download/HTTP", "scheme": "http"},
        {"url": "https://www.proxynova.com/proxy-server-list/", "scheme": "http"},
        {"url": "https://proxydb.net/", "scheme": "http"},
        {"url": "https://www.proxy-list.download/HTTPS", "scheme": "https"},
        {"url": "https://www.proxydocker.com/en/proxylist/search-raw", "scheme": "http"},
        {"url": "https://hidemy.name/en/proxy-list/", "scheme": "http"},
        {"url": "https://www.proxy-list.download/SOCKS5", "scheme": "http"},
        {"url": "https://www.proxynova.com/proxy-server-list/anonymous-proxies/", "scheme": "http"},
        {"url": "https://incloak.com/proxy-list/", "scheme": "http"},
        {"url": "https://proxydb.net/?protocol=http&protocol=https&anonlvl=4&anonlvl=3&country=", "scheme": "http"},
        {"url": "https://free-proxy-list.com/", "scheme": "http"},
        {"url": "https://www.proxynova.com/proxy-server-list/country-us/", "scheme": "http"},
        {"url": "https://free-proxy-list.net/anonymous-proxy.html", "scheme": "http"},
        {"url": "https://proxyservers.pro/proxy/list/anonymous", "scheme": "http"},
        {"url": "https://proxyservers.pro/proxy/list/high-uptime", "scheme": "http"},
        {"url": "https://free-proxy-list.net/uk-proxy.html", "scheme": "http"},
        {"url": "https://www.proxynova.com/proxy-server-list/country-au/", "scheme": "http"},
        {"url": "https://free-proxy-list.net/anonymous-proxy.html", "scheme": "http"},
    ]
    proxies = get_proxies(sources)
    working_proxies = asyncio.run(check_proxies(proxies))
    print(f"Working proxies: {working_proxies}")

if __name__ == '__main__':
    main()