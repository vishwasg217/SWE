import bcrypt



def hash(password: str):
    salt = bcrypt.gensalt()
    password = password.encode("utf-8")
    return bcrypt.hashpw(password, salt)


