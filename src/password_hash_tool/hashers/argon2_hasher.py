import time

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class Argon2Hasher:
    def __init__(self, time_cost: int = 3, memory_cost: int = 65536, parallelism: int = 4):
        self.ph = PasswordHasher(
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism,
        )

    def hash(self, password: str) -> dict:
        start = time.perf_counter()
        hashed = self.ph.hash(password)
        elapsed = (time.perf_counter() - start) * 1000
        return {
            "algorithm": "argon2id",
            "hash": hashed,
            "time_ms": round(elapsed, 2),
        }

    def verify(self, password: str, hash_str: str) -> dict:
        start = time.perf_counter()
        try:
            valid = self.ph.verify(hash_str, password)
        except VerifyMismatchError:
            valid = False
        elapsed = (time.perf_counter() - start) * 1000
        return {
            "valid": valid,
            "time_ms": round(elapsed, 2),
        }
