from database import *
from utility import check_valid_token, check_valid_channel_name
from auth import auth_u_id_from_token
from error import InputError, AccessError

# Provide a list of all channels (and their associated details) 
# that the authorised user is part of
def channels_list(token):
    # if token is invalid raise an Exception
    check_valid_token(token)
    u_id = auth_u_id_from_token(token)
    return {
        'channels': data_user_channels(u_id),
    }



# Provide a list of all channels (and their associated details)
def channels_listall(token):
    # if token is invalid raise an Exception
    check_valid_token(token)
    return {
        'channels': data_channels_list(),
    }

# Creates a new channel with that name that is 
# either a public or private channel
def channels_create(token, name, is_public):
    # if the name is more than 20 or token is invalid raise an Exception
    check_valid_channel_name(name)
    check_valid_token(token)
    if is_channel_empty():
        # when the channel is empty
        channel_id = 0
    else:
        # The last channel's id plus 1
        channel_id = data_last_channel_id() + 1
    new_channel = {
        'channel_id' : channel_id,
        'name' : name,
        'visibility' : is_public,
        'members' : [],
        'owners' : [],
        'messages' : [],
    }
    # add new_channel to the list
    data_add_channel(new_channel)
    u_id = auth_u_id_from_token(token)
    data_add_owner(u_id, channel_id)
    data_add_member(u_id, channel_id)
    return {
        'channel_id': channel_id,
    }
