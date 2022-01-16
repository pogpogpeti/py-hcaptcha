import random
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
options = Options()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
self.home_folder = os.path.expanduser('~')
with open(f"{self.home_folder}\\spot-js\\hsw.spot", "r") as f:
    hsw = f.read()

def get_proof(data):
    proof = driver.execute_script(hsw + f"return hsw('{data}');")
    proof += "".join(random.choices("ghijklmnopqrstuvwxyz", k=5))
    return proof
