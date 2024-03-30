import jwt

REFRESH_TOKEN = 'refresh_token'
ACCESS_TOKEN = 'access_token'

JWT_ACCESS_TOKEN_EXPIRATION = 15 * 60  # 15 minutes
JWT_REFRESH_TOKEN_EXPIRATION = 7 * 24 * 60 * 60  # 7 days

# for access_token
SECRET_KEY = 'bekk-developers'


# A helper function to verify the auth token
def verify_auth_token(token, verify_signature=True):
    try:
        #  Decode and verify the JWT token
        if not verify_signature:
            #  TO RETURN DATA IN THE TOKEN
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'],
                                 options={"verify_signature": False})

        else:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
