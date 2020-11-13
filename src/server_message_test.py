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

def test_server_message_send(url):

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

    # Message of invalid length sent by the first user, which was invalid
    dataIn4 = {
        'token': return_data1['token'],
        'channel_id': 0,
        'message': "H" * 1500,
    }
    r = requests.post(f"{url}/message/send", json=dataIn4)
    return_data4 = r.json()
    assert return_data4['code'] == 400

    # The second user tries to send message to the channel created by
    # the first user without joining, which is unauthorised
    dataIn5 = {
        'token': return_data2['token'],
        'channel_id': 0,
        'message': "Let me in!",
    }
    r = requests.post(f"{url}/message/send", json=dataIn5)
    assert return_data4['code'] == 400

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
    assert return_data9 == {'message_id': 0}

    # Message sent by the first user
    dataIn10 = {
        'token': return_data1['token'],
        'channel_id': 0,
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=dataIn10)
    return_data10 = r.json()
    assert return_data10 == {'message_id': 1}

def test_server_message_remove(url):

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

    # The first user tries to remove a message with invalid message_id
    dataIn5 = {
        'token': return_data1['token'],
        'message_id': 5,
    }
    r = requests.delete(f"{url}/message/remove", json=dataIn5)
    return_data5 = r.json()
    assert return_data5['code'] == 400

    # The second user tries to get the channel messages of the channel
    # created by the first user, which is unauthorised
    dataIn6 = {
        'token': return_data2['token'],
        'message_id': 0,
    }
    r = requests.delete(f"{url}/message/remove", json=dataIn6)
    return_data6 = r.json()
    assert return_data6['code'] == 400

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

    # Another message sent by the second user
    dataIn10 = {
        'token': return_data2['token'],
        'channel_id': 0,
        'message': "Notice me",
    }
    r = requests.post(f"{url}/message/send", json=dataIn10)

    # The first user remove a message as owner
    dataIn11 = {
        'token': return_data1['token'],
        'message_id': 1,
    }
    r = requests.delete(f"{url}/message/remove", json=dataIn11)

    # The second user remove a message as the authorised member making the request
    dataIn12 = {
        'token': return_data2['token'],
        'message_id': 2,
    }
    r = requests.delete(f"{url}/message/remove", json=dataIn12)

    # The first user remove a message as the authorised member making
    # the request, and remove the same message again, which is invalid
    dataIn13 = {
        'token': return_data1['token'],
        'message_id': 0,
    }
    r = requests.delete(f"{url}/message/remove", json=dataIn13)
    r = requests.delete(f"{url}/message/remove", json=dataIn13)
    return_data15 = r.json()
    assert return_data15['code'] == 400

def test_server_message_edit(url):

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

    # The second user tries to edit the channel messages sent by first
    # user in the channel created by the first user, which is unauthorised
    dataIn6 = {
        'token': return_data2['token'],
        'message_id': 0,
        'message': 'ohayo',
    }
    r = requests.put(f"{url}/message/edit", json=dataIn6)
    return_data6 = r.json()
    assert return_data6['code'] == 400

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

    # Another message sent by the second user
    dataIn10 = {
        'token': return_data2['token'],
        'channel_id': 0,
        'message': "Notice me",
    }
    r = requests.post(f"{url}/message/send", json=dataIn10)

    # The first user edits a message as owner
    dataIn11 = {
        'token': return_data1['token'],
        'message_id': 1,
        'message': 'Changed2nd'
    }
    r = requests.put(f"{url}/message/edit", json=dataIn11)

    # The second user edits a message as the authorised member making the request
    dataIn12 = {
        'token': return_data2['token'],
        'message_id': 2,
        'message': 'Changed3nd'
    }
    r = requests.put(f"{url}/message/edit", json=dataIn12)

    # The first user edits a message as the authorised member making
    # the request, with the new message being empty
    dataIn13 = {
        'token': return_data1['token'],
        'message_id': 0,
        'message': ''
    }
    r = requests.put(f"{url}/message/edit", json=dataIn13)
