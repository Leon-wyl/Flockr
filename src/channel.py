import channels

def channel_invite(token, channel_id, u_id):

    # Invalid user
    check = 0
    for user in data['users']:
        if u_id == user['u_id']:
            check = 1
    if check = 0:
        raise Exception('Invitation failed, user does not exsist')

    # Invalid channel
    check = 0
    for channel in data['channels']:
        if channel_id == channel['id']:
            check = 1
            for member in channel['members']:
                if token == member['member_id']:
                    # if authorised, invite user with user_id into the channel
                    # member[]
                    #
                    #
                    #
    if check = 0:
        raise Exception('Invitation failed, channel has not been created')

    # the authorised user is not already a member of the channel
    raise Exception('invite failed, permission denied')

def channel_details(token, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages(token, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave(token, channel_id):

    # check if channel does not exsist
    check = 0
    for channels in channels.channels_listall(token):
        if channels['channel_id'] == channel_id:
            check = 1
    if check == 0:
        raise Exception("leave failed, channel does not exsist")

    # check if user is in the channel
    for channel in data['channels']:
        if channel['member_id'] == token:
            channel['member_id'] == None

    # else, user is not in the channel
    raise Exception("leave railed, you have not joined the channel yet")


def channel_join(token, channel_id):

    # check if channel does not exsist
    check = 0
    for channels in data['channels']:
        if channels['id'] == channel_id:
            check = 1
    if check == 0:
        raise Exception("join failed, channel does not exsist")

    # check if already joined
    for channels in channels.channels_list(token):
        if channels['id'] == channel_id:
            raise Exception("join failed, you already joined this channel")
    
    # if nothing goes wrong, join the channel
    from data import channels
    for user in data.['users']:
        if token == user.token:
            channels['members'].append({
                u_id = user.u_id
                name_first = user.name_first
                name_last = user.name_last
            })
    

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }