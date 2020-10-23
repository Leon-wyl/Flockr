import re
import hashlib
import jwt
from database import data_email_search, data_handle, data_upload, data_login, data_logout, \
    data_u_id
from error import InputError
from utility import token_generate

REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
SECRET = "fri09mango01"

def auth_login(email, password):
    '''Given a registered user's email and
    password and generates a valid token
    for the user to remain authenticated'''

    correct_u_id = auth_login_check(email, password)
    token = token_generate(correct_u_id)
    data_login(correct_u_id, token)
    return {
        'u_id': correct_u_id,
        'token': token,
    }

def auth_logout(token):
    '''Given an active token, invalidates the token to
    log the user out'''

    if token != None:
        return data_logout(token)
    # User already logged out
    return {
        'is_success': False
    }

def auth_register(email, password, name_first, name_last):
    '''Check whether the input argument email, password, name_first
    and name_last are valid. If yes, create u_id, token, handle and
    upload the data. Then return u_id and token'''
    auth_register_check(email, password, name_first, name_last)

    # Encode password, create u_id, token, handle and upload the data
    password = auth_password_encode(password)
    u_id = data_u_id()
    token = token_generate(u_id)
    handle = data_handle(name_first, name_last, u_id)
    data_upload(u_id, email, password, name_first, name_last, handle, token)

    return {
        'u_id': u_id,
        'token': token,
    }

def auth_login_check(email, password):
    '''Check whether the email and password are valid. If yes,
    return a dict of u_id and token. If not, raise error'''
    auth_email_check(email)

    # Find out whether the input email is a registered email
    correct_user = data_email_search(email)

    if correct_user is None:
        # If the email has not been registered
        raise InputError(f"Error, email address {email} has not been registered yet")

    password = auth_password_encode(password)
    if correct_user['password'] != password:
        # If the password is not correct
        raise InputError("Password is not correct")

    return correct_user['u_id']

def auth_register_check(email, password, name_first, name_last):
    ''' Check whether the email, password, name_first,
    name_last valid. If one of them not, raise error'''
    auth_email_check(email)

    if data_email_search(email) is not None:
        # Check whether email was registered
        raise InputError(f"Email address {email} is already being used by another user")

    if len(password) in range(0, 6):
        # If the length of password is too short (less than 6)
        raise InputError("Password entered is less than 6 characters long")

    if len(name_first) not in range(1, 51):
        # If the length of name_first is out of range (1 to 50)
        raise InputError("name_first is not between 1 and 50 characters inclusively in length")

    if len(name_last) not in range(1, 51):
        # If the length of name_last is out of range (1 to 50)
        raise InputError("name_last is not between 1 and 50 characters inclusively in length")

def auth_email_check(email):
    '''Test whether the email input is valid. If not, raise exception'''
    if not re.search(REGEX, email):
        raise InputError("Email entered is not a valid email")

def auth_password_encode(password):
    ''' Return the encoded password'''
    return hashlib.sha256(password.encode()).hexdigest()

def auth_u_id_from_token(token):
    '''Input a token, return its corresponding u_id'''
    decoded_jwt = jwt.decode(token.encode(), SECRET, algorithms=['HS256'])
    u_id = int(decoded_jwt['u_id'])
    return u_id
