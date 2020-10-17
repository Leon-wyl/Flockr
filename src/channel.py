import error
import channels
import auth
from error import InputError
from error import AccessError
from database import data


def channel_invite(token, channel_id, u_id):
    valid_user(u_id)
    channel = valid_channel(channel_id) #valid_channel returns the info of channel of given channel_id
    valid_member(channel, token)
    channel_join(u_id, channel_id)

# Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel.
def channel_details(token, channel_id): 
    for channels in data['channels']:
        # Check for valid channel ID inputted
        if channel_id == channels['channel_id']: 
            for members in channels['members']:
                # Check if user is in the channel
                if token == members['u_id']:
                    channel_name = channels['name']
                    owners = []
                    # Append owner in channel into a new list
                    for owner in channels['owners']:
                        new_owner = {}
                        new_owner['u_id'] = owner['u_id']
                        new_owner['name_first'] = owner['name_first']
                        new_owner['name_last'] = owner['name_last']
                        owners.append(new_owner)
                    # Append member in channel into a new list
                    members = []
                    for member in channels['members']:
                        new_member = {}
                        new_member['u_id'] = member['u_id']
                        new_member['name_first'] = member['name_first']
                        new_member['name_last'] = member['name_last']
                        members.append(new_member)
                    # Return channel name, owner list and member list
                    return {
                        'name': channel_name,
                        'owner_members': owners,
                        'all_members': members,
                    }
                
            raise AccessError("You are unauthorised to obtain the details of this channel")
    raise InputError("You have entered an invalid channel ID")

# Given a Channel with ID channel_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.
def channel_messages(token, channel_id, start):
    channel = valid_channel(channel_id)      
    valid_member(channel, token)
    message_count = 0
    # Check if message start is a valid start, raise InputError if invalid 
    if start > len(channel['messages']):
        raise InputError("You have entered an invalid start which is greater than the total number of messages in the channel")
    if message_count > 50:
        end = start + 50
    else:
        end = -1
    # Append message in channel into a new list, return the list
    message_list =[]
    for message in data['channels'][channel_count]['messages']:
	    message_list.append(message)                
    return message_list, start, end           

def channel_leave(token, channel_id):
    channel = valid_channel(channel_id)
    member = valid_member(channel, token)
    channel['members'].remove(member)

def channel_join(token, channel_id):
    user = valid_user(token)
    channel = valid_channel(channel_id)
    is_public_channel(channel)
    channel['members'].append(user)

# Make user with user id u_id an owner of this channel
def channel_addowner(token, channel_id, u_id):
    channel = valid_channel(channel_id)
    # addtional checks
    for owner in channel['owners']:
        if u_id == owner['u_id']:
            raise InputError('User is already an owner of the channel')
    # check whether the user with user id of token is authorised to use add owner
    if valid_owner(token, channel) == False:
        raise AccessError('You are not authorised to add an owner')
    owner = valid_user(u_id)
    channel['owners'].append(owner)

# Remove user with user id u_id an owner of this channel
def channel_removeowner(token, channel_id, u_id):
    channel = valid_channel(channel_id)
    if not valid_owner(u_id, channel):
        raise InputError('User is not an owner of this channel')
    owner_id = valid_owner(token, channel)
    if not owner_id:
        raise AccessError('You are not authorised to remove an owner')
    owner = valid_user(owner_id)
    channel['owners'].remove(owner)

def valid_user(u_id):
    for user in data['users']:
        if u_id == user['u_id']:
            return user
    raise InputError('User is invalid')

def is_public_channel(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            if channel['visibility'] == False:
                raise AccessError("Channel is private")

def valid_channel(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel
    raise InputError("Channel_id is invalid")

# check if the the user who use add_owner is permitted to add owner 
# and check if the user being added is already an owner
def valid_owner(u_id, channel):
    for owner in channel['owners']:
        # check if the person who runs this command is owner
        if u_id == owner['u_id']:
            return u_id 
    return False

def valid_member(channel, u_id):
    for member in channel['members']:
        if u_id == member['u_id']:
            return member
    raise AccessError('Invalid member id')