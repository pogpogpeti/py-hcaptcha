# py-hcaptcha
An unofficial wrapper for interacting with hCaptcha challenges.

* Device must be running Windows with Google Chrome installed.
* Some parts of the code need to be changed frequently and therefore may be written in a sloppy way.

# Install
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
The module comes with a built-in solver, utilizing a simple bruteforce method. The solver class accepts a Redis or a dict-like object as the database parameter.
It'll take many attempts to successfully solve a challenge, but this number should decrease as the database grows.

```python
from hcaptcha.solving import Solver
from redis import Redis

solver = Solver(database=Redis(), min_answers=5)
solver.solve(challenge)
```
