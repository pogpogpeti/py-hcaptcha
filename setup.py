import setuptools
import time

with open("requirements.txt") as fp:
    requirements = fp.read().splitlines()

setuptools.setup(
    name="py-hcaptcha",
    author="fetix",
    version=str(time.time()),
    url="https://github.com/pogpogpeti/py-hcaptcha",
    packages=setuptools.find_packages(),
    classifiers=[],
    install_requires=requirements
)
