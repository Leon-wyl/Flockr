import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
from other import clear
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

def test_echo(url):
    '''
    A simple test to check echo
    '''
    resp = requests.get(url + 'echo', params={'data': 'hello'})
    assert json.loads(resp.text) == {'data': 'hello'}

def test_server_message_react(url):

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

    # Message sent by the first user
    dataIn4 = {
        'token': return_data1['token'],
        'channel_id': 0,
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=dataIn4)

    # The first user tries to react to a message with invalid message_id
    dataIn5 = {
        'token': return_data1['token'],
        'message_id': 5,
        'react_id': 1,
    }
    r = requests.post(f"{url}/message/react", json=dataIn5)
    return_data5 = r.json()
    assert return_data5['code'] == 400
    
    # The first user tries to react to a message with invalid react_id
    dataIn20 = {
        'token': return_data1['token'],
        'message_id': 0,
        'react_id': 5,
    }
    r = requests.post(f"{url}/message/react", json=dataIn20)
    return_data20 = r.json()
    assert return_data20['code'] == 400

    # The second user tries to react to the message
    # created by the first user, which is invalid
    dataIn6 = {
        'token': return_data2['token'],
        'message_id': 0,
        'react_id': 1,
    }
    r = requests.post(f"{url}/message/react", json=dataIn6)
    return_data6 = r.json()
    assert return_data6['code'] == 400

    # The second user join the channel
    dataIn8 = {
        'token': return_data2['token'],
        'channel_id': 0,
    }
    r = requests.post(f"{url}/channel/join", json=dataIn8)

    # The first user reacts to the message 
    dataIn11 = {
        'token': return_data1['token'],
        'message_id': 0,
        'react_id': 1,
    }
    r = requests.post(f"{url}/message/react", json=dataIn11)
    

    # The second user reacts to the message 
    dataIn12 = {
        'token': return_data2['token'],
        'message_id': 0,
        'react_id': 1,
    }
    r = requests.post(f"{url}/message/react", json=dataIn12)

    # The second user reacts to the same message again, which is invalid
    dataIn13 = {
        'token': return_data2['token'],
        'message_id': 0,
        'react_id': 1,
    }
    r = requests.post(f"{url}/message/react", json=dataIn13)
    return_data13 = r.json()
    assert return_data13['code'] == 400
    
def test_server_message_unreact(url):

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

    # Message sent by the first user
    dataIn4 = {
        'token': return_data1['token'],
        'channel_id': 0,
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=dataIn4)

    # The first user tries to unreact to a message with invalid message_id
    dataIn5 = {
        'token': return_data1['token'],
        'message_id': 5,
        'react_id': 1,
    }
    r = requests.post(f"{url}/message/unreact", json=dataIn5)
    return_data5 = r.json()
    assert return_data5['code'] == 400
    
    # The first user tries to unreact to a message with invalid react_id
    dataIn20 = {
        'token': return_data1['token'],
        'message_id': 0,
        'react_id': 5,
    }
    r = requests.post(f"{url}/message/unreact", json=dataIn20)
    return_data20 = r.json()
    assert return_data20['code'] == 400

    # The second user tries to unreact to the message
    # created by the first user, which is invalid
    dataIn6 = {
        'token': return_data2['token'],
        'message_id': 0,
        'react_id': 1,
    }
    r = requests.post(f"{url}/message/unreact", json=dataIn6)
    return_data6 = r.json()
    assert return_data6['code'] == 400

    # The second user join the channel
    dataIn8 = {
        'token': return_data2['token'],
        'channel_id': 0,
    }
    r = requests.post(f"{url}/channel/join", json=dataIn8)

    # The first user reacts to the message 
    dataIn11 = {
        'token': return_data1['token'],
        'message_id': 0,
        'react_id': 1,
    }
    r = requests.post(f"{url}/message/react", json=dataIn11)
    

    # The second user reacts to the message 
    dataIn12 = {
        'token': return_data2['token'],
        'message_id': 0,
        'react_id': 1,
    }
    r = requests.post(f"{url}/message/react", json=dataIn12)
    
    # The second user unreacts to the message, then unreacts the same mesage again, which is invalid
    dataIn22 = {
        'token': return_data2['token'],
        'message_id': 0,
        'react_id': 1,
    }
    r = requests.post(f"{url}/message/unreact", json=dataIn22)
    '''
    r = requests.post(f"{url}/message/unreact", json=dataIn22)
    return_data22 = r.json()
    assert return_data22['code'] == 400
    '''
