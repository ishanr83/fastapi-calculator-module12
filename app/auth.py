from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bcrypt has a 72-byte limit, so we truncate if needed
MAX_PASSWORD_LENGTH = 72


def get_password_hash(password: str) -> str:
    # Truncate password to bcrypt's 72-byte limit
    password_bytes = password.encode('utf-8')[:MAX_PASSWORD_LENGTH]
    return pwd_context.hash(password_bytes.decode('utf-8'))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Truncate password to bcrypt's 72-byte limit
    password_bytes = plain_password.encode('utf-8')[:MAX_PASSWORD_LENGTH]
    return pwd_context.verify(password_bytes.decode('utf-8'), hashed_password)
