import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from auth import auth_login, auth_logout, auth_register
from channels import channels_list, channels_listall, channels_create
from channel import channel_invite, channel_details, channel_messages, channel_leave, \
    channel_join, channel_addowner, channel_removeowner
from message import message_send, message_remove, message_edit
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle
from other import clear, users_all, admin_userpermission_change, search

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route('/auth/login', methods=['POST'])
def server_login():
    data = request.get_json()
    if 'email' in data and 'password' in data:
        return dumps(auth_login(data['email'], data['password']))
    raise InputError(description='invalid input')

@APP.route('/auth/logout', methods=['POST'])
def server_logout():
    data = request.get_json()
    return dumps(auth_logout(data['token']))

@APP.route('/auth/register', methods=['POST'])
def server_register():
    data = request.get_json()
    return dumps(auth_register(data['email'], data['password'], data['name_first'], \
        data['name_last']))

@APP.route('/channels/list', methods=['GET'])
def server_list():
    return dumps(channels_list(request.args.get('token')))

@APP.route('/channels/listall', methods=['GET'])
def server_listall():
    return dumps(channels_listall(request.args.get('token')))

@APP.route('/channels/create', methods=['POST'])
def server_create():
    data = request.get_json()
    return dumps(channels_create(data['token'], data['name'], data['is_public']))

@APP.route('/channel/invite', methods=['POST'])
def server_invite():
    data = request.get_json()
    return dumps(channel_invite(data['token'], int(data['channel_id']), int(data['u_id'])))

@APP.route('/channel/details', methods=['GET'])
def server_details():
    return dumps(channel_details(request.args.get('token'), int(request.args.get('channel_id'))))

@APP.route('/channel/messages', methods=['GET'])
def server_message():
    return dumps(channel_messages(request.args.get('token'), int(request.args.get('channel_id')), \
        int(request.args.get('start'))))

@APP.route('/channel/leave', methods=['POST'])
def server_leave():
    data = request.get_json()
    return dumps(channel_leave(data['token'], int(data['channel_id'])))

@APP.route('/channel/join', methods=['POST'])
def server_join():
    data = request.get_json()
    return dumps(channel_join(data['token'], int(data['channel_id'])))

@APP.route('/channel/addowner', methods=['POST'])
def server_addowner():
    data = request.get_json()
    return dumps(channel_addowner(data['token'], int(data['channel_id']), int(data['u_id'])))

@APP.route('/channel/removeowner', methods=['POST'])
def server_removeowner():
    data = request.get_json()
    return dumps(channel_removeowner(data['token'], int(data['channel_id']), int(data['u_id'])))

@APP.route('/message/send', methods=['POST'])
def server_send():
    data = request.get_json()
    return dumps(message_send(data['token'],int(data['channel_id']), data['message']))

@APP.route('/message/remove', methods=['DELETE'])
def server_remove():
    data = request.get_json()
    return dumps(message_remove(data['token'], int(data['message_id'])))

@APP.route('/message/edit', methods=['PUT'])
def server_edit():
    data = request.get_json()
    return dumps(message_edit(data['token'], int(data['message_id']), data['message']))

@APP.route('/user/profile', methods=['GET'])
def server_profile():
    return dumps(user_profile(request.args.get('token'), int(request.args.get('u_id'))))

@APP.route('/user/profile/setname', methods=['PUT'])
def server_profile_setname():
    data = request.get_json()
    return dumps(user_profile_setname(data['token'], data['name_first'], data['name_last']))

@APP.route('/user/profile/setemail', methods=['PUT'])
def server_profile_setemail():
    data = request.get_json()
    return dumps(user_profile_setemail(data['token'], data['email']))

@APP.route('/user/profile/sethandle', methods=['PUT'])
def server_profile_sethandle():
    data = request.get_json()
    return dumps(user_profile_sethandle(data['token'], data['handle_str']))

@APP.route('/user/profile/uploadphoto', methods=['POST'])
def server_profile_uploadphoto():
    data = request.get_json()
    return dumps(user_profile_uploadphoto(data['token'], data['img_url'], data['x_start'], data['y_start'], data['x_end'], data['y_end'])))

@APP.route('/users/all', methods=['GET'])
def server_all():
    return dumps(users_all(request.args.get('token')))

@APP.route('/admin/userpermission/change', methods=['POST'])
def server_userpermission_change():
    data = request.get_json()
    return dumps(admin_userpermission_change(data['token'], int(data['u_id']), int(data['permission_id'])))

@APP.route('/search', methods=['GET'])
def server_search():
    return dumps(search(request.args.get('token'), request.args.get('query_str')))

@APP.route('/clear', methods=['DELETE'])
def server_clear():
    return dumps(clear())

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
