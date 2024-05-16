from datetime import datetime, timezone, timedelta
from pathlib import Path

import jwt
from cryptography.hazmat.primitives import serialization

now = datetime.now(timezone.utc)

payload = {
    "iss": "https://auth.pyjobs.works",
    "sub": "23456543",
    "aud": "https://pyjobs.works/jobs",
    "iat": now.timestamp(),
    "exp": (now + timedelta(hours=1)).timestamp()
}

signing_key = Path("private_key.pem").read_text()

signing_key_loaded = serialization.load_pem_private_key(
    data=signing_key.encode(), password=None
)

token = jwt.encode(payload=payload, key=signing_key_loaded, algorithm="RS256")

print(token)
