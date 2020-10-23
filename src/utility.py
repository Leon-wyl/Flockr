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









