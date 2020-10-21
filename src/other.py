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
