from error import InputError
from error import AccessError
from database import *
from utility import *
from auth import *
from database import data
import threading
import time


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
    channel_id = prior_check_pin_unpin(token, message_id)
    check_message_pinned(message_id, channel_id)

def message_unpin(token, message_id):
    channel_id = prior_check_pin_unpin(token, message_id)
    check_message_unpinned(message_id, channel_id)

def prior_check_pin_unpin(token, message_id):
    check_valid_token(token)
    u_id = auth_u_id_from_token(token)
    channel_id = data_get_channel_id(message_id)
    check_authorised_member_channel(channel_id, u_id)
    if not is_owner_exist(u_id, channel_id):
        check_global_owner(u_id)
    return channel_id
    
def message_react(token, message_id, react_id):
    channel_id = prior_check_react_unreact(token, message_id, react_id)
    u_id = auth_u_id_from_token(token)
    check_message_reacted(message_id, channel_id, react_id, u_id)

def message_unreact(token, message_id, react_id):
    channel_id = prior_check_react_unreact(token, message_id, react_id)
    u_id = auth_u_id_from_token(token)
    check_message_unreacted(message_id, channel_id, react_id, u_id)
    
def prior_check_react_unreact(token, message_id, react_id):
    check_valid_token(token)
    u_id = auth_u_id_from_token(token)
    channel_id = data_get_channel_id(message_id)
    check_authorised_member_channel(channel_id, u_id)
    check_valid_react_id(react_id)
    return channel_id

def message_sendlater(token, channel_id, message, time_sent):
    check_valid_token(token)
    u_id = auth_u_id_from_token(token)
    check_valid_channel(channel_id)
    check_authorised_member_channel(channel_id, u_id)
    check_valid_message_length(message)
    time_diff = check_time_diff(time_sent)
    t = threading.Timer(time_diff, data_message_send(channel_id, u_id, message))
    t.start()