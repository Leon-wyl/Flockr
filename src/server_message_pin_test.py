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

def test_message_pin_valid0(url):
    '''Owner of the channel pin the message sent by a member'''
    clear()

    # Register user 0
    user0_data_input = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
        'name_first': "Yilang",
        'name_last': "W",
    }
    r = requests.post(f"{url}/auth/register", json=user0_data_input)
    user0_data_output = r.json()

    # Register user 1
    user1_data_input = {
        'email': "billgates@outlook.com",
        'password':  "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates"
    }
    r = requests.post(f"{url}/auth/register", json=user1_data_input)
    user1_data_output = r.json()

    # Register user 2
    user2_data_input = {
        'email': "johnson@icloud.com",
        'password': "RFVtgb45678",
        'name_first': "M",
        'name_last': "Johnson"
    }
    r = requests.post(f"{url}/auth/register", json=user2_data_input)
    user2_data_output = r.json()

    # User 0 create a channel
    channel0_data_input = {
        'token': user0_data_output['token'],
        'name': "channel0",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel0_data_input)
    channel0_data_output = r.json()

    # User 1 join the channel
    user1_join_data_input = {
        'token': user1_data_output['token'],
        'channel_id': channel0_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user1_join_data_input)

    # User 1 create another channel
    channel1_data_input = {
        'token': user1_data_output['token'],
        'name': "channel1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data_input)
    channel1_data_output = r.json()

    # user 2 join the channel created by user 1
    user2_join_data_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user2_join_data_input)

    # User 0 join channel1
    user0_join_data_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user0_join_data_input)

    # User 2 send a message
    user2_message_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=user2_message_input)
    user2_message_output = r.json()

    # User 1 send a message
    user1_message_input = {
        'token': user1_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hi",
    }
    r = requests.post(f"{url}/message/send", json=user1_message_input)

    # User 1 pin the message sent by user 2
    user1_pin_input = {
        'token': user1_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/pin", json=user1_pin_input)

    # User 0 get all channel messages
    user0_get_message_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'start': 0,
    }
    r = requests.get(f"{url}/channel/messages", params=user0_get_message_input)
    user0_get_message_output = r.json()
    assert user0_get_message_output['message_list'][0]['is_pinned'] == True


def test_message_pin_valid1(url):
    '''Owner of the flockr pin the message sent by a member'''
    clear()

    # Register user 0
    user0_data_input = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
        'name_first': "Yilang",
        'name_last': "W",
    }
    r = requests.post(f"{url}/auth/register", json=user0_data_input)
    user0_data_output = r.json()

    # Register user 1
    user1_data_input = {
        'email': "billgates@outlook.com",
        'password':  "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates"
    }
    r = requests.post(f"{url}/auth/register", json=user1_data_input)
    user1_data_output = r.json()

    # Register user 2
    user2_data_input = {
        'email': "johnson@icloud.com",
        'password': "RFVtgb45678",
        'name_first': "M",
        'name_last': "Johnson"
    }
    r = requests.post(f"{url}/auth/register", json=user2_data_input)
    user2_data_output = r.json()

    # User 0 create a channel
    channel0_data_input = {
        'token': user0_data_output['token'],
        'name': "channel0",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel0_data_input)
    channel0_data_output = r.json()

    # User 1 join the channel
    user1_join_data_input = {
        'token': user1_data_output['token'],
        'channel_id': channel0_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user1_join_data_input)

    # User 1 create another channel
    channel1_data_input = {
        'token': user1_data_output['token'],
        'name': "channel1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data_input)
    channel1_data_output = r.json()

    # user 2 join the channel created by user 1
    user2_join_data_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user2_join_data_input)

    # User 0 join channel1
    user0_join_data_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user0_join_data_input)

    # User 2 send a message
    user2_message_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=user2_message_input)
    user2_message_output = r.json()

    # User 1 send a message
    user1_message_input = {
        'token': user1_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hi",
    }
    r = requests.post(f"{url}/message/send", json=user1_message_input)

    # User 0 pin the message sent by user 2
    user0_pin_input = {
        'token': user0_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/pin", json=user0_pin_input)

    # User 0 get all channel messages
    user0_get_message_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'start': 0,
    }
    r = requests.get(f"{url}/channel/messages", params=user0_get_message_input)
    user0_get_message_output = r.json()
    assert user0_get_message_output['message_list'][0]['is_pinned'] == True

