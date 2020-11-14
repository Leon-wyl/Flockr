import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
from database import *
from utility import token_generate
from error import InputError

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

def test_integration(url):
    # Clear
    requests.delete(f"{url}/clear")
    # Normal register
    dataIn1 = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
        'name_first': "Yilang",
        'name_last': "W",
    }
    r = requests.post(f"{url}/auth/register", json=dataIn1)
    return_data = r.json()
    assert return_data['u_id'] == 0
    assert return_data['token'] == token_generate(return_data['u_id'])
    # Logout the user
    dataIn2 = {
        'token': return_data['token']
    }
    r = requests.post(f"{url}/auth/logout", json=dataIn2)
    return_data = r.json()
    assert return_data['is_success'] == True
    # Login this user
    dataIn3 = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
    }
    r = requests.post(f"{url}/auth/login", json=dataIn3)
    return_data = r.json()
    assert return_data['u_id'] == 0
    assert return_data['token'] == token_generate(return_data['u_id'])
    # Create a channel
    resp = requests.post(f"{url}/channels/create", \
        json={'token': return_data['token'], 'name': 'first', 'is_public': True})
    assert resp.json() == {'channel_id' : 0}
    resp = requests.post(f"{url}/channels/create", \
        json={'token': return_data['token'], 'name': 'second', 'is_public': True})
    assert resp.json() == {'channel_id' : 1}
    # List all channels of authorised user
    resp = requests.get(f"{url}/channels/list", params={'token': return_data['token']})
    resp = resp.json()
    assert resp['channels'] == [{'channel_id': 0, 'name': 'first'}, {'channel_id': 1, 'name': 'second'}]
    # Provide a list of all channels
    resp = requests.get(f"{url}/channels/listall", params={'token': return_data['token']})
    resp = resp.json()
    assert resp['channels'] == [{'channel_id': 0, 'name': 'first'}, {'channel_id': 1, 'name': 'second'}]
    # Register another user
    info = requests.post(f"{url}/auth/register", \
        json={'email': "eviedunstone@gmail.com", 'password': 'Qwerty6', 'name_first': 'Evie', 'name_last': 'Dunstone'})
    info = info.json()
    # Join the channel
    requests.post(f"{url}/channel/join", \
        json={'token': info['token'], 'channel_id': 0})
    # Add owner
    requests.post(f"{url}/channel/addowner", \
        json={'token': return_data['token'], 'channel_id': 0, 'u_id': 1})
    # Remove owner
    requests.post(f"{url}/channel/removeowner", \
        json={'token': return_data['token'], 'channel_id': 0, 'u_id': 1})
    # Leave channel
    requests.post(f"{url}/channel/leave", \
        json={'token': info['token'], 'channel_id': 0})
    # Invite new member to channel
    requests.post(f"{url}/channel/invite", \
        json={'token': return_data['token'], 'channel_id': 0, 'u_id': 1})

    # Returns a list of all users and their associated details
    resp = requests.get(f"{url}/users/all", params={'token': info['token']})
    resp = resp.json()
    assert resp == {'users': [
        {
            'u_id': 0,
            'email': "leonwu@gmail.com",
            'name_first': "Yilang",
            'name_last': "W",
            'handle_str': 'yilangw',
            'profile_img_url': resp['users'][0]['profile_img_url']
         },
         {
            'u_id': 1,
            'email': "eviedunstone@gmail.com",
            'name_first': "Evie",
            'name_last': "Dunstone",
            'handle_str': 'eviedunstone',
            'profile_img_url': resp['users'][1]['profile_img_url']
         }

    ]}
    # Permission change
    requests.post(f"{url}/admin/userpermission/change", \
        json={'token': return_data['token'], 'u_id': 1, 'permission_id': 1})

    # User profile
    resp = requests.get(f"{url}/user/profile", \
        params={'token': return_data['token'], 'u_id': 1})
    resp = resp.json()
    assert resp == {'user':
        {
            'u_id': 1,
            'email': "eviedunstone@gmail.com",
            'name_first': "Evie",
            'name_last': "Dunstone",
            'handle_str': 'eviedunstone',
            'profile_img_url': resp['user']['profile_img_url']
         }
    }
    # Set name to user_profile
    requests.put(f"{url}/user/profile/setname", \
        json={'token': return_data['token'], 'name_first': 'Yilang', 'name_last': "W"})
    # Set email to user_profile
    requests.put(f"{url}/user/profile/setemail", \
        json={'token': return_data['token'], 'email': 'leonwu@gmail.com'})
    # Set handle to user_profile
    requests.put(f"{url}/user/profile/sethandle", \
        json={'token': return_data['token'], 'handle_str': 'yilangw'})
    # Send message
    resp = requests.post(f"{url}/message/send", \
        json={'token': return_data['token'], 'channel_id': 0, 'message': 'areyouok'})
    resp = resp.json()
    assert resp == {'message_id': 0}
    # Send message
    resp = requests.post(f"{url}/message/send", \
        json={'token': return_data['token'], 'channel_id': 0, 'message': 'I am okey'})
    resp = resp.json()
    assert resp == {'message_id': 1}
    # Send message
    resp = requests.post(f"{url}/message/send", \
        json={'token': return_data['token'], 'channel_id': 0, 'message': 'adsfadfk'})
    resp = resp.json()
    assert resp == {'message_id': 2}
    # Edit message
    requests.put(f"{url}/message/edit", \
        json={'token': return_data['token'], 'message_id': 2, 'message': 'jjjjjjj'})
    # Delete message
    requests.delete(f"{url}/message/remove", \
        json={'token': return_data['token'], 'message_id': 2})
    # Delete message
    requests.delete(f"{url}/message/remove", \
        json={'token': return_data['token'], 'message_id': 1})
    # Leave channel
    requests.post(f"{url}/channel/leave", \
        json={'token': info['token'], 'channel_id': 0})
    # Message search
    resp = requests.get(f"{url}/search", params={'token': return_data['token'], 'query_str': 'ok'})
    resp = resp.json()
    assert resp == {'messages': [
        {
            'message_id': 0,
            'u_id': 0,
            'message': "areyouok",
            'time_created': 0,
        }

    ]}

    # Channel message
    resp = requests.get(f"{url}/channel/messages", \
        params={'token': return_data['token'], 'channel_id': 0, 'start': 0})
    resp = resp.json()
    assert resp == {
        'messages':
            [{
            'message_id': 0,
            'u_id': 0,
            'message': "areyouok",
            'time_created': 0,
            'reacts': [],
            'is_pinned': False,
        }],
        'start': 0,
        'end': -1,
    }
    # Channel details
    resp = requests.get(f"{url}/channel/details", \
        params={'token': return_data['token'], 'channel_id': 0})
    resp = resp.json()
    assert resp == {
        'name': 'first',
        'owner_members':[
            {
                'u_id': 0,
                'name_first': 'Yilang',
                'name_last': 'W',
                'profile_img_url': resp['owner_members'][0]['profile_img_url']
            }
        ],
        'all_members': [
            {
                'u_id': 0,
                'name_first': 'Yilang',
                'name_last': 'W',
                'profile_img_url': resp['all_members'][0]['profile_img_url']
            }
        ]
    }

