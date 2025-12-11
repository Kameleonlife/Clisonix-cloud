import logging

def get_logger(name: str = "mesh"):
    l = logging.getLogger(name)
    if not l.handlers:
        h = logging.StreamHandler()
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
        h.setFormatter(fmt)
        l.addHandler(h)
    l.setLevel(logging.INFO)
    return l
