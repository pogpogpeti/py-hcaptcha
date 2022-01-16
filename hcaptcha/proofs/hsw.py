import random
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
options = Options()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)


def get_proof(data, hsw):
    proof = driver.execute_script(hsw + f"return hsw('{req}');")
    proof += "".join(random.choices("ghijklmnopqrstuvwxyz", k=5))
    return proof
