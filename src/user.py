from error import InputError
from error import AccessError
from database import *
from utility import *
from auth import *

def user_profile(token, u_id):
    check_valid_user(u_id)
    user = data_user(u_id)
    if token == user['token']:
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
    user = check_valid_token(token)
    check_name_length(name_first, name_last)
    user['name_first'] = name_first
    user['name_last'] = name_last
    return {
    }

def user_profile_setemail(token, email):
    auth_email_check(email)
    if data_email_search(email) == None:    # if no one has the same email as this one
        user = check_valid_token(token)
        user['email'] == email
    return {
    }

def user_profile_sethandle(token, handle_str):
    return {
    }