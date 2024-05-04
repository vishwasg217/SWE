import bcrypt

def hash(password: str):
    salt = bcrypt.gensalt()
    password = password.encode("utf-8")
    hash = bcrypt.hashpw(password, salt)
    hash = hash.decode("utf-8")
    return hash

def verify(plain_password: str, hashed_password: str):
    plain_password = plain_password.encode("utf-8")
    hashed_password = hashed_password.encode("utf-8")
    return bcrypt.checkpw(plain_password, hashed_password)


