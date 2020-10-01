import re

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

data = {
    'users':[],
    'channels':[],
}

def auth_login(email, password):
    '''Given a registered users' email and 
    password and generates a valid token 
    for the user to remain authenticated'''
    global data

    if not (re.search(regex,email)):  
        raise Exception(f"Email entered is not a valid email")

    correct_user = None
    for user in data['users']:
        if user['email'] == email:
            correct_user = user

    if correct_user == None:
        raise Exception(f"Error, email address {email} has not been registered yet")

    if correct_user['password'] != password:
        raise Exception(f"Error, wrong password")
    
    return {
        'u_id': correct_user['u_id'],
        'token': correct_user['u_id'],
    }

def auth_logout(token):
    '''Given an active token, invalidates the taken to 
    log the user out. If a valid token is given, and the 
    user is successfully logged out, it returns true, 
    otherwise false.'''
    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    '''Given a user's first and last name, email address, and password, create a new account
    for them and return a new token for authentication in their session. A handle is generated
    that is the concatentation of a lowercase-only first name and last name. If the
    concatenation is longer than 20 characters, it is cutoff at 20 characters. If the handle 
    is already taken, you may modify the handle in any way you see fit to make it unique.'''
    global data

    if not (re.search(regex,email)):  
        raise Exception(f"Email entered is not a valid email")

    for user in data['users']:
        if user['email'] == email:
            raise Exception(f"Email address {email} is already being used by another user")
    
    if len(password) in range(0, 6):
        raise Exception("Password entered is less than 6 characters long")

    if len(name_first) not in range(1, 50):
        raise Exception("name_first is not between 1 and 50 characters inclusively in length")

    if len(name_last) not in range(1, 50):
        raise Exception("name_last is not between 1 and 50 characters inclusively in length")

    u_id = len(data['users'])

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
    })

    return {
        'u_id': u_id,
        'token': u_id,
    }
