from typing import Literal

from pydantic import BaseModel, Field


class HashRequest(BaseModel):
    password: str = Field(..., min_length=1, description="Password to hash")
    algorithm: Literal["bcrypt", "argon2id", "scrypt"] = Field(
        default="argon2id", description="Hashing algorithm"
    )
    cost: int | None = Field(default=None, description="Cost parameter (algorithm-specific)")


class HashResponse(BaseModel):
    algorithm: str
    hash: str
    time_ms: float


class VerifyRequest(BaseModel):
    password: str = Field(..., min_length=1, description="Password to verify")
    hash: str = Field(..., min_length=1, description="Hash to verify against")


class VerifyResponse(BaseModel):
    valid: bool
    time_ms: float


class BenchmarkResult(BaseModel):
    algorithm: str
    avg_ms: float
    iterations: int
