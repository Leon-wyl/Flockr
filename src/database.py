data = {
    'users': [],
    'channels': [],
}

def data_email_search(email):
    ''' Loop through the database to find whether there is a same email in the database'''
    for user in data['users']:
        if user['email'] == email:
            return user
    return None

def data_handle(name_first, name_last, u_id):
    '''Create a handle using the first name and the last name'''
    handle = (name_first + name_last).lower()
    for user in data['users']:
        if user['handle'] == handle[:20]:
            # Solution for a handle that is the same as a existing handle being created
            handle = handle[:6] + str(u_id)
            handle = handle[:20]
            break
    return handle

def data_upload(u_id, email, password, name_first, name_last, handle, token):
    '''Upload the data of a new user to the database'''
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

def data_login(email):
    '''Change login state'''
    for user in data['users']:
        if user['email'] == email:
            user['login'] = True

def data_logout(u_id):
    '''Given an active u_id, invalidates the taken to
    log the user out. If a valid u_id is given, and the
    user is successfully logged out, it returns true,
    otherwise false.'''

    if u_id in range(len(data['users'])) and data['users'][u_id]['login']:
        data['users'][u_id]['login'] = False
        return {
            'is_success': True,
        }

    return {
        'is_success': False,
    }

def data_u_id():
    return len(data['users'])
