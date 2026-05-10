import time

import bcrypt


class BcryptHasher:
    def __init__(self, cost: int = 12):
        self.cost = cost

    def hash(self, password: str) -> dict:
        start = time.perf_counter()
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=self.cost))
        elapsed = (time.perf_counter() - start) * 1000
        return {
            "algorithm": "bcrypt",
            "hash": hashed.decode(),
            "time_ms": round(elapsed, 2),
        }

    def verify(self, password: str, hash_str: str) -> dict:
        start = time.perf_counter()
        valid = bcrypt.checkpw(password.encode(), hash_str.encode())
        elapsed = (time.perf_counter() - start) * 1000
        return {
            "valid": valid,
            "time_ms": round(elapsed, 2),
        }
