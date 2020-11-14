import re
import hashlib
import jwt
import random
from database import data_email_search, data_handle, data_upload, data_login, data_logout, \
    data_u_id, data_reset_code_renew, data_password_renew
from error import InputError
from utility import token_generate, email_check, register_check, login_check, password_encode, \
    check_reset_code, check_valid_password, send_email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
SECRET = "fri09mango01"

def auth_login(email, password):
    '''Given a registered user's email and
    password and generates a valid token
    for the user to remain authenticated'''

    correct_u_id = login_check(email, password)
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
    # User already logged
    return {
        'is_success': False
    }

def auth_register(email, password, name_first, name_last):
    '''Check whether the input argument email, password, name_first
    and name_last are valid. If yes, create u_id, token, handle and
    upload the data. Then return u_id and token'''
    register_check(email, password, name_first, name_last)

    # Encode password, create u_id, token, handle and upload the data
    password = password_encode(password)
    u_id = data_u_id()
    token = token_generate(u_id)
    handle = data_handle(name_first, name_last, u_id)
    data_upload(u_id, email, password, name_first, name_last, handle, token)

    return {
        'u_id': u_id,
        'token': token,
    }

def auth_u_id_from_token(token):
    '''Input a token, return its corresponding u_id'''
    decoded_jwt = jwt.decode(token.encode(), SECRET, algorithms=['HS256'])
    u_id = int(decoded_jwt['u_id'])
    return u_id

def auth_passwordreset_request(email):
    '''Generate a five-digit random number as reset
    code then send a email to the user email'''
    sample_numbers = '1234567890'
    reset_code = ''.join((random.choice(sample_numbers) for i in range(5)))
    user = data_email_search(email)
    data_reset_code_renew(user['u_id'], reset_code)
    send_email(email, reset_code)

    return {}

def auth_passwordreset_reset(reset_code, new_password):
    '''If the reset_code and new_password is valid, reset password'''
    u_id = check_reset_code(reset_code)
    check_valid_password(new_password)
    data_password_renew(u_id, password_encode(new_password))

    return {}

