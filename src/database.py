'''The database for the user and channel data'''
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
    '''If the register is the first register, set this register as a flockr owner. Then
    upload the data of a new user to the database'''
    permission_id = 2
    if u_id == 0:
        permission_id = 1
    data['users'].append({
        'u_id': u_id,
        'email': email,
        'password': password,
        'name_first': name_first,
        'name_last': name_last,
        'handle': handle,
        'token': token,
        'permission_id': permission_id
    })

def data_login(u_id, token):
    data['users'][u_id]['token'] = token

def data_logout(u_id):
    '''If a valid u_id is given, and the user is successfully
     logged out, returns true, otherwise false.'''

    if u_id in range(len(data['users'])):
        data['users'][u_id]['token'] = None
        return {
            'is_success': True,
        }
    return {
        'is_success': False,
    }

def data_u_id():
    '''Create u_id'''
    return len(data['users'])
    
def data_last_channel_id():
    return data['channels'][-1]['channel_id']
    
def data_add_channel(new_channel):
    data['channels'].append(new_channel)
    return
    
def is_channel_empty():
    if data['channels'] == []:
        return True
    return False

def is_user_exist(u_id):
    for user in data['users']:
        if u_id == user['u_id']:
            return True
    return False

def is_public_channel(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel['visibility']

def is_channel_exist(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return True
    return False

def data_channels_list():
    # creat an empty list and append channels to it
    channels = []
    for channel in data['channels']:
        new_channel = {}
        new_channel['channel_id'] = channel['channel_id']
        new_channel['name'] = channel['name']
        channels.append(new_channel)
    return channels

def data_user_channels(u_id):
    # create an empty list
    user_channel = []
    for channel in data['channels']:
        for member in channel['members']:
            # add channel to list if the user is a member of that channel
            if member['u_id'] == u_id:
                new_channel = {}
                new_channel['channel_id'] = channel['channel_id']
                new_channel['name'] = channel['name']
                user_channel.append(new_channel)
                break
    return user_channel


def is_owner_exist(u_id, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for owner in channel['owners']:
                # check if the person who runs this command is owner
                if u_id == owner['u_id']:
                    return True
    return False

def is_member_exist(u_id, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['members']:
                # check if the person who runs this command is owner
                if u_id == member['u_id']:
                    return True
    return False




def data_add_owner(u_id, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for user in data['users']:
                if u_id == user['u_id']:
                    channel['owners'].append(user)
                    return
            
    

def data_remove_owner(u_id, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for user in data['users']:
                if u_id == user['u_id']:
                    channel['owners'].remove(user)
                    return

















