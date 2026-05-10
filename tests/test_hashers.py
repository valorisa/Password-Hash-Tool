from password_hash_tool.hashers import HASHERS


def test_bcrypt_hash_and_verify():
    hasher = HASHERS["bcrypt"](cost=4)
    result = hasher.hash("testpassword")
    assert result["algorithm"] == "bcrypt"
    assert result["hash"].startswith("$2b$")
    assert result["time_ms"] > 0

    verify_result = hasher.verify("testpassword", result["hash"])
    assert verify_result["valid"] is True

    verify_result = hasher.verify("wrongpassword", result["hash"])
    assert verify_result["valid"] is False


def test_argon2_hash_and_verify():
    hasher = HASHERS["argon2id"](time_cost=1, memory_cost=16384, parallelism=1)
    result = hasher.hash("testpassword")
    assert result["algorithm"] == "argon2id"
    assert result["hash"].startswith("$argon2id$")
    assert result["time_ms"] > 0

    verify_result = hasher.verify("testpassword", result["hash"])
    assert verify_result["valid"] is True

    verify_result = hasher.verify("wrongpassword", result["hash"])
    assert verify_result["valid"] is False


def test_scrypt_hash_and_verify():
    hasher = HASHERS["scrypt"](n=1024, r=8, p=1)
    result = hasher.hash("testpassword")
    assert result["algorithm"] == "scrypt"
    assert result["hash"].startswith("$scrypt$")
    assert result["time_ms"] > 0

    verify_result = hasher.verify("testpassword", result["hash"])
    assert verify_result["valid"] is True

    verify_result = hasher.verify("wrongpassword", result["hash"])
    assert verify_result["valid"] is False
