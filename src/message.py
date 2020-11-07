from error import InputError
from error import AccessError
from database import *
from utility import *
from auth import *
from database import data


def message_send(token, channel_id, message):
    check_valid_token(token)
    u_id = auth_u_id_from_token(token)
    check_authorised_member_channel(channel_id, u_id)
    check_valid_message_length(message)
    return {
        'message_id': data_message_send(channel_id, u_id, message),
    }

def message_remove(token, message_id):
    check_valid_token(token)
    u_id = auth_u_id_from_token(token)
    channel_id = data_get_channel_id(message_id)
    check_authorised_member_message(u_id, channel_id, message_id)
    data_message_remove(channel_id, message_id)

def message_edit(token, message_id, message):
    check_valid_token(token)
    u_id = auth_u_id_from_token(token)
    channel_id = data_get_channel_id(message_id)
    check_authorised_member_message(u_id, channel_id, message_id)
    data_message_edit(channel_id, message_id, message)
    
def message_pin(token, message_id):
    check_valid_token(token)
    u_id = auth_u_id_from_token(token)
    channel_id = data_get_channel_id(message_id)
    check_authorised_member_channel(channel_id, u_id)
    if not is_owner_exist(u_id, channel_id):
        check_global_owner(u_id)
    check_message_pinned(message_id, channel_id)
