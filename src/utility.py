import jwt
from database import *
from error import InputError
from error import AccessError

SECRET = "fri09mango01"

def check_valid_permission_id(permission_id):
    if permission_id != 1 and permission_id != 2:
        raise InputError("Invalid permission_id")
    return
    
    
def check_global_owner(u_id):
    if data_permission(u_id) != 1:
        raise AccessError("You are not owner of flockr")
    return

def check_valid_user(u_id):
    if not is_user_exist(u_id):
        raise InputError('User is invalid')
    return
    
def check_valid_token(token): 
    if not is_token_exist(token) or token == None:
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

def check_valid_message_start(start, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            if start > len(channel['messages']):
                raise InputError("Start is greater than the total number of messages in the channel")
            return

def token_generate(u_id):
    '''Return the generated token'''
    return jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256').decode('utf-8')

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
    
def check_valid_message_length(message):
    if len(message) > 1000:
        raise InputError('Message is more than 1000 characters')
    return

def check_message_exist(message_id):
    for channel in data['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                return
    raise InputError('Message does not exist')
    
def check_authorised_member_message(u_id, channel_id, message_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for owner in channel['owners']:
                if u_id == owner['u_id']:
                    return 
            for message in channel['messages']:
                if u_id == message['u_id']:
                    return
    raise AccessError('User is not the authorised user making this request nor an owner of this channel or the flockr') 
    
    

