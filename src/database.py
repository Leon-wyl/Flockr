from error import AccessError

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

def data_logout(token):
    '''If a valid u_id is given, then turn the token into None to
     logged out, returns true, otherwise raise AccessError.'''
    
    for user in data['users']:
        if user['token'] == token:
            user['token'] = None
            return {
                'is_success': True
            }
    raise AccessError("Error, token is invalid")

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


def is_token_exist(token):
    for user in data['users']:
        if token == user['token']:
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
                if u_id == owner['u_id']:
                    return True
    return False


def is_member_exist(u_id, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['members']:
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



def data_add_member(u_id, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for user in data['users']:
                if u_id == user['u_id']:
                    channel['members'].append(user)
                    return
            
    

def data_remove_member(u_id, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for user in data['users']:
                if u_id == user['u_id']:
                    channel['members'].remove(user)
                    return


def channel_numbers():
    return len(data['channels'])

def data_clear():
    data['users'].clear()
    data['channels'].clear()

'''
def is_login(token):
    for user in data['users']:
        if token == user['token']:
            return user['login']
'''



def data_users_list():
    user_list = []
    for user in data['users']:
        new_user = {}
        new_user['u_id'] = user['u_id']
        new_user['email'] = user['email']
        new_user['name_first'] = user['name_first']
        new_user['name_last'] = user['name_last']
        new_user['handle_str'] = user['handle']
        user_list.append(new_user)
    return user_list
        

def data_permission(u_id):
    for user in data['users']:
        if user['u_id'] == u_id:
            return user['permission_id']

      
def data_change_permission(u_id, permission_id):
    for user in data['users']:
        if user['u_id'] == u_id:
            user['permission_id'] = permission_id
            return


def data_search_message(query_str, u_id):
    message_list = []
    for channel in data['channels']:
        for member in channel['members']:
            # add channel to list if the user is a member of that channel
            if member['u_id'] == u_id:
                for message in channel['messages']:
                    if query_str in message['message']:
                        new_massage = {}
                        new_massage['message_id'] = message['message_id']
                        new_massage['u_id'] = message['u_id']
                        new_massage['message'] = message['message']
                        new_massage['time_created'] = message['time_created']
                        message_list.append(new_massage)
                break
    return message_list