def test_message_pin_valid2(url):
    '''Owner of the flockr pin the message sent by a the owner of the channel'''
    clear()

    # Register user 0
    user0_data_input = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
        'name_first': "Yilang",
        'name_last': "W",
    }
    r = requests.post(f"{url}/auth/register", json=user0_data_input)
    user0_data_output = r.json()

    # Register user 1
    user1_data_input = {
        'email': "billgates@outlook.com",
        'password':  "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates"
    }
    r = requests.post(f"{url}/auth/register", json=user1_data_input)
    user1_data_output = r.json()

    # Register user 2
    user2_data_input = {
        'email': "johnson@icloud.com",
        'password': "RFVtgb45678",
        'name_first': "M",
        'name_last': "Johnson"
    }
    r = requests.post(f"{url}/auth/register", json=user2_data_input)
    user2_data_output = r.json()

    # User 0 create a channel
    channel0_data_input = {
        'token': user0_data_output['token'],
        'name': "channel0",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel0_data_input)
    channel0_data_output = r.json()

    # User 1 join the channel
    user1_join_data_input = {
        'token': user1_data_output['token'],
        'channel_id': channel0_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user1_join_data_input)

    # User 1 create another channel
    channel1_data_input = {
        'token': user1_data_output['token'],
        'name': "channel1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data_input)
    channel1_data_output = r.json()

    # user 2 join the channel created by user 1
    user2_join_data_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user2_join_data_input)

    # User 0 join channel1
    user0_join_data_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user0_join_data_input)

    # User 2 send a message
    user2_message_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=user2_message_input)

    # User 1 send a message
    user1_message_input = {
        'token': user1_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hi",
    }
    r = requests.post(f"{url}/message/send", json=user1_message_input)
    user1_message_output = r.json()

    # User 0 pin the message sent by user 1
    user0_pin_input = {
        'token': user0_data_output['token'],
        'message_id': user1_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/pin", json=user0_pin_input)

    # User 0 get all channel messages
    user0_get_message_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'start': 0,
    }
    r = requests.get(f"{url}/channel/messages", params=user0_get_message_input)
    user0_get_message_output = r.json()
    assert user0_get_message_output['message_list'][1]['is_pinned'] == True

def test_message_pin_valid3(url):
    '''Owner of the flockr pin the message sent by a the owner of the channel'''
    clear()

    # Register user 0
    user0_data_input = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
        'name_first': "Yilang",
        'name_last': "W",
    }
    r = requests.post(f"{url}/auth/register", json=user0_data_input)
    user0_data_output = r.json()

    # Register user 1
    user1_data_input = {
        'email': "billgates@outlook.com",
        'password':  "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates"
    }
    r = requests.post(f"{url}/auth/register", json=user1_data_input)
    user1_data_output = r.json()

    # Register user 2
    user2_data_input = {
        'email': "johnson@icloud.com",
        'password': "RFVtgb45678",
        'name_first': "M",
        'name_last': "Johnson"
    }
    r = requests.post(f"{url}/auth/register", json=user2_data_input)
    user2_data_output = r.json()

    # User 0 create a channel
    channel0_data_input = {
        'token': user0_data_output['token'],
        'name': "channel0",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel0_data_input)
    channel0_data_output = r.json()

    # User 1 join the channel
    user1_join_data_input = {
        'token': user1_data_output['token'],
        'channel_id': channel0_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user1_join_data_input)

    # User 1 create another channel
    channel1_data_input = {
        'token': user1_data_output['token'],
        'name': "channel1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data_input)
    channel1_data_output = r.json()

    # user 2 join the channel created by user 1
    user2_join_data_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user2_join_data_input)

    # User 0 join channel1
    user0_join_data_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user0_join_data_input)

    # User 2 send a message
    user2_message_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=user2_message_input)

    # User 0 send a message
    user0_message_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hi",
    }
    r = requests.post(f"{url}/message/send", json=user0_message_input)
    user0_message_output = r.json()

    # User 0 pin the message sent by user 1
    user1_pin_input = {
        'token': user1_data_output['token'],
        'message_id': user0_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/pin", json=user1_pin_input)

    # User 0 get all channel messages
    user0_get_message_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'start': 0,
    }
    r = requests.get(f"{url}/channel/messages", params=user0_get_message_input)
    user0_get_message_output = r.json()
    assert user0_get_message_output['message_list'][1]['is_pinned'] == True

