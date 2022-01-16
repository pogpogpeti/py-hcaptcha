# py-hcaptcha
Forked h-captcha solver made by @h0nde
Made for a discord token generator, but can be used for everything.

# Install
```bash
pip install -U git+https://github.com/pogpogpeti/py-hcaptcha --upgrade
```
# Requirements
* Must download ChromeDriver according to your Chrome ver. and put it in PATH or in the script folder.
* PyTorch
* Selenium
* numpy

# Usage Example
```bash
def get_captcha():
    while True:
        ch = None
        try:
            ch = hcaptcha.Challenge(
                site_key="f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34",
                site_url="https://discord.com/",
                image_detection=<boolean, True or False>,
                #proxy=<insert proxy here>
            )
            ch.submit()
            if ch.token: 
                ch.close()
                return ch.token
                break

        except: ch = None
        finally: 
            if ch: ch.close()
```
