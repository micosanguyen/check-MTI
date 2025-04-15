#!/usr/bin/env python

import json
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #disable ssl warning

# parser username + password from json file
with open('C:\\Users\\hungnv4\\Desktop\\2025-04-11T04_31_09.499Z_8ae2f605e319dcdf6_ExportFileStix2Stix-Cyber-Observable_simple.json', 'r', encoding='utf-8') as file:
    accounts = json.load(file)

def check_domain_daily(daily_accounts):
    url = "https://daily.mbageas.life/api/v2/sale_auth/sign_in"

    for acc in daily_accounts:
        domains = ["daily.mbageas.life"]
        if any(domain in acc.get("x_opencti_description", "") for domain in domains):
        # if "bmh.mbageas.life" in acc.get("x_opencti_description", "") or "bangminhhoa.mbageas.life" in acc.get("x_opencti_description", ""):
            username = acc.get("account_login")
            password = acc.get("credential")
            print(f"\nAccount: {username} / {password}")

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*, application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36",
                "Authorization": "Bearer null",
                "Origin": "https://daily.mbageas.life",
                "Referer": "https://daily.mbageas.life/login",
                "Locale": "vi",
            }

            # Cookie nếu cần thì thêm ở đây
            cookies = {
                "_ga": "GA1.1.1001361431.1721637924",
                "_ga_831TQYMZWZ": "GS1.2.1739176857.1.0.1739176857.0.0.0",
                "_ga_32YZD3NTBS": "GS1.1.1739182624.2.0.1739182624.0.0.0",
                "_ga_XVM0FBBF44": "GS1.1.1744698749.7.1.1744698756.0.0.0"
            }

            data = {
                "ic_user": username,
                "password": password
            }

            with requests.Session() as session:
                session.headers.update(headers)
                session.cookies.update(cookies)
                response = session.post(url, json=data)

                try:
                    res_json = response.json()
                    print(f"✅ Status Code: {response.status_code}")
                    print(f"📨 Message: {res_json.get('message', 'No message in response')}")
                except ValueError:
                    print(f"⚠️ Response không phải JSON: {response.text}")

# Gọi hàm
check_domain_daily(accounts)
