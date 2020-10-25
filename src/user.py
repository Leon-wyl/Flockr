from error import InputError
from error import AccessError
from database import *
from utility import *
from auth import *

def user_profile(token, u_id):
    check_valid_user(u_id)
    user = data_user(u_id)
    check_valid_token(token)
    return {
        'user': {
            'u_id': u_id,
            'email': user['email'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle'],
        }
    }

def user_profile_setname(token, name_first, name_last):
    user = is_token_exist(token)
    check_name_length(name_first, name_last)
    user['name_first'] = name_first
    user['name_last'] = name_last
    return {
    }

def user_profile_setemail(token, email):
    email_check(email)
    if data_email_search(email) == None:    # if no one has the same email as this one
        user = is_token_exist(token)        # find the user with token
        user['email'] = email
        return {
        }
    raise InputError("The email has already been used by another user")

def user_profile_sethandle(token, handle_str):
    if not is_token_exist(token):
        raise AccessError('You are not authorised to change handle')
    user = is_token_exist(token)        # find the user with token
    check_handle_length(handle_str)
    check_handle_exist(handle_str)
    user['handle'] = handle_str
    return {
    }