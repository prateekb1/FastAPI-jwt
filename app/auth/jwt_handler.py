# This file is responsible for signing, encoding, decoding and returning JWT
import time # Setting an expiration limit for the tokens
import jwt
from decouple import config 
# Helps to organise settings so i dont have to change parameters without having to redeploy you application 
# Also easy to store you parameters in an ini or .env files 

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# Function returns the generated Tokens (JWTs)
def token_response(token: str):
    return {
        "access token" : token
    }


def signJWT(userID : str):
    payload = {
        "userID" : userID,
        "expiry" : time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token:str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {
            
        }