def test_message_pin_invalid0(url):
    '''message_id is not a valid message'''
    clear()

    # Register user 0
    user0_data_input = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
        'name_first': "Yilang",
        'name_last': "W",
    }
    r = requests.post(f"{url}/auth/register", json=user0_data_input)
    user0_data_output = r.json()

    # Register user 1
    user1_data_input = {
        'email': "billgates@outlook.com",
        'password':  "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates"
    }
    r = requests.post(f"{url}/auth/register", json=user1_data_input)
    user1_data_output = r.json()

    # Register user 2
    user2_data_input = {
        'email': "johnson@icloud.com",
        'password': "RFVtgb45678",
        'name_first': "M",
        'name_last': "Johnson"
    }
    r = requests.post(f"{url}/auth/register", json=user2_data_input)
    user2_data_output = r.json()

    # User 0 create a channel
    channel0_data_input = {
        'token': user0_data_output['token'],
        'name': "channel0",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel0_data_input)
    channel0_data_output = r.json()

    # User 1 join the channel
    user1_join_data_input = {
        'token': user1_data_output['token'],
        'channel_id': channel0_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user1_join_data_input)

    # User 1 create another channel
    channel1_data_input = {
        'token': user1_data_output['token'],
        'name': "channel1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data_input)
    channel1_data_output = r.json()

    # user 2 join the channel created by user 1
    user2_join_data_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user2_join_data_input)

    # User 0 join channel1
    user0_join_data_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user0_join_data_input)

    # User 2 send a message
    user2_message_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=user2_message_input)

    # User 1 send a message
    user1_message_input = {
        'token': user1_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hi",
    }
    r = requests.post(f"{url}/message/send", json=user1_message_input)

    # User 1 pin a non exist message
    user1_pin_input = {
        'token': user1_data_output['token'],
        'message_id': 2,
    }
    r = requests.post(f"{url}/message/pin", json=user1_pin_input)
    user1_pin_output = r.json()
    assert user1_pin_output['message'] == '<p>Message does not exist</p>'

