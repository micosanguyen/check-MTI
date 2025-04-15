#!/usr/bin/env python

import json
import argparse
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #disable ssl warning

parser = argparse.ArgumentParser(description="Read JSON file from given path")
parser.add_argument(
    '--file',
    type=str,
    required=True,
    help='Path to the JSON file'
)

args = parser.parse_args()
file_path = args.file

# parser username + password from json file
with open(file_path, 'r', encoding='utf-8') as file:
    accounts = json.load(file)

def check_domain_bmh(bmh_accounts):

    # URL login SAP Fiori
    url = "https://bmh.mbageas.life/sap/bc/ui5_ui5/ui2/ushell/shells/abap/FioriLaunchpad.html"

    # get token from response
    def extract_xsrf_token_from_html(html):
        soup = BeautifulSoup(html, 'html.parser')
        input_tag = soup.find('input', attrs={'name': 'sap-login-XSRF'})
        if input_tag:
            return input_tag.get('value')
        return None

    for acc in bmh_accounts:
        domains = ["bmh.mbageas.life", "bangminhhoa.mbageas.life", "daotao.mbageas.life", "training.mbageas.life"]
        if any(domain in acc.get("x_opencti_description", "") for domain in domains):
        # if "bmh.mbageas.life" in acc.get("x_opencti_description", "") or "bangminhhoa.mbageas.life" in acc.get("x_opencti_description", ""):
            username = acc.get("account_login")
            password = acc.get("credential")
            print("\nLogin URL: " + url)
            print(f"Account: {username} / {password}")

            try:
                # GET request retrieve token & cookie
                session = requests.Session()
                get_response = session.get(url, timeout=10, verify=False)
                xsrf_token = extract_xsrf_token_from_html(get_response.text)

                if not xsrf_token:
                    print("token sap-login-XSRF not found.")
                    continue
                else:
                    print(f"XSRF Token: {xsrf_token}")

                # Data payload
                payload = {
                    "sap-system-login-oninputprocessing": "onLogin",
                    "sap-urlscheme": "",
                    "sap-system-login": "onLogin",
                    "sap-system-login-basic_auth": "",
                    "sap-client": "100",
                    "sap-accessibility": "",
                    "sap-login-XSRF": xsrf_token,
                    "sap-system-login-cookie_disabled": "",
                    "sap-hash": "",
                    "sap-language": "EN",
                    "sap-user": username,
                    "sap-password": password,
                }

                # POST request
                headers = {
                    "Origin": "https://bmh.mbageas.life",
                    "User-Agent": "Mozilla/5.0",
                    "Referer": url,
                    "Content-Type": "application/x-www-form-urlencoded",
                }

                response = session.post(url, headers=headers, data=payload, timeout=10, verify=False)

                # Parse HTML
                soup = BeautifulSoup(response.text, "html.parser")
                error_label = soup.find('label', id='LOGIN_LBL_ERROR')

                if error_label:
                    print("Response:", error_label.text.strip())
                else:
                    print("No response reason, maybe valid")

            except Exception as e:
                print("Error when run:", e)

def check_domain_daily(daily_accounts):
    url = "https://daily.mbageas.life/api/v2/sale_auth/sign_in"

    for acc in daily_accounts:
        domains = ["daily.mbageas.life", "salesportal.mbageas.life"]
        if any(domain in acc.get("x_opencti_description", "") for domain in domains):
        # if "bmh.mbageas.life" in acc.get("x_opencti_description", "") or "bangminhhoa.mbageas.life" in acc.get("x_opencti_description", ""):
            username = acc.get("account_login")
            password = acc.get("credential")
            print("\nLogin URL: " + url)
            print(f"Account: {username} / {password}")

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*, application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36",
                "Authorization": "Bearer null",
                "Origin": "https://daily.mbageas.life",
                "Referer": "https://daily.mbageas.life/login",
                "Locale": "vi",
            }

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
                    print(f"Status Code: {response.status_code}")
                    message = res_json.get('message')
                    if message in [None, "None"]:
                        print("No response reason, maybe valid")
                    else:
                        print(f"Message: {message}")

                except ValueError:
                    print(f"Response không phải JSON: {response.text}")

def check_domain_banca(banca_accounts):
    url = "https://banca.mbageas.life/api/v2/sale_auth/sign_in"

    for acc in banca_accounts:
        domains = ["banca.mbageas.life", "salesportal.mbageas.life"]
        if any(domain in acc.get("x_opencti_description", "") for domain in domains):
        # if "bmh.mbageas.life" in acc.get("x_opencti_description", "") or "bangminhhoa.mbageas.life" in acc.get("x_opencti_description", ""):
            username = acc.get("account_login")
            password = acc.get("credential")
            print("\nLogin URL: " + url)
            print(f"Account: {username} / {password}")

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*, application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36",
                "Authorization": "Bearer null",
                "Origin": "https://banca.mbageas.life",
                "Referer": "https://banca.mbageas.life/login",
                "Locale": "vi",
            }

            cookies = {
                "_ga": "GA1.1.1001361431.1721637924",
                "_ga_831TQYMZWZ": "GS1.2.1739176857.1.0.1739176857.0.0.0",
                "_ga_32YZD3NTBS": "GS1.1.1739182624.2.0.1739182624.0.0.0",
                "_ga_XVM0FBBF44": "GS1.1.1744702994.8.1.1744703055.0.0.0"
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
                    print(f"Status Code: {response.status_code}")
                    message = res_json.get('message')
                    if message in [None, "None"]:
                        print("No response reason, maybe valid")
                    else:
                        print(f"Message: {message}")

                    # print(f"Message: {res_json.get('message', 'No message in response')}")

                except ValueError:
                    print(f"Response không phải JSON: {response.text}")

def check_domain_kh(kh_accounts):
    url = "https://apikhachhang.mbageas.life/v1/auth/login"

    for acc in kh_accounts:
        domains = ["kh.mbageas.life", "khachhang.mbageas.life"]
        if any(domain in acc.get("x_opencti_description", "") for domain in domains):
        # if "bmh.mbageas.life" in acc.get("x_opencti_description", "") or "bangminhhoa.mbageas.life" in acc.get("x_opencti_description", ""):
            username = acc.get("account_login")
            password = acc.get("credential")
            print("\nLogin URL: " + url)
            print(f"Account: {username} / {password}")

            headers = {
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.63 Safari/537.36",
                "Origin": "https://khachhang.mbageas.life",
                "Referer": "https://khachhang.mbageas.life/"
            }


            data = {
                "userName": username,
                "password": password,
                "browser": "Web - chrome"
            }

            with requests.Session() as session:
                session.headers.update(headers)
                response = session.post(url, json=data)

                try:
                    res_json = response.json()
                    msg = res_json.get("data", {}).get("msg", "No response reason, maybe valid")

                    if msg in [None, "None"]:
                        print(("No response reason, maybe valid"))
                    else:
                        print(f"Message: {msg}")
                except Exception as e:
                    print("Can't parse response JSON:")
                    print(response.text)

check_domain_bmh(accounts)
print("==============================================================================================================")
check_domain_daily(accounts)
print("==============================================================================================================")
check_domain_banca(accounts)
print("==============================================================================================================")
check_domain_kh(accounts)
print("==============================================================================================================")