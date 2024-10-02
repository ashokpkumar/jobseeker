
import jwt
from passlib.hash import pbkdf2_sha256

def jwt_encode(payload)->dict:
    """
    To encode a payload using jwt and secret key
    """
    return jwt.encode(payload, "secretkey", algorithm="HS256")


def jwt_decode(token)->str:
    """
    To decode a JWT encoded token and send back the payload
    """
    return jwt.decode(token, "secretkey", algorithms=["HS256"])

def hash_password(password):
    return pbkdf2_sha256.hash(password)
    

def check_hash_password(password,password_hash):
    return pbkdf2_sha256.verify(password,password_hash)
    