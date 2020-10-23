from error import InputError
from error import AccessError
from database import *
from utility import *
from auth import *

def user_profile(token, u_id):
    '''user = valid_user(u_id)
    if token == user['token']:
        return {
            'user': {
                'u_id': u_id,
                'email': user[email],
                'name_first': user[name_first],
                'name_last': user[name_last],
                'handle_str': user[handle],
            },
        }'''

def user_profile_setname(token, name_first, name_last):
    return {
    }

def user_profile_setemail(token, email):
    return {
    }

def user_profile_sethandle(token, handle_str):
    return {
    }