import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
from error import InputError

# Use this fixture to get the URL of the server. 
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

def test_echo(url):
    '''
    A simple test to check echo
    '''
    resp = requests.get(url + 'echo', params={'data': 'hey'})
    assert json.loads(resp.text) == {'data': 'hey'}

def test_server_channel(url):
    requests.delete(f"{url}/clear")
    # test_channel_invite_success
    FirstUser = {
        'email': "leonwu@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Yilang",
        'name_last': "Wu",
    }
    r = requests.post(f"{url}/auth/register", json=FirstUser)
    return_data = r.json()
    token1 = return_data['token']

    requests.post(f"{url}/channels/create", json={'token': token1, 'name': 'first', 'is_public': True})
    
    SecondUser = {
        'email': "dennislin@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Dennis",
        'name_last': "Lin",
    }
    r = requests.post(f"{url}/auth/register", json=SecondUser)
    return_data = r.json()
    token2 = return_data['token']

    # test_channel_join_successful
    requests.post(f"{url}/channel/join", json={'token': token2, 'channel_id': 0})
    r = requests.get(f"{url}/channel/details", params={'token': token2, 'channel_id': 0})
    return_data = r.json()
    assert len(return_data['all_members']) == 2

    # test_channel_join_channel_already_joined
    r = requests.post(f"{url}/channel/join", json={'token': token2, 'channel_id': 0})
    return_data = r.json()
    assert return_data['message'] == '<p>Member already exists</p>'

    # test_channel_join_is_private
    requests.post(f"{url}/channels/create", json={'token': token1, 'name': 'second', 'is_public': False})
    r = requests.post(f"{url}/channel/join", json={'token': token2, 'channel_id': 1})
    return_data = r.json()
    assert return_data['message'] == '<p>Channel is private</p>'

    # test_channel_leave_successful
    requests.post(f"{url}/channel/leave", json={'token': token2, 'channel_id': 0})
    r = requests.get(f"{url}/channel/details", params={'token': token1, 'channel_id': 0})
    return_data = r.json()
    assert len(return_data['all_members']) == 1

    # test_channel_leave_unauthorised
    r = requests.post(f"{url}/channel/leave", json={'token': token2, 'channel_id': 1})
    return_data = r.json()
    assert return_data['message'] == '<p>Invalid token</p>'

    # test_channel_leave_invalid_channel
    r = requests.post(f"{url}/channel/leave", json={'token': token1, 'channel_id': 2})
    return_data = r.json()
    assert return_data['message'] == '<p>Channel_id is invalid</p>'

    # test_channel_invite_success

    ThirdUser = {
        'email': "guanbin@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Guanbin",
        'name_last': "Wen",
    }
    r = requests.post(f"{url}/auth/register", json=ThirdUser)
    return_data = r.json()
    token3 = return_data['token']
    u_id3 = return_data['u_id']

    requests.post(f"{url}/channel/invite", json={'token': token1, 'channel_id': 0, 'u_id': u_id3})
    r = requests.get(f"{url}/channel/details", params={'token': token1, 'channel_id': 0})
    return_data = r.json()
    assert len(return_data['all_members']) == 2

    # test_channel_invite_invalid_user
    r = requests.post(f"{url}/channel/invite", json={'token': token1, 'channel_id': 0, 'u_id': 100})
    return_data = r.json()
    assert return_data['message'] == '<p>User is invalid</p>'

    # test_channel_invite_unauthorised
    r = requests.post(f"{url}/channel/invite", json={'token': token3, 'channel_id': 1, 'u_id': 2})
    return_data = r.json()
    assert return_data['message'] == '<p>Member does not exist</p>'

    # check member correctness
    r = requests.get(f"{url}/channel/details", params={'token': token1, 'channel_id': 0})
    return_data = r.json()
    assert return_data['all_members'] == [{'name_first': 'Yilang', 'name_last': 'Wu', 'u_id': 0}, 
    {'name_first': 'Guanbin', 'name_last': 'Wen', 'u_id': 2}]

    # test_channel_invite_user_already_joined
    r = requests.post(f"{url}/channel/invite", json={'token': token1, 'channel_id': 0, 'u_id': 0})
    return_data = r.json()
    assert return_data['message'] == '<p>Member already exists</p>'

    # test_channel_invite_invalid_channel
    r = requests.post(f"{url}/channel/invite", json={'token': token1, 'channel_id': 4, 'u_id': 1})
    return_data = r.json()
    assert return_data['message'] == '<p>Channel is invalid</p>'