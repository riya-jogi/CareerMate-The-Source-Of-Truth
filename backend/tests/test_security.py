import uuid
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hashing_and_verification():
    plain = "CandidatePass@2026!"
    hashed = hash_password(plain)

    assert hashed != plain
    assert hashed.startswith("$2b$") or hashed.startswith("$2a$")
    assert verify_password(plain, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False


def test_jwt_token_generation_and_decoding():
    user_id = str(uuid.uuid4())
    token = create_access_token(subject=user_id, claims={"role": "candidate"})

    assert isinstance(token, str)
    decoded = decode_access_token(token)

    assert decoded["sub"] == user_id
    assert decoded["role"] == "candidate"
    assert "exp" in decoded
    assert "iat" in decoded
