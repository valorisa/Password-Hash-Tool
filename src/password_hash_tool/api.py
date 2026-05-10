from fastapi import FastAPI, HTTPException

from password_hash_tool.benchmark import run_benchmark
from password_hash_tool.hashers import HASHERS
from password_hash_tool.models import (
    BenchmarkResult,
    HashRequest,
    HashResponse,
    VerifyRequest,
    VerifyResponse,
)

app = FastAPI(
    title="Password-Hash-Tool API",
    description="Hash, verify, and benchmark passwords using modern algorithms.",
    version="0.1.0",
)


@app.post("/hash", response_model=HashResponse)
def hash_password(request: HashRequest):
    if request.algorithm not in HASHERS:
        raise HTTPException(status_code=400, detail=f"Unknown algorithm: {request.algorithm}")

    hasher = HASHERS[request.algorithm]()
    result = hasher.hash(request.password)
    return result


@app.post("/verify", response_model=VerifyResponse)
def verify_password(request: VerifyRequest):
    detected = None
    if request.hash.startswith("$2b$") or request.hash.startswith("$2a$"):
        detected = "bcrypt"
    elif request.hash.startswith("$argon2"):
        detected = "argon2id"
    elif request.hash.startswith("$scrypt$"):
        detected = "scrypt"

    if detected is None:
        raise HTTPException(status_code=400, detail="Could not detect algorithm from hash format.")

    hasher = HASHERS[detected]()
    result = hasher.verify(request.password, request.hash)
    return result


@app.get("/benchmark", response_model=list[BenchmarkResult])
def benchmark_algorithms(iterations: int = 10):
    results = run_benchmark(iterations=iterations)
    return results


@app.get("/health")
def health():
    return {"status": "ok"}
