from . import hsl
from . import hsw

def get_proof(type, data, hsw: str):
    if type == "hsl":
        return hsl.get_proof(data)
    elif type == "hsw":
        return hsw.get_proof(data, hsw)
    raise Exception(f"Unrecognized proof type '{type}'")
