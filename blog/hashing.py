from passlib.context import CryptContext

class Hash():
    def bcrypt(password: str):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)
