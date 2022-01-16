from .http_ import HTTPClient
from .agents import random_agent
from .utils import is_main_process, parse_jsw
import json
import os

home_folder = os.path.expanduser('~')

def download_script_files():
    files = ("hsw.spot", )

    with HTTPClient() as http:
        resp = http.request(
            method="GET", 
            url="https://hcaptcha.com/checksiteconfig"
                "?host=dashboard.hcaptcha.com"
                "&sitekey=13257c82-e129-4f09-a733-2a7cb3102832"
                "&sc=0&swa=0",
            headers={
                "User-Agent": random_agent().user_agent
            })

        base_url = "https://newassets.hcaptcha.com"
        base_url += parse_jsw(json.loads(resp.read())["c"]["req"]) \
                    ["payload"]["l"].split("hcaptcha.com", 1)[1]

        if not os.path.isdir(f"{home_folder}\\spot-js"):
            os.mkdir(f"{home_folder}\\spot-js")

        for filename in files:
            resp = http.request(method="GET", url=f"{base_url}/{filename}")
            with open(f"{home_folder}\\spot-js\\{filename}", "wb") as fp:
                fp.write(resp.read())

if is_main_process():
    download_script_files()
