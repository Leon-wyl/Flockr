from database import *
from auth import *
from error import InputError
from error import AccessError

def check_valid_user(u_id):
    if not is_user_exist(u_id):
        raise InputError('User is invalid')
    return
    
def check_valid_token(token): 
    u_id = auth_u_id_from_token(token)
    if not is_token_exist(token):
        raise AccessError('Token is invalid') 
    if not is_login(u_id):
        raise AccessError('Token is invalid')
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
    

def check_member_exist(u_id, channel_id):
    if not is_member_exist(u_id, channel_id):
        raise InputError('Member does not exist')
    return


def check_member_not_exist(u_id, channel_id):
    if is_member_exist(u_id, channel_id):
        raise InputError('Member already exists')
    return



def check_public_channel(channel_id):
    if not is_public_channel(channel_id):
        raise AccessError("Channel is private")
    return







# Those touch data
def valid_user(u_id):
    for user in data['users']:
        if u_id == user['u_id']:
            return user
    raise InputError('User is invalid')



def valid_channel(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel
    raise InputError("Channel_id is invalid")

# check if the the user who use add_owner is permitted to add owner
def valid_owner(u_id, channel):
    for owner in channel['owners']:
        # check if the person who runs this command is owner
        if u_id == owner['u_id']:
            return u_id 
    raise InputError('You are not an owner yet! Only an owner have this permission')

def valid_member(channel, u_id):
    for member in channel['members']:
        if u_id == member['u_id']:
            return member
    raise AccessError('Invalid member id')














