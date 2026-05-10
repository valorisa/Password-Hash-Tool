import hashlib
import os
import time


class ScryptHasher:
    def __init__(self, n: int = 16384, r: int = 8, p: int = 1, dklen: int = 64):
        self.n = n
        self.r = r
        self.p = p
        self.dklen = dklen

    def hash(self, password: str) -> dict:
        salt = os.urandom(16)
        start = time.perf_counter()
        dk = hashlib.scrypt(
            password.encode(), salt=salt, n=self.n, r=self.r, p=self.p, dklen=self.dklen
        )
        elapsed = (time.perf_counter() - start) * 1000
        hash_str = f"$scrypt$n={self.n}$r={self.r}$p={self.p}${salt.hex()}${dk.hex()}"
        return {
            "algorithm": "scrypt",
            "hash": hash_str,
            "time_ms": round(elapsed, 2),
        }

    def verify(self, password: str, hash_str: str) -> dict:
        parts = hash_str.split("$")
        n = int(parts[2].split("=")[1])
        r = int(parts[3].split("=")[1])
        p = int(parts[4].split("=")[1])
        salt = bytes.fromhex(parts[5])
        expected_dk = parts[6]

        start = time.perf_counter()
        dk = hashlib.scrypt(
            password.encode(), salt=salt, n=n, r=r, p=p, dklen=len(bytes.fromhex(expected_dk))
        )
        elapsed = (time.perf_counter() - start) * 1000
        valid = dk.hex() == expected_dk
        return {
            "valid": valid,
            "time_ms": round(elapsed, 2),
        }
