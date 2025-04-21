import hashlib


def stable_hash(u: int) -> int:
    return int(hashlib.md5(str(u).encode()).hexdigest(), 16)

