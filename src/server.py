import sys
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from error import InputError
from auth import auth_login, auth_logout, auth_register, auth_passwordreset_request, \
    auth_passwordreset_reset
from channels import channels_list, channels_listall, channels_create
from channel import channel_invite, channel_details, channel_messages, channel_leave, \
    channel_join, channel_addowner, channel_removeowner
from message import message_send, message_remove, message_edit, message_pin, message_unpin, \
    message_react, message_unreact, message_sendlater
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle, user_profile_uploadphoto
from other import clear, users_all, admin_userpermission_change, search, standup_active, \
    standup_send, standup_start

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

@APP.route('/auth/passwordreset/request', methods=['POST'])
def server_passwordreset_request():
    data = request.get_json()
    return dumps(auth_passwordreset_request(data['email']))

@APP.route('/auth/passwordreset/reset', methods=['POST'])
def server_passwordreset_reset():
    data = request.get_json()
    return dumps(auth_passwordreset_reset(data['reset_code'], data['new_password']))

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
    result = channel_details(request.args.get('token'), int(request.args.get('channel_id')))
    for member in result['all_members']:
        member['profile_img_url'] = str(request.url_root) + member['profile_img_url']
        print(member['profile_img_url'])
    for owner in result['owner_members']:
        owner['profile_img_url'] = str(request.url_root) + owner['profile_img_url']
        print(owner['profile_img_url'])
    return dumps(result)

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
    result = user_profile(request.args.get('token'), int(request.args.get('u_id')))
    result['user']['profile_img_url'] = str(request.url_root) + result['user']['profile_img_url']
    return dumps(result)

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
    return dumps(user_profile_uploadphoto(data['token'], data['img_url'], int(data['x_start']), int(data['y_start']), int(data['x_end']), int(data['y_end'])))

@APP.route('/static/<path:path>', methods=['GET'])
def server_profile_uploadphoto_serve_photo(path):
    return send_from_directory('/static', path)

@APP.route('/users/all', methods=['GET'])
def server_all():
    result = users_all(request.args.get('token'))
    for user in result['users']:
        user['profile_img_url'] = str(request.base_url) + user['profile_img_url']
    return dumps(result)

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

@APP.route('/message/pin', methods=['POST'])
def server_pin():
    data = request.get_json()
    return dumps(message_pin(data['token'], int(data['message_id'])))

@APP.route('/message/unpin', methods=['POST'])
def server_unpin():
    data = request.get_json()
    return dumps(message_unpin(data['token'], int(data['message_id'])))

@APP.route('/message/react', methods=['POST'])
def server_react():
    data = request.get_json()
    return dumps(message_react(data['token'], int(data['message_id']), int(data['react_id'])))

@APP.route('/message/unreact', methods=['POST'])
def server_unreact():
    data = request.get_json()
    return dumps(message_unreact(data['token'], int(data['message_id']), int(data['react_id'])))

@APP.route('/message/sendlater', methods=['POST'])
def server_sendlater():
    data = request.get_json()
    return dumps(message_sendlater(data['token'], int(data['channel_id']), data['message'], \
        int(data['time_sent'])))

@APP.route('/standup/start', methods=['POST'])
def server_start_standup():
    data = request.get_json()
    return dumps(standup_start(data['token'], int(data['channel_id']), data['length']))

@APP.route('/standup/active', methods=['GET'])
def server_active_standup():
    return dumps(standup_active(request.args.get('token'), int(request.args.get('channel_id'))))

@APP.route('/standup/send', methods=['POST'])
def server_send_standup():
    data = request.get_json()
    return dumps(standup_send(data['token'], int(data['channel_id']), data['message']))

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
