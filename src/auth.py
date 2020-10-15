import re
from database import data

regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

def auth_login(email, password):
    '''Given a registered user's email and
    password and generates a valid token
    for the user to remain authenticated'''
    global data

    if not re.search(regex, email):
        # Test whether the email input is valid. If not, raisee exception
        raise Exception("Email entered is not a valid email")

    # Find out whether the input email is a registered email
    correct_user = None
    for user in data['users']:
        if user['email'] == email:
            correct_user = user

    if correct_user is None:
        # If the email has not been registered, raise exception
        raise Exception(f"Error, email address {email} has not been registered yet")

    if correct_user['password'] != password:
        # If the password is not correct, raise exception
        raise Exception("Password is not correct")

    # Change login state
    correct_user['login'] = True

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

    if u_id in range(len(data['users'])) and data['users'][u_id]['login'] == True:
        # If the input u_id is a valid u_id and the login state is True, switch login state to false and return is_success True
        data['users'][u_id]['login'] = False
        return {
            'is_success': True,
        }
    else:
        # If not, return is_success False
        return {
            'is_success': False,
        }

def auth_register(email, password, name_first, name_last):
    '''Given a user's first and last name, email address, and password, create a new account
    for them and return a new token for authentication in their session. A handle is generated
    that is the concatentation of a lowercase-only first name and last name. If the
    concatenation is longer than 20 characters, it is cutoff at 20 characters. If the handle
    is already taken, you may modify the handle in any way you see fit to make it unique.'''
    global data

    if not re.search(regex, email):
        # Test whether the email input is valid. If not, raisee exception
        raise Exception("Email entered is not a valid email")

    # Loop through the database to find whether there is a same email registered in the database. If yes, raise exception
    for user in data['users']:
        if user['email'] == email:
            raise Exception(f"Email address {email} is already being used by another user")

    if len(password) in range(0, 6):
        # If the length of password is too short (less than 6), raise exception
        raise Exception("Password entered is less than 6 characters long")

    if len(name_first) not in range(1, 51):
        # If the length of name_first is out of range (1 to 50), raise exception
        raise Exception("name_first is not between 1 and 50 characters inclusively in length")

    if len(name_last) not in range(1, 51):
        # If the length of name_last is out of range (1 to 50), raise exception
        raise Exception("name_last is not between 1 and 50 characters inclusively in length")

    # Create u_id and token
    u_id = len(data['users'])
    token = str(u_id)

    # Create handle
    handle = (name_first + name_last).lower()
    for user in data['users']:
        if user['handle'] == handle[:20]:
            # Solution for a handle that is the same as a existing handle being created
            handle = handle[:6] + str(u_id)
            handle = handle[:20]
            break

    # Upload the data to the database
    data['users'].append({
        'u_id': u_id,
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
        'handle': handle,
        'login': False,
        'token': token,
    })

    return {
        'u_id': u_id,
        'token': token,
    }
