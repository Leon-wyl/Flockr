from database import *
from utility import *
from auth import auth_u_id_from_token


# Resets the internal data of the application to it's initial state
def clear():
    data_clear()

# Returns a list of all users and their associated details
def users_all(token):
    check_valid_token(token)
    return {
        'users': data_users_list()
    }

# Given a User by their user ID, set their permissions
# to new permissions described by permission_id
def admin_userpermission_change(token, u_id, permission_id):
    check_valid_token(token)
    check_valid_user(u_id)
    check_valid_permission_id(permission_id)
    token_id = auth_u_id_from_token(token)
    check_global_owner(token_id)
    data_change_permission(u_id, permission_id)

# Given a query string, return a collection of messages in all of the
# channels that the user has joined that match the query
def search(token, query_str):
    check_valid_token(token)
    token_id = auth_u_id_from_token(token)
    return {
        'messages': data_search_message(query_str, token_id),
    }

def standup_start(token, channel_id, length):
    check_valid_token(token)
    check_valid_channel(channel_id)
    check_standup_not_active(channel_id)
    u_id = auth_u_id_from_token(token)
    time = data_standup_start(u_id, channel_id, length)
    return {
        'time_finish': time
    }


def standup_active(token, channel_id):
    check_valid_token(token)
    check_valid_channel(channel_id)
    return data_standup_status(channel_id)

def standup_send(token, channel_id, message):
    check_valid_token(token)
    check_valid_channel(channel_id)
    check_valid_message_length(message)
    check_standup_active(channel_id)
    u_id = auth_u_id_from_token(token)
    check_authorised_member(u_id, channel_id)
    data_message_buffer(u_id, message, channel_id)
    return {}

