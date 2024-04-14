from http import HTTPStatus
import jwt
from db import users as users

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


def missing_token(token, type=ACCESS_TOKEN):
    if not token:
        return {
            {'error': type + ' is missing.'},
            HTTPStatus.UNAUTHORIZED
        }


def unauthorized_access(user_id, access_token):
    token_user_id = verify_auth_token(access_token, False)['user_id']
    if user_id != token_user_id:
        return (
            {'error': 'Unauthorized to view the user\'s tasks'},
            HTTPStatus.UNAUTHORIZED
        )


def valid_tokens(access_token, refresh_token):
    if not verify_auth_token(access_token):
        if not verify_auth_token(refresh_token):
            # USER NEEDS TO RE-LOGIN
            return (
                {'error': 'Invalid tokens.'},
                HTTPStatus.UNAUTHORIZED
            )


def verify(user_id, access_token, refresh_token):
    # CHECK IF THE ACCESS TOKEN IS MISSING
    missing_access_token = missing_token(access_token, ACCESS_TOKEN)
    if missing_access_token:
        return missing_access_token

    # CHECK IF THE REFRESH TOKEN IS MISSING
    missing_refresh_token = missing_token(access_token, REFRESH_TOKEN)
    if missing_refresh_token:
        return missing_refresh_token

    # CHECK IF THE USER_ID AND THE USER_ID FROM TOKEN MATCHES
    res = unauthorized_access(user_id, access_token)
    if res:
        return res

    # CHECK IF THE TOKENS ARE VALID
    res = valid_tokens(access_token, refresh_token)
    if res:
        return res

    # verified user
    return None


def regenerate_access_token(access_token, refresh_token):
    access_token_user_id = verify_auth_token(access_token, False)['user_id']
    refresh_token_user_id = verify_auth_token(refresh_token, False)['user_id']

    if (access_token_user_id == refresh_token_user_id
       and not verify_auth_token(access_token, refresh_token)
       and verify_auth_token(refresh_token)):
        return users.generate_access_token(access_token_user_id)
    return access_token
