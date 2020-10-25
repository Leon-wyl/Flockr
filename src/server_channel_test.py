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

def test_server_channel_details(url):

    # Register a user
    dataIn1 = {
        'email': "leonwu@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Yilang",
        'name_last': "Wu",
    }
    r = requests.post(f"{url}/auth/register", json=dataIn1)
    return_data1 = r.json()

    # Register another user
    dataIn2 = {
        'email': "billgates@outlook.com",
        'password': "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates",
    }
    r = requests.post(f"{url}/auth/register", json=dataIn2)
    return_data2 = r.json()

    # Channel created by the first user
    dataIn3 = {
        'token': return_data1['token'],
        'name': "group1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=dataIn3)
    return_data3 = r.json()
    
    # The first user tries to get the channel details from an invalid channel
    dataIn4 = {
        'token': return_data1['token'],
        'channel_id': 4,
    }
    r = requests.get(f"{url}/channel/details", params=dataIn4)
    return_data4 = r.json()
    assert return_data4['code'] == 400

    # The second user tries to get the channel details of the channel created by the first user, which is unauthorised    
    dataIn5 = {
        'token': return_data2['token'],
        'channel_id': 0,
    }
    r = requests.get(f"{url}/channel/details", params=dataIn5)
    return_data5 = r.json()
    assert return_data5['code'] == 400
    
    # The second user join the channel
    dataIn6 = {
        'token': return_data2['token'],
        'channel_id': 0,
    }
    r = requests.post(f"{url}/channel/join", json=dataIn6)
    
    resp = requests.get(f"{url}/channel/details", params=dataIn6) 
    resp = resp.json()
    assert resp == {'all_members': [{'name_first': 'Yilang', 'name_last': 'Wu', 'u_id': 0}, {'name_first': 'Bill', 'name_last': 'Gates', 'u_id': 1}], 'name': 'group1', 'owner_members': [{'name_first': 'Yilang', 'name_last': 'Wu', 'u_id': 0}]}

def test_server_channel_messages(url):

    # Register a user
    dataIn1 = {
        'email': "leonwu@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Yilang",
        'name_last': "Wu",
    }
    r = requests.post(f"{url}/auth/register", json=dataIn1)
    return_data1 = r.json()

    # Register another user
    dataIn2 = {
        'email': "billgates@outlook.com",
        'password': "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates",
    }
    r = requests.post(f"{url}/auth/register", json=dataIn2)
    return_data2 = r.json()

    # Channel created by the first user
    dataIn3 = {
        'token': return_data1['token'],
        'name': "group1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=dataIn3)
    return_data3 = r.json()
    
    # Message sent by the first user
    dataIn4 = {
        'token': return_data1['token'],
        'channel_id': 0,
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=dataIn4)
    return_data4 = r.json()

    # The first user tries to get the channel messages from an invalid channel
    dataIn5 = {
        'token': return_data1['token'],
        'channel_id': 5,
        'start': 0
    }
    r = requests.get(f"{url}/channel/messages", params=dataIn5)
    return_data5 = r.json()
    assert return_data5['code'] == 400
    
    # The first user tries to get the channel messages from channel with an invalid start
    dataIn6 = {
        'token': return_data1['token'],
        'channel_id': 0,
        'start': 10
    }
    r = requests.get(f"{url}/channel/messages", params=dataIn6)
    return_data6 = r.json()
    assert return_data6['code'] == 400

    # The second user tries to get the channel messages of the channel created by the first user, which is unauthorised    
    dataIn7 = {
        'token': return_data2['token'],
        'channel_id': 0,
    }
    r = requests.get(f"{url}/channel/details", params=dataIn7)
    return_data7 = r.json()
    assert return_data7['code'] == 400   
    
    # The second user join the channel
    dataIn8 = {
        'token': return_data2['token'],
        'channel_id': 0,
    }
    r = requests.post(f"{url}/channel/join", json=dataIn8)
    
    # Message sent by the second user
    dataIn9 = {
        'token': return_data2['token'],
        'channel_id': 0,
        'message': "Hey there first",
    }
    r = requests.post(f"{url}/message/send", json=dataIn9)
    return_data9 = r.json()
    
    dataIn10 = {
        'token': return_data1['token'],
        'channel_id': 0,
        'start': 0
    }
    
    resp = requests.get(f"{url}/channel/messages", params=dataIn10) 
    resp = resp.json()
    assert resp == {'end': -1, 'message_list': [{'message': 'Hello', 'message_id': 0, 'time_created': 0, 'u_id': 0}, {'message': 'Hey there first', 'message_id': 1, 'time_created': 0, 'u_id': 1}], 'start': 0}    
    