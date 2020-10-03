import error
import channels
import auth
from error import InputError
from error import AccessError
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
            for member in channel['members']:
                if token == member['u_id']:
                    check = 1
                    # if authorised, invite user with user_id into the channel
                    channel_join(u_id, channel_id)
                    break
    if check == 0:
        raise Exception(f'InputError, invitation failed, invalid channel')

    # the authorised user is not already a member of the channel



def channel_details(token, channel_id):
    #Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel.
    
    for channels in data['channels']:
        if channel_id == channels['channel_id']: 
            for members in channels['members']:
                if token == members['u_id']:
                    channel_name = channels['name']
                    owners = []
                    for owner in channels['owners']:
                        new_owner = {}
                        new_owner['u_id'] = owner['u_id']
                        new_owner['name_first'] = owner['name_first']
                        new_owner['name_last'] = owner['name_last']
                        owners.append(new_owner)
                    members = []
                    for member in channels['members']:
                        new_member = {}
                        new_member['u_id'] = member['u_id']
                        new_member['name_first'] = member['name_first']
                        new_member['name_last'] = member['name_last']
                        members.append(new_member)
                    return {
                        'name': channel_name,
                        'owner_members': owners,
                        'all_members': members,
                    }
                
            raise AccessError("You are unauthorised to obtain the details of this channel")
    raise InputError("You have entered an invalid channel ID")


def channel_messages(token, channel_id, start):
    #Given a Channel with ID channel_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.
    #channels.messages { message_id, u_id, message, time_created  }
    valid_id = False
    channel_count = 0
    for channels in data['channels']:
        if channel_id == channels['channel_id']:
            valid_id = True
            break
        channel_count =+ 1
    if not valid_id:
        raise InputError("You have entered an invalid channel ID")
            
    authorised_user = False
    for members in channels['members']:
        if token == members['u_id']:
            authorised_user = True
            break
    if not authorised_user:
        raise AccessError("You are unauthorised to obtain the messages of this channel") 
        
    owners = []
    if start > len(data['channels'][channel_count]['messages']):
        raise InputError("You have entered an invalid start which is greater than the total number of messages in the channel")
    if message_count > 50:
        end = start + 50
    else:
        end = -1
    message_list =[]
    for message in data['channels'][channel_count]['messages']:
	    channel['messages'].append(message)                
    return message_list, start, end           
    '''  
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
    '''


def channel_leave(token, channel_id):

    # check if channel exsist
    check = 0
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:           
            # find the member
            for member in channel['members']:
                if token == member['u_id']:
                    check = 1
                    channel['members'].remove(member)
                    break
                     # clean member details
    if check == 0:
        raise Exception(f"InputError, leave failed, channel does not exsist")

    # else, user is not in the channel


def channel_join(token, channel_id):

    # check if channel_id is valid
    # if nothing goes wrong, join the channel
    user_exist = False
    for user in data['users']:
        if token == user['u_id']:
            user_exist = True
            member = user
            break
    if not user_exist:
        raise Exception(f'InputError, user is invalid')
    channel_exist = False
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            # check if the channel is public
            if channel['visibility'] == False:
                raise Exception(f"AccessError, join failed, channel is private")
            channel['members'].append(member)
            channel_exist = True
            break
    if not channel_exist:
        raise Exception(f"InputError, join failed, channel is invalid")

def channel_addowner(token, channel_id, u_id):
    check = 0
    for user in data['users']:
        if u_id == user['u_id']:
            check = 1
            add_owner = user
            
    if check == 0:
        raise Exception(f'InputError, invitation failed, invalid user')
    check = 0
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            owner_exist = False
            for owner in channel['owners']:
                if u_id == owner['u_id']:
                    owner_exist = True
            for owner in channel['owners']:
                if token == owner['u_id'] and not owner_exist:
                    check = 1
                    channel['owners'].append(add_owner)
    if check == 0:
        raise Exception(f'InputError, invitation failed, invalid user')             

def channel_removeowner(token, channel_id, u_id):
    check = 0
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            owner_exist = False
            for owner in channel['owners']:
                if u_id == owner['u_id']:
                    remove_owner = owner
                    owner_exist = True
            for owner in channel['owners']:
                if token == owner['u_id'] and owner_exist:
                    check = 1
                    channel['owners'].remove(remove_owner)
    if check == 0:
        raise Exception(f'InputError, invitation failed, invalid user') 
