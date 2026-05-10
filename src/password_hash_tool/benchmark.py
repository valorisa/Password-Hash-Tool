import statistics
import time

from password_hash_tool.hashers import HASHERS


def run_benchmark(iterations: int = 10, password: str = "BenchmarkPassword123!") -> list[dict]:
    results = []
    for name, hasher_cls in HASHERS.items():
        hasher = hasher_cls()
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            hasher.hash(password)
            elapsed = (time.perf_counter() - start) * 1000
            times.append(elapsed)
        results.append({
            "algorithm": name,
            "avg_ms": round(statistics.mean(times), 2),
            "min_ms": round(min(times), 2),
            "max_ms": round(max(times), 2),
            "iterations": iterations,
        })
    return results
