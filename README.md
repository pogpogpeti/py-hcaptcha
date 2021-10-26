# py-hcaptcha
An unofficial wrapper for interacting with hCaptcha challenges.

# Install
* Device must be have Google Chrome installed.
```bash
pip install git+https://github.com/h0nde/py-hcaptcha
```

# Usage
```python
import hcaptcha

ch = hcaptcha.Challenge(
    site_key="f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34",
    site_url="https://discord.com/",
    #http_proxy="user:pass@127.0.0.1:8888",
    #ssl_context=__import__("ssl")._create_unverified_context(),
    timeout=5
)

print(ch.question["en"])

for tile in ch:
    image = tile.get_image(raw=False)
    image.show()
    if input("answer (y/n): ").lower() == "y":
        ch.answer(tile)

try:
    token = ch.submit()
    print(token)
except hcaptcha.ChallengeError as err:
    print(err)
```

# Solving
The module comes with a built-in solver, utilizing a simple-but-efficient bruteforce method. `Solver` accepts a Redis or a dict-like object as the database parameter.

It may take a lot of attempts to solve a challenge, but this'll become better as the database grows.

```python
import multiprocessing
import threading
import itertools
from hcaptcha.challenges import Challenge
from hcaptcha.solving import Solver
from redis import Redis

WORKER_COUNT = 16
THREAD_COUNT = 50

def worker(proxy_list):
    proxy_iter = itertools.cycle(proxy_list)
    db = Redis()
    solver = Solver(db)

    for _ in range(50):
        threading.Thread(
            target=thread,
            args=(solver, proxy_iter)
        ).start()

def thread(solver, proxy_iter):
    while True:
        ch = None
        try:
            ch = Challenge(
                site_key="f5561ba9-8f1e-40ca-9b5b-a0b3f719ef34",
                site_url="https://discord.com/",
                http_proxy=next(proxy_iter)
            )
            token = solver.solve(ch)
            print(token)

        except Exception as err:
            print(f"{err!r}")
        finally:
            if ch: ch.close()

if __name__ == "__main__":
    with open("proxies.txt") as fp:
        proxies = fp.read().splitlines()
        per = int(len(proxies) / WORKER_COUNT)
    
    for num in range(WORKER_COUNT):
        multiprocessing.Process(
            target=worker,
            args=(proxies[per * num : per * (num + 1)],)
        ).start()
```
