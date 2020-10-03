import re
from database import data

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

def auth_login(email, password):
    '''Given a registered user's email and
    password and generates a valid token
    for the user to remain authenticated'''
    global data

    if not re.search(regex, email):
        raise Exception("Email entered is not a valid email")

    correct_user = None
    for user in data['users']:
        if user['email'] == email:
            correct_user = user

    if correct_user is None:
        raise Exception(f"Error, email address {email} has not been registered yet")

    if correct_user['password'] != password:
        raise Exception("Error, wrong password")

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
        data['users'][u_id]['login'] = False
        return {
            'is_success': True,
        }
    else:
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
        raise Exception("Email entered is not a valid email")

    for user in data['users']:
        if user['email'] == email:
            raise Exception(f"Email address {email} is already being used by another user")

    if len(password) in range(0, 5):
        raise Exception("Password entered is less than 6 characters long")

    if len(name_first) not in range(1, 50):
        raise Exception("name_first is not between 1 and 50 characters inclusively in length")

    if len(name_last) not in range(1, 50):
        raise Exception("name_last is not between 1 and 50 characters inclusively in length")

    u_id = len(data['users'])
    token = str(u_id)

    handle = (name_first + name_last).lower()
    for user in data['users']:
        if user['handle'] == handle[:20]:
            handle = handle[:6] + str(u_id)
            handle = handle[:20]
            break

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
