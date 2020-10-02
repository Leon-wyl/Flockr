import channels
import auth
from database import data

def channel_invite(token, channel_id, u_id):

    # Invalid user
    check = 0
    for user in data['users']:
        if u_id == user['u_id']:
            check = 1
    if check == 0:
        raise Exception(f'InputError, invitation failed, invalid user')

    # Invalid channel
    check = 0
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            check = 1
            for member in channel['members']:
                if token == member['u_id']:
                    # if authorised, invite user with user_id into the channel
                    import channel_join
                    channel_join(u_id, channel_id)
    if check == 0:
        raise Exception(f'InputError, invitation failed, invalid channel')

    # the authorised user is not already a member of the channel
    raise Exception(f'AccessError, invitation failed, permission denied')

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

    # check if channel exsist
    check = 0
    for channel in channels.channels_listall(token):
        if channel['channel_id'] == channel_id:
            check = 1
            # find the member
            for member in channel['members']:
                if token == member['u_id']:
                    member.clear() # clean member details
    if check == 0:
        raise Exception(f"InputError, leave failed, channel does not exsist")

    # else, user is not in the channel
    raise Exception(f"AccessError, leave failed, you have not joined the channel yet")


def channel_join(token, channel_id):

    # check if channel_id is valid
    check = 0
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            check = 1
            # check if the channel is public
            if channel['visibility'] == False:
                raise Exception(f"AccessError, join failed, channel is private")
    if check == 0:
        raise Exception(f"InputError, join failed, channel is invalid")
    
    # if nothing goes wrong, join the channel
    for user in data['users']:
        if token == user['u_id']:
            member = {
                'u_id': user['u_id'],
                'name_first': user['name_first'],
                'name_last': user['name_last'],
            }
            data['channels']['members'].append(member)
    
    raise Exception(f'InputError, user is invalid')
    

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }
