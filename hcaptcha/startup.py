from .http_ import HTTPClient
from .utils import is_main_process, parse_jsw
import json
import os

def download_files():
    with HTTPClient() as http:
        resp = http.request(
            method="GET", 
            url="https://hcaptcha.com/checksiteconfig"
                "?host=dashboard.hcaptcha.com"
                "&sitekey=13257c82-e129-4f09-a733-2a7cb3102832"
                "&sc=0&swa=0",
            headers={"User-Agent": "a"})
        base_path = parse_jsw(
            json.loads(resp.read())["c"]["req"]
            )["payload"]["l"].split("hcaptcha.com", 1)[1]
        if not os.path.isdir("hcaptcha-js"):
            os.mkdir("hcaptcha-js")

        for filename in ("hsw.js",):
            resp = http.request(
                method="GET",
                url=f"https://newassets.hcaptcha.com{base_path}/{filename}",
            )
            with open(f"hcaptcha-js/{filename}", "wb") as fp:
                fp.write(resp.read())

if is_main_process():
    download_files()