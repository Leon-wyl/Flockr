import re
from database import data_email_search, data_handle_create, data_upload, data_login, data_logout, data_u_id_create
from error import InputError

regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

def auth_login(email, password):
    '''Given a registered user's email and
    password and generates a valid token
    for the user to remain authenticated'''

    if not re.search(regex, email):
        # Test whether the email input is valid. If not, raisee exception
        raise InputError("Email entered is not a valid email")

    # Find out whether the input email is a registered email
    correct_user = data_email_search(email)

    if correct_user == None:
        # If the email has not been registered, raise exception
        raise InputError(f"Error, email address {email} has not been registered yet")

    if correct_user['password'] != password:
        # If the password is not correct, raise exception
        raise InputError("Password is not correct")

    # Change login state
    data_login(email)

    return {
        'u_id': correct_user['u_id'],
        'token': correct_user['token'],
    }

def auth_logout(token):
    '''Given an active token, invalidates the taken to
    log the user out. If a valid token is given, and the
    user is successfully logged out, it returns true,
    otherwise false.'''
    u_id = int(token)

    return data_logout(u_id)

def auth_register(email, password, name_first, name_last):
    '''Given a user's first and last name, email address, and password, create a new account
    for them and return a new token for authentication in their session. A handle is generated
    that is the concatentation of a lowercase-only first name and last name. If the
    concatenation is longer than 20 characters, it is cutoff at 20 characters. If the handle
    is already taken, you may modify the handle in any way you see fit to make it unique.'''

    if not re.search(regex, email):
        # Test whether the email input is valid. If not, raisee exception
        raise InputError("Email entered is not a valid email")
    
    if data_email_search(email) != None:
        # If there is a same email registered in the database, raise exception
        raise InputError(f"Email address {email} is already being used by another user")

    if len(password) in range(0, 6):
        # If the length of password is too short (less than 6), raise exception
        raise InputError("Password entered is less than 6 characters long")

    if len(name_first) not in range(1, 51):
        # If the length of name_first is out of range (1 to 50), raise exception
        raise InputError("name_first is not between 1 and 50 characters inclusively in length")

    if len(name_last) not in range(1, 51):
        # If the length of name_last is out of range (1 to 50), raise exception
        raise InputError("name_last is not between 1 and 50 characters inclusively in length")

    # Create u_id and token
    u_id = data_u_id_create()
    token = str(u_id)

    # Create a handle and upload the data
    handle = data_handle_create(name_first, name_last, u_id)
    data_upload(u_id, email, password, name_first, name_last, handle, token)

    return {
        'u_id': u_id,
        'token': token,
    }
