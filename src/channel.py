from error import InputError
from error import AccessError
from database import *
from utility import *
from auth import *

def channel_invite(token, channel_id, u_id):
    check_valid_user(u_id)
    check_valid_token(token)
    # valid_channel returns the info of channel of given channel_id
    check_valid_channel(channel_id)
    token_id = auth_u_id_from_token(token)
    check_member_exist(token_id, channel_id)
    check_member_not_exist(u_id, channel_id)
    data_add_member(u_id, channel_id)
    return {}

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

# Given a Channel with ID channel_id that the authorised user is part of, 
# return up to 50 messages between index "start" and "start + 50". 
# Message with index 0 is the most recent message in the channel. 
# This function returns a new index "end" which is the value of "start + 50", 
# or, if this function has returned the least recent messages in the channel, 
# returns -1 in "end" to indicate there are no more messages to load after this return.

def channel_messages(token, channel_id, start):
    channel = valid_channel(channel_id)
    valid_member(channel, token)
    message_count = 0
    # Check if message start is a valid start, raise InputError if invalid 
    if start > len(channel['messages']):
        raise InputError("You message is greater than the total number of messages in the channel")
    if message_count > 50:
        end = start + 50
    else:
        end = -1
    # Append message in channel into a new list, return the list
    message_list = []
    for message in channel['messages']:
	    message_list.append(message)
    return message_list, start, end

def channel_leave(token, channel_id):
    channel = valid_channel(channel_id)
    member = valid_member(channel, token)
    channel['members'].remove(member)
    return {}

def channel_join(token, channel_id):
    check_valid_token(token)
    check_valid_channel(channel_id)
    u_id = auth_u_id_from_token(token)
    # make sure member doesn't exist before joining
    check_member_not_exist(u_id, channel_id)
    check_public_channel(channel_id)
    data_add_member(u_id, channel_id)
    return {}

# Make user with user id u_id an owner of this channel
def channel_addowner(token, channel_id, u_id):
    check_valid_channel(channel_id)
    check_valid_token(token)
    check_valid_user(u_id)
    # make sure the user with u_id is not a owner
    check_owner_not_exist(u_id, channel_id)
    # check whether the user with user id of token is authorised to use add owner
    token_id = auth_u_id_from_token(token)
    check_owner_exist(token_id, channel_id)
    data_add_owner(u_id, channel_id)
    if not is_member_exist(u_id, channel_id):
        data_add_member(u_id, channel_id)
    return {}

# Remove user with user id u_id an owner of this channel
def channel_removeowner(token, channel_id, u_id):
    check_valid_channel(channel_id)
    check_valid_token(token)
    check_valid_user(u_id)
    check_owner_exist(u_id, channel_id)
    token_id = auth_u_id_from_token(token)
    check_owner_exist(token_id, channel_id)
    data_remove_owner(u_id, channel_id)
    return {}