def test_message_pin_invalid1(url):
    '''Message with ID message_id is already unpinned'''
    clear()

    # Register user 0
    user0_data_input = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
        'name_first': "Yilang",
        'name_last': "W",
    }
    r = requests.post(f"{url}/auth/register", json=user0_data_input)
    user0_data_output = r.json()

    # Register user 1
    user1_data_input = {
        'email': "billgates@outlook.com",
        'password':  "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates"
    }
    r = requests.post(f"{url}/auth/register", json=user1_data_input)
    user1_data_output = r.json()

    # Register user 2
    user2_data_input = {
        'email': "johnson@icloud.com",
        'password': "RFVtgb45678",
        'name_first': "M",
        'name_last': "Johnson"
    }
    r = requests.post(f"{url}/auth/register", json=user2_data_input)
    user2_data_output = r.json()

    # User 0 create a channel
    channel0_data_input = {
        'token': user0_data_output['token'],
        'name': "channel0",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel0_data_input)
    channel0_data_output = r.json()

    # User 1 join the channel
    user1_join_data_input = {
        'token': user1_data_output['token'],
        'channel_id': channel0_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user1_join_data_input)

    # User 1 create another channel
    channel1_data_input = {
        'token': user1_data_output['token'],
        'name': "channel1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data_input)
    channel1_data_output = r.json()

    # user 2 join the channel created by user 1
    user2_join_data_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user2_join_data_input)

    # User 0 join channel1
    user0_join_data_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user0_join_data_input)

    # User 2 send a message
    user2_message_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=user2_message_input)
    user2_message_output = r.json()

    # User 1 send a message
    user1_message_input = {
        'token': user1_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hi",
    }
    r = requests.post(f"{url}/message/send", json=user1_message_input)

    # User 1 pin the message sent by user 2
    user1_pin_input = {
        'token': user1_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/pin", json=user1_pin_input)

    # User 1 pin the message sent by user 2
    user1_pin_input = {
        'token': user1_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/pin", json=user1_pin_input)
    user1_pin_output = r.json()
    assert user1_pin_output['message'] == '<p>Message has already been pinned</p>'

def test_message_pin_invalid2(url):
    '''The authorised user is not a member of the channel that the message is within'''
    clear()

    # Register user 0
    user0_data_input = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
        'name_first': "Yilang",
        'name_last': "W",
    }
    r = requests.post(f"{url}/auth/register", json=user0_data_input)
    user0_data_output = r.json()

    # Register user 1
    user1_data_input = {
        'email': "billgates@outlook.com",
        'password':  "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates"
    }
    r = requests.post(f"{url}/auth/register", json=user1_data_input)
    user1_data_output = r.json()

    # Register user 2
    user2_data_input = {
        'email': "johnson@icloud.com",
        'password': "RFVtgb45678",
        'name_first': "M",
        'name_last': "Johnson"
    }
    r = requests.post(f"{url}/auth/register", json=user2_data_input)
    user2_data_output = r.json()

    # User 0 create a channel
    channel0_data_input = {
        'token': user0_data_output['token'],
        'name': "channel0",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel0_data_input)
    channel0_data_output = r.json()

    # User 1 join the channel
    user1_join_data_input = {
        'token': user1_data_output['token'],
        'channel_id': channel0_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user1_join_data_input)

    # User 1 create another channel
    channel1_data_input = {
        'token': user1_data_output['token'],
        'name': "channel1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data_input)
    channel1_data_output = r.json()

    # user 2 join the channel created by user 1
    user2_join_data_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user2_join_data_input)

    # User 2 send a message
    user2_message_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=user2_message_input)
    user2_message_output = r.json()

    # User 1 send a message
    user1_message_input = {
        'token': user1_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hi",
    }
    r = requests.post(f"{url}/message/send", json=user1_message_input)

    # User 0 pin the message sent by user 2
    user1_pin_input = {
        'token': user0_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/pin", json=user1_pin_input)
    user0_pin_output = r.json()
    assert user0_pin_output['message'] == '<p>User is not in channel</p>'

def test_message_pin_invalid3(url):
    '''The authorised user is not an owner'''
    clear()

    # Register user 0
    user0_data_input = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
        'name_first': "Yilang",
        'name_last': "W",
    }
    r = requests.post(f"{url}/auth/register", json=user0_data_input)
    user0_data_output = r.json()

    # Register user 1
    user1_data_input = {
        'email': "billgates@outlook.com",
        'password':  "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates"
    }
    r = requests.post(f"{url}/auth/register", json=user1_data_input)
    user1_data_output = r.json()

    # Register user 2
    user2_data_input = {
        'email': "johnson@icloud.com",
        'password': "RFVtgb45678",
        'name_first': "M",
        'name_last': "Johnson"
    }
    r = requests.post(f"{url}/auth/register", json=user2_data_input)
    user2_data_output = r.json()

    # User 0 create a channel
    channel0_data_input = {
        'token': user0_data_output['token'],
        'name': "channel0",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel0_data_input)
    channel0_data_output = r.json()

    # User 1 join the channel
    user1_join_data_input = {
        'token': user1_data_output['token'],
        'channel_id': channel0_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user1_join_data_input)

    # User 1 create another channel
    channel1_data_input = {
        'token': user1_data_output['token'],
        'name': "channel1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data_input)
    channel1_data_output = r.json()

    # user 2 join the channel created by user 1
    user2_join_data_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user2_join_data_input)

    # User 0 join channel1
    user0_join_data_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user0_join_data_input)

    # User 2 send a message
    user2_message_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=user2_message_input)
    user2_message_output = r.json()

    # User 1 send a message
    user1_message_input = {
        'token': user1_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hi",
    }
    r = requests.post(f"{url}/message/send", json=user1_message_input)

    # User 2 pin the message sent by user 2
    user2_pin_input = {
        'token': user2_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/pin", json=user2_pin_input)
    user2_pin_output = r.json()
    assert user2_pin_output['message'] == '<p>You are not owner of flockr</p>'

def test_message_unpin_valid0(url):
    '''Owner of the channel pin the message sent by a member, then the message is unpinned
    by the owner of flockr'''
    clear()

    # Register user 0
    user0_data_input = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
        'name_first': "Yilang",
        'name_last': "W",
    }
    r = requests.post(f"{url}/auth/register", json=user0_data_input)
    user0_data_output = r.json()

    # Register user 1
    user1_data_input = {
        'email': "billgates@outlook.com",
        'password':  "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates"
    }
    r = requests.post(f"{url}/auth/register", json=user1_data_input)
    user1_data_output = r.json()

    # Register user 2
    user2_data_input = {
        'email': "johnson@icloud.com",
        'password': "RFVtgb45678",
        'name_first': "M",
        'name_last': "Johnson"
    }
    r = requests.post(f"{url}/auth/register", json=user2_data_input)
    user2_data_output = r.json()

    # User 0 create a channel
    channel0_data_input = {
        'token': user0_data_output['token'],
        'name': "channel0",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel0_data_input)
    channel0_data_output = r.json()

    # User 1 join the channel
    user1_join_data_input = {
        'token': user1_data_output['token'],
        'channel_id': channel0_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user1_join_data_input)

    # User 1 create another channel
    channel1_data_input = {
        'token': user1_data_output['token'],
        'name': "channel1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data_input)
    channel1_data_output = r.json()

    # user 2 join the channel created by user 1
    user2_join_data_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user2_join_data_input)

    # User 0 join channel1
    user0_join_data_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user0_join_data_input)

    # User 2 send a message
    user2_message_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=user2_message_input)
    user2_message_output = r.json()

    # User 1 send a message
    user1_message_input = {
        'token': user1_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hi",
    }
    r = requests.post(f"{url}/message/send", json=user1_message_input)

    # User 1 pin the message sent by user 2
    user1_pin_input = {
        'token': user1_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/pin", json=user1_pin_input)

    # User 0 unpin the message just pinned by user 1
    user0_unpin_input = {
        'token': user0_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/unpin", json=user0_unpin_input)

    # User 0 get all channel messages
    user0_get_message_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'start': 0,
    }
    r = requests.get(f"{url}/channel/messages", params=user0_get_message_input)
    user0_get_message_output = r.json()
    assert user0_get_message_output['message_list'][0]['is_pinned'] == False

def test_message_unpin_valid1(url):
    '''Owner of the flocker pins a message sent by a member then the 
    message is uppined by the owner of the channel'''
    clear()

    # Register user 0
    user0_data_input = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
        'name_first': "Yilang",
        'name_last': "W",
    }
    r = requests.post(f"{url}/auth/register", json=user0_data_input)
    user0_data_output = r.json()

    # Register user 1
    user1_data_input = {
        'email': "billgates@outlook.com",
        'password':  "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates"
    }
    r = requests.post(f"{url}/auth/register", json=user1_data_input)
    user1_data_output = r.json()

    # Register user 2
    user2_data_input = {
        'email': "johnson@icloud.com",
        'password': "RFVtgb45678",
        'name_first': "M",
        'name_last': "Johnson"
    }
    r = requests.post(f"{url}/auth/register", json=user2_data_input)
    user2_data_output = r.json()

    # User 0 create a channel
    channel0_data_input = {
        'token': user0_data_output['token'],
        'name': "channel0",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel0_data_input)
    channel0_data_output = r.json()

    # User 1 join the channel
    user1_join_data_input = {
        'token': user1_data_output['token'],
        'channel_id': channel0_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user1_join_data_input)

    # User 1 create another channel
    channel1_data_input = {
        'token': user1_data_output['token'],
        'name': "channel1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data_input)
    channel1_data_output = r.json()

    # user 2 join the channel created by user 1
    user2_join_data_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user2_join_data_input)

    # User 0 join channel1
    user0_join_data_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user0_join_data_input)

    # User 2 send a message
    user2_message_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=user2_message_input)
    user2_message_output = r.json()

    # User 1 send a message
    user1_message_input = {
        'token': user1_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hi",
    }
    r = requests.post(f"{url}/message/send", json=user1_message_input)

    # User 0 pin the message sent by user 2
    user0_pin_input = {
        'token': user0_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/pin", json=user0_pin_input)

    # User 1 unpin the message just pinned by user 1
    user1_unpin_input = {
        'token': user1_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/unpin", json=user1_unpin_input)

    # User 0 get all channel messages
    user0_get_message_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'start': 0,
    }
    r = requests.get(f"{url}/channel/messages", params=user0_get_message_input)
    user0_get_message_output = r.json()
    assert user0_get_message_output['message_list'][0]['is_pinned'] == False

def test_message_unpin_invalid0(url):
    '''message_id is not a valid message'''
    clear()

    # Register user 0
    user0_data_input = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
        'name_first': "Yilang",
        'name_last': "W",
    }
    r = requests.post(f"{url}/auth/register", json=user0_data_input)
    user0_data_output = r.json()

    # Register user 1
    user1_data_input = {
        'email': "billgates@outlook.com",
        'password':  "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates"
    }
    r = requests.post(f"{url}/auth/register", json=user1_data_input)
    user1_data_output = r.json()

    # Register user 2
    user2_data_input = {
        'email': "johnson@icloud.com",
        'password': "RFVtgb45678",
        'name_first': "M",
        'name_last': "Johnson"
    }
    r = requests.post(f"{url}/auth/register", json=user2_data_input)
    user2_data_output = r.json()

    # User 0 create a channel
    channel0_data_input = {
        'token': user0_data_output['token'],
        'name': "channel0",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel0_data_input)
    channel0_data_output = r.json()

    # User 1 join the channel
    user1_join_data_input = {
        'token': user1_data_output['token'],
        'channel_id': channel0_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user1_join_data_input)

    # User 1 create another channel
    channel1_data_input = {
        'token': user1_data_output['token'],
        'name': "channel1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data_input)
    channel1_data_output = r.json()

    # user 2 join the channel created by user 1
    user2_join_data_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user2_join_data_input)

    # User 0 join channel1
    user0_join_data_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user0_join_data_input)

    # User 2 send a message
    user2_message_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=user2_message_input)
    user2_message_output = r.json()

    # User 1 send a message
    user1_message_input = {
        'token': user1_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hi",
    }
    r = requests.post(f"{url}/message/send", json=user1_message_input)

    # User 0 pin the message sent by user 2
    user0_pin_input = {
        'token': user0_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/pin", json=user0_pin_input)

    # User 1 unpin the message just pinned by user 0
    user1_unpin_input = {
        'token': user1_data_output['token'],
        'message_id': 2,
    }
    r = requests.post(f"{url}/message/unpin", json=user1_unpin_input)
    user1_unpin_output = r.json()
    assert user1_unpin_output['message'] == '<p>Message does not exist</p>'

def test_message_unpin_invalid1(url):
    '''Message with ID message_id is already unpinned'''
    clear()

    # Register user 0
    user0_data_input = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
        'name_first': "Yilang",
        'name_last': "W",
    }
    r = requests.post(f"{url}/auth/register", json=user0_data_input)
    user0_data_output = r.json()

    # Register user 1
    user1_data_input = {
        'email': "billgates@outlook.com",
        'password':  "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates"
    }
    r = requests.post(f"{url}/auth/register", json=user1_data_input)
    user1_data_output = r.json()

    # Register user 2
    user2_data_input = {
        'email': "johnson@icloud.com",
        'password': "RFVtgb45678",
        'name_first': "M",
        'name_last': "Johnson"
    }
    r = requests.post(f"{url}/auth/register", json=user2_data_input)
    user2_data_output = r.json()

    # User 0 create a channel
    channel0_data_input = {
        'token': user0_data_output['token'],
        'name': "channel0",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel0_data_input)
    channel0_data_output = r.json()

    # User 1 join the channel
    user1_join_data_input = {
        'token': user1_data_output['token'],
        'channel_id': channel0_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user1_join_data_input)

    # User 1 create another channel
    channel1_data_input = {
        'token': user1_data_output['token'],
        'name': "channel1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data_input)
    channel1_data_output = r.json()

    # user 2 join the channel created by user 1
    user2_join_data_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user2_join_data_input)

    # User 0 join channel1
    user0_join_data_input = {
        'token': user0_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user0_join_data_input)

    # User 2 send a message
    user2_message_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=user2_message_input)
    user2_message_output = r.json()

    # User 1 send a message
    user1_message_input = {
        'token': user1_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hi",
    }
    r = requests.post(f"{url}/message/send", json=user1_message_input)

    # User 0 pin the message sent by user 2
    user0_pin_input = {
        'token': user0_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/pin", json=user0_pin_input)

    # User 1 unpin the message just pinned by user 0
    user1_unpin_input = {
        'token': user1_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/unpin", json=user1_unpin_input)
    
    # User 0 unpin again
    user0_unpin_input = {
        'token': user0_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/unpin", json=user0_unpin_input)
    user0_unpin_output = r.json()
    assert user0_unpin_output['message'] == '<p>Message is not pinned already</p>'

def test_message_unpin_invalid2(url):
    '''The authorised user is not a member of the channel that the message is within'''
    clear()

    # Register user 0
    user0_data_input = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
        'name_first': "Yilang",
        'name_last': "W",
    }
    r = requests.post(f"{url}/auth/register", json=user0_data_input)
    user0_data_output = r.json()

    # Register user 1
    user1_data_input = {
        'email': "billgates@outlook.com",
        'password':  "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates"
    }
    r = requests.post(f"{url}/auth/register", json=user1_data_input)
    user1_data_output = r.json()

    # Register user 2
    user2_data_input = {
        'email': "johnson@icloud.com",
        'password': "RFVtgb45678",
        'name_first': "M",
        'name_last': "Johnson"
    }
    r = requests.post(f"{url}/auth/register", json=user2_data_input)
    user2_data_output = r.json()

    # User 0 create a channel
    channel0_data_input = {
        'token': user0_data_output['token'],
        'name': "channel0",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel0_data_input)
    channel0_data_output = r.json()

    # User 1 join the channel
    user1_join_data_input = {
        'token': user1_data_output['token'],
        'channel_id': channel0_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user1_join_data_input)

    # User 1 create another channel
    channel1_data_input = {
        'token': user1_data_output['token'],
        'name': "channel1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data_input)
    channel1_data_output = r.json()

    # user 2 join the channel created by user 1
    user2_join_data_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user2_join_data_input)

    # User 2 send a message
    user2_message_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=user2_message_input)
    user2_message_output = r.json()

    # User 1 send a message
    user1_message_input = {
        'token': user1_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hi",
    }
    r = requests.post(f"{url}/message/send", json=user1_message_input)

    # User 1 pin the message sent by user 2
    user1_pin_input = {
        'token': user1_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/pin", json=user1_pin_input)

    # User 0 unpin the message just pinned by user 1
    user0_unpin_input = {
        'token': user0_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/unpin", json=user0_unpin_input)
    user0_unpin_output = r.json()
    assert user0_unpin_output['message'] == '<p>User is not in channel</p>'

def test_message_unpin_invalid3(url):
    '''The authorised user is not an owner'''
    clear()

    # Register user 0
    user0_data_input = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
        'name_first': "Yilang",
        'name_last': "W",
    }
    r = requests.post(f"{url}/auth/register", json=user0_data_input)
    user0_data_output = r.json()

    # Register user 1
    user1_data_input = {
        'email': "billgates@outlook.com",
        'password':  "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates"
    }
    r = requests.post(f"{url}/auth/register", json=user1_data_input)
    user1_data_output = r.json()

    # Register user 2
    user2_data_input = {
        'email': "johnson@icloud.com",
        'password': "RFVtgb45678",
        'name_first': "M",
        'name_last': "Johnson"
    }
    r = requests.post(f"{url}/auth/register", json=user2_data_input)
    user2_data_output = r.json()

    # User 0 create a channel
    channel0_data_input = {
        'token': user0_data_output['token'],
        'name': "channel0",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel0_data_input)
    channel0_data_output = r.json()

    # User 1 join the channel
    user1_join_data_input = {
        'token': user1_data_output['token'],
        'channel_id': channel0_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user1_join_data_input)

    # User 1 create another channel
    channel1_data_input = {
        'token': user1_data_output['token'],
        'name': "channel1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", json=channel1_data_input)
    channel1_data_output = r.json()

    # user 2 join the channel created by user 1
    user2_join_data_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
    }
    r = requests.post(f"{url}/channel/join", json=user2_join_data_input)

    # User 2 send a message
    user2_message_input = {
        'token': user2_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hello",
    }
    r = requests.post(f"{url}/message/send", json=user2_message_input)
    user2_message_output = r.json()

    # User 1 send a message
    user1_message_input = {
        'token': user1_data_output['token'],
        'channel_id': channel1_data_output['channel_id'],
        'message': "Hi",
    }
    r = requests.post(f"{url}/message/send", json=user1_message_input)

    # User 1 pin the message sent by user 2
    user1_pin_input = {
        'token': user1_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/pin", json=user1_pin_input)

    # User 2 unpin the message just pinned by user 1
    user2_unpin_input = {
        'token': user2_data_output['token'],
        'message_id': user2_message_output['message_id'],
    }
    r = requests.post(f"{url}/message/unpin", json=user2_unpin_input)
    user2_unpin_output = r.json()
    assert user2_unpin_output['message'] == '<p>You are not owner of flockr</p>'