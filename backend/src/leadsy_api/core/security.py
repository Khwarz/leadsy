from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_hash(plain_text: str) -> str:
    return password_context.hash(plain_text)
