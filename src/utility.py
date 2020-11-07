import jwt
import re
import hashlib
from database import *
from error import InputError
from error import AccessError

SECRET = "fri09mango01"
REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

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
        raise AccessError('Owner does not exist')
    return
    
    
def check_owner_not_exist(u_id, channel_id):
    if is_owner_exist(u_id, channel_id):
        raise InputError('User is already an owner of the channel')
    return


def check_authorised_member(u_id, channel_id):
    if not is_member_exist(u_id, channel_id):
        raise AccessError('Member does not exist')
    return 

def check_member_not_exist(u_id, channel_id):
    if is_member_exist(u_id, channel_id):
        raise InputError('Member already exists')
    return

def check_handle_exist(handle_str):
    for user in data['users']:
        if user['handle'] == handle_str:
            raise InputError('Handle is already used by another user')
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
    raise InputError("Channel is invalid")
               
def token_generate(u_id):
    '''Return the generated token'''
    return jwt.encode({'u_id': u_id}, SECRET, algorithm='HS256').decode('utf-8')
    
def check_name_length(name_first, name_last):
    if len(name_first) > 0 and len(name_first) <= 50:
        if len(name_last) >0 and len(name_last) <= 50:
            return True
        raise InputError("Lastname is too long!")
    raise InputError("Firstname is too long!")

def check_handle_length(handle_str):
    if len(handle_str) > 20:
        raise InputError("Handle is too long!")
    if len(handle_str) < 3:
        raise InputError("Handle is too short!")
    return

def valid_channel(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel
    raise InputError("Channel_id is invalid")

def valid_member(channel, token):
    for member in channel['members']:
        if token == member['token']:
            return member
    raise AccessError('Invalid token')
    
def check_valid_message_length(message):
    if len(message) > 1000:
        raise InputError('Message is more than 1000 characters')
    return
    
''' def check_message_exist(message_id):
    for channel in data['channels']:
        for message in channel['messages']:
            if message_id == message['message_id']:
                return
    raise InputError('Message does not exist')
    '''
    
def check_authorised_member_message(u_id, channel_id, message_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for owner in channel['owners']:
                if u_id == owner['u_id']:
                    return 
            for message in channel['messages']:
                if u_id == message['u_id'] and message_id == message['message_id']:
                    return
    raise AccessError('User is not the authorised user making this request nor an owner of this channel or the flockr') 

def email_check(email):
    '''Test whether the email input is valid. If not, raise exception'''
    if not re.search(REGEX, email):
        raise InputError("Email entered is not a valid email")

def register_check(email, password, name_first, name_last):
    ''' Check whether the email, password, name_first,
    name_last valid. If one of them not, raise error'''
    email_check(email)

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

def login_check(email, password):
    '''Check whether the email and password are valid. If yes,
    return a dict of u_id and token. If not, raise error'''
    email_check(email)

    # Find out whether the input email is a registered email
    correct_user = data_email_search(email)

    if correct_user is None:
        # If the email has not been registered
        raise InputError(f"Error, email address {email} has not been registered yet")

    password = password_encode(password)
    if correct_user['password'] != password:
        # If the password is not correct
        raise InputError("Password is not correct")

    return correct_user['u_id']

def password_encode(password):
    ''' Return the encoded password'''
    return hashlib.sha256(password.encode()).hexdigest()

def check_authorised_member_channel(channel_id, u_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['members']:
                if u_id == member['u_id']:
                    return
    raise AccessError("User is not in channel")

def check_message_pinned(message_id, channel_id):
    if data_message_pinned(message_id, channel_id) == True:
        raise InputError("Message has already been pinned")

def check_message_unpinned(message_id, channel_id):
    if data_message_unpinned(message_id, channel_id) == True:
        raise InputError("Message is not pinned already")
