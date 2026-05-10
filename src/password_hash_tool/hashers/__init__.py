from password_hash_tool.hashers.bcrypt_hasher import BcryptHasher
from password_hash_tool.hashers.argon2_hasher import Argon2Hasher
from password_hash_tool.hashers.scrypt_hasher import ScryptHasher

HASHERS = {
    "bcrypt": BcryptHasher,
    "argon2id": Argon2Hasher,
    "scrypt": ScryptHasher,
}

__all__ = ["BcryptHasher", "Argon2Hasher", "ScryptHasher", "HASHERS"]
