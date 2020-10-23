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

def channel_details(token, channel_id):
    check_valid_token(token)
    check_valid_channel(channel_id)
    u_id = auth_u_id_from_token(token)
    check_member_exist(u_id, channel_id)
    return {
        'name': data_channel_name(channel_id),
        'owner_members': data_channel_owners(channel_id),
        'all_members': data_channel_members(channel_id),
    }

def channel_messages(token, channel_id, start):
    check_valid_token(token)
    check_valid_channel(channel_id)
    u_id = auth_u_id_from_token(token)
    check_member_exist(u_id, channel_id)
    check_valid_message_start(start, channel_id)
    end = data_channel_messages_end(start, channel_id)
    message_list = data_channel_messages(channel_id, start, end)
    
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


