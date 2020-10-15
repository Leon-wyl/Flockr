import error
import channels
import auth
from error import InputError
from error import AccessError
from database import data


def channel_invite(token, channel_id, u_id):

    # Check for valid user ID input
    check = 0
    for user in data['users']:
        if u_id == user['u_id']:
            check = 1
    if check == 0:
        raise Exception(f'InputError, invitation failed, invalid user')
    # Check for valid channel ID input
    checkchannel = 0
    checkuser = 0
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            checkchannel = 1
            for member in channel['members']:
                if token == member['u_id']:
                    checkuser = 1
                    # if authorised, invite user with user_id into the channel
                    channel_join(u_id, channel_id)
                    break
    if checkchannel == 0:
        raise Exception(f'InputError, invitation failed, invalid channel')
    # Check if the user is authorised in the channel
    if checkuser == 0:
        raise Exception(f'AccessError, invitation failed, unauthorised user')




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
    # Check for valid channel ID inputted, raise InputError if invalid
    valid_id = False
    channel_count = 0
    message_count = 0
    for channels in data['channels']:
        if channel_id == channels['channel_id']:
            valid_id = True
            break
        channel_count =+ 1
    if not valid_id:
        raise InputError("You have entered an invalid channel ID")
        
    # Check if user is an authorised user in the channel, raise AccessError if unauthorised        
    authorised_user = False
    for members in channels['members']:
        if token == members['u_id']:
            authorised_user = True
            break
    if not authorised_user:
        raise AccessError("You are unauthorised to obtain the messages of this channel") 
        
    # Check if message start is a valid start, raise InputError if invalid 
    if start > len(data['channels'][channel_count]['messages']):
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
    # Check if channel exist
    check = 0
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:           
            # Find the member
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

# Make user with user id u_id an owner of this channel
def channel_addowner(token, channel_id, u_id):
    # check whether the user is valid
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
            # find if the user with u_id is owner
            owner_exist = False
            for owner in channel['owners']:
                if u_id == owner['u_id']:
                    owner_exist = True
            for owner in channel['owners']:
                # find if the user with token is owner
                if token == owner['u_id'] and not owner_exist:
                    check = 1
                    channel['owners'].append(add_owner)
    # if one of the requirements is not reached
    if check == 0:
        raise Exception(f'InputError, invitation failed, invalid user')             

# Remove user with user id u_id an owner of this channel
def channel_removeowner(token, channel_id, u_id):
    check = 0
    for channel in data['channels']:
        # find channel with channel_id
        if channel_id == channel['channel_id']:
            # find if the user with u_id is owner
            owner_exist = False
            for owner in channel['owners']:
                if u_id == owner['u_id']:
                    remove_owner = owner
                    owner_exist = True
            for owner in channel['owners']:
                # find if the user with token is owner
                if token == owner['u_id'] and owner_exist:
                    check = 1
                    channel['owners'].remove(remove_owner)
    # if one of the requirements is not reached
    if check == 0:
        raise Exception(f'InputError, invitation failed, invalid user') 
