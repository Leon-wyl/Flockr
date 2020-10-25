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

def test_server_user(url):
    # test server user profile success
    FirstUser1 = {
        'email': "leonwu@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Yilang",
        'name_last': "Wu",
    }
    r = requests.post(f"{url}/auth/register", json=FirstUser1)
    return_data = r.json()
    assert return_data['u_id'] == 0
    assert return_data['token'] == token_generate(return_data['u_id'])

    FirstUser = {
        'token': token_generate(0),
        'u_id': 0,
    }
    r = requests.get(f"{url}/user/profile", params=FirstUser)
    return_data = r.json()
    assert return_data == {
        'user': {
            'u_id': 0,
            'email': "leonwu@gmail.com",
            'name_first': "Yilang",
            'name_last': "Wu",
            'handle_str': "yilangwu",
        }
    }

    # test server user profile invalid user
    InvalidUser = {
        'token': 0,
        'u_id': 1,
    }
    r = requests.get(f"{url}/user/profile", params=InvalidUser)
    return_data = r.json()
    assert return_data['message'] == '<p>User is invalid</p>'

    # test server user profile setname
    ChangedName = {
        'token': token_generate(0),
        'name_first': 'Dennis',
        'name_last': 'Lin',
    }

    r = requests.put(f"{url}/user/profile/setname", json=ChangedName)
    return_data = r.json()
    assert return_data == {}

    r = requests.get(f"{url}/user/profile", params=FirstUser)
    return_data = r.json()
    assert return_data == {
        'user': {
            'u_id': 0,
            'email': "leonwu@gmail.com",
            'name_first': "Dennis",
            'name_last': "Lin",
            'handle_str': "yilangwu",
        }
    }

    # test_user_profile_setname_first_name_too_long
    TooLongName = {
        'token': token_generate(0),
        'name_first': 'Dennissssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss',
        'name_last': 'Lin',
    }

    r = requests.put(f"{url}/user/profile/setname", json=TooLongName)
    return_data = r.json()
    assert return_data['message'] == '<p>Firstname is too long!</p>'

    # test_user_profile_setname_last_name_too_long
    TooLongName = {
        'token': token_generate(0),
        'name_first': 'Dennis',
        'name_last': 'Linnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn',
    }

    r = requests.put(f"{url}/user/profile/setname", json=TooLongName)
    return_data = r.json()
    assert return_data['message'] == '<p>Lastname is too long!</p>'

    # test server user_profile_setemail

    ChangedEmail = {
        'token': token_generate(0),
        'email': '2071807612@qq.com'
    }

    r = requests.put(f"{url}/user/profile/setemail", json=ChangedEmail)
    return_data = r.json()
    assert return_data == {}

    r = requests.get(f"{url}/user/profile", params=FirstUser)
    return_data = r.json()
    assert return_data == {
        'user': {
            'u_id': 0,
            'email': "2071807612@qq.com",
            'name_first': "Dennis",
            'name_last': "Lin",
            'handle_str': "yilangwu",
        }
    }

    # test_user_profile_setemail_already_used
    InvalidEmail = {
        'token': token_generate(0),
        'email': '2071807612@qq.com'
    }

    r = requests.put(f"{url}/user/profile/setemail", json=InvalidEmail)
    return_data = r.json()
    assert return_data['message'] == '<p>The email has already been used by another user</p>'

    # server test user_profile_sethandle

    ChangedHandle = {
        'token': token_generate(0),
        'handle_str': 'dennislin'
    }

    r = requests.put(f"{url}/user/profile/sethandle", json=ChangedHandle)
    return_data = r.json()
    assert return_data == {}

    r = requests.get(f"{url}/user/profile", params=FirstUser)
    return_data = r.json()
    assert return_data == {
        'user': {
            'u_id': 0,
            'email': "2071807612@qq.com",
            'name_first': "Dennis",
            'name_last': "Lin",
            'handle_str': "dennislin",
        }
    }