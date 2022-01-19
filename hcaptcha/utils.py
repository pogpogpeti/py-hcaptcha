from .http_ import HTTPClient
import httpx
from base64 import b64decode
import json
import random
import string

def latest_version_id():
    resp = httpx.request("GET", "https://hcaptcha.com/1/api.js").text
    resp_ver = resp.split('https://newassets.hcaptcha.com/captcha/v1/')[1].split('/static')[0]
    return(resp_ver)

def random_widget_id():
    widget_id = "".join(random.choices(
        string.ascii_lowercase + string.digits,
        k=random.randint(10, 12)
    ))
    return widget_id

def parse_jsw(data):
    fields = data.split(".")
    return {
        "header": json.loads(b64decode(fields[0])),
        "payload": json.loads(b64decode(fields[1] + ("=" * ((4 - len(fields[1]) % 4) % 4)))),
        "signature": b64decode(fields[2].replace("_", "/").replace("-", "+")  + ("=" * ((4 - len(fields[1]) % 4) % 4))),
        "raw": {
            "header": fields[0],
            "payload": fields[1],
            "signature": fields[2]
        }
    }

def hostname_from_url(url):
    return url.split("://", 1)[1].split("/", 1)[0].lower()

def is_main_process():
    proc = __import__("multiprocessing").current_process()
    return proc.name == "MainProcess"
