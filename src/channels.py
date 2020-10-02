from database import data

# Provide a list of all channels (and their associated details) 
# that the authorised user is part of
def channels_list(token):
    # if token is invalid raise an Exception
    exist = False
    for user in data['users']:
        if token == user['u_id']:
            exist = True
            break
    if not exist:
        raise Exception(f"Invalid token!")
    # creat an empty list
    user_channel = []
    for channel in data['channels']:
        for member in channel['members']:
            # add channel to list if the user is a member of that channel
            if member['u_id'] == token:
                user_channel.append(channel)
                break
    return {
        'channels': user_channel,
    }



# Provide a list of all channels (and their associated details)
def channels_listall(token):
    # if token is invalid raise an Exception
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

# Creates a new channel with that name that is 
# either a public or private channel
def channels_create(token, name, is_public):
    # if the name is more than 20 or token is invalid raise an Exception
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
        # when the channel is empty
        channel_id = 0
    else:
        # The last channel's id plus 1
        channel_id = data['channels'][-1]['channel_id'] + 1
    new_channel = {
        'channel_id' : channel_id,
        'name' : name,
        'visibility' : is_public,
        'members' : [],
        'owners' : [],
        'messages' : [],
    }
    # add new_channel to the list
    data['channels'].append(new_channel)
    return {
        'channel_id': channel_id,
    }


