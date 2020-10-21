from database import *

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
    pass



# Given a query string, return a collection of messages in all of the 
# channels that the user has joined that match the query
def search(token, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
