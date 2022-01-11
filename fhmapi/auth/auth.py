import os
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

from werkzeug.datastructures import Authorization

from dotenv import load_dotenv

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = os.getenv('ALGORITHMS')
API_AUDIENCE = os.getenv('API_AUDIENCE')

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code':'No authorization header found',
            'description':'Not Jwt in request'}, 401)

    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')

    if len(header_parts) != 2:
        raise AuthError({
            'code':'Invalid_header',
            'description':'Authorization malformed'}, 401)
    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code':'Invalid_header',
            'description':'Authorization malformed'},401)
    
    payload_part = header_parts[1]
    return payload_part

# 
def check_permissions(permission, payload):
    if not 'permissions' in payload:
        raise AuthError({
            'code':'invalid_claims',
            'description':'Permission not included in JWT.'
        }, 403)
    
    if permission not in payload['permissions']:
        raise AuthError({
            'code':'Unauthorized',
            'description':'Permission not found'
        }, 403)
    
    return True

def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)

    #CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code':'Invalid_header',
            'description':'Authorization malformed'
        }, 401)
    
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty':key['kty'],
                'kid':key['kid'],
                'use':key['use'],
                'n':key['n'],
                'e':key['e']
            }
    
    if rsa_key:
        try:
            #USE THE KEY TO VALIDATE DE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms= ALGORITHMS,
                audience = API_AUDIENCE,
                issuer='https://'+AUTH0_DOMAIN+'/'
            )        
            return payload
        
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code':'token_expired',
                'description':'Token expired'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
        
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 403)

# Decorator requires_auth
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator