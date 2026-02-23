import hashlib

def make_hash(session_id: str, num: str) -> str:
    return hashlib.sha256((session_id + num).encode()).hexdigest()