from database import data

def channels_list(token):
    exist = False
    for user in data['users']:
        if token == user['u_id']:
            exist = True
            break
    if not exist:
        raise Exception(f"Invalid token!")
    user_channel = []
    for channel in data['channels']:
        for member in channel['members']:
            if member['u_id'] == token:
                user_channel.append(channel)
                break
    return {
        'channels': user_channel,
    }

def channels_listall(token):
    exist = False
    for user in data['users']:
        if token == user['u_id']:
            exist = True
            break
    if not exist:
        raise Exception(f"Invalid token!")
    return {
        'channels': data['channels'],
    }

def channels_create(token, name, is_public):
    if len(name) > 20:
        raise Exception(f"This name is too long!")
    exist = False
    for user in data['users']:
        if token == user['u_id']:
            exist = True
            break
    if not exist:
        raise Exception(f"Invalid token!")

    if data['channels'] == []:
        channel_id = 1
    else:
        channel_id = data['channels'][-1]['channel_id'] + 1
    new_channel = {
        'channel_id' : channel_id,
        'name' : name,
        'visibility' : is_public,
        'members' : [],
        'owners' : [],
    }
    data['channels'].append(new_channel)
    return {
        'channel_id': channel_id,
    }


