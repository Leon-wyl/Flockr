from database import *
from error import InputError
from error import AccessError

def check_valid_user(u_id):
    if not is_user_exist(u_id):
        raise InputError('User is invalid')
    return

def check_valid_channel(channel_id):
    if not is_channel_exist(channel_id):
        raise InputError("Channel is invalid")
    return
    
    
def check_valid_channel_name(name):
    if len(name) > 20:
        raise InputError(f"This name is too long!")
    return

def check_owner_exist(u_id, channel_id):
    if not is_owner_exist(u_id, channel_id):
        raise InputError('Owner does not exist')
    return
    
    
def check_owner_not_exist(u_id, channel_id):
    if is_owner_exist(u_id, channel_id):
        raise InputError('Already an owner of the channel')
    return
