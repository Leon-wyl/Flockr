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

def test_server_user_profile(url):
    # Register a user
    dataIn = {
        'email': "leonwu@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Yilang",
        'name_last': "Wu",
    }
    r = requests.post(f"{url}/auth/register", json=dataIn)
    return_data1 = r.json()

    dataIn = {
        'token': token_generate(0),
        'u_id': 0,
    }
    r = requests.post(f"{url}/user/profile", json=dataIn)
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

    dataIn = {
        token': token_generate(0),
        'u_id': 0,

    r = requests.post(f"{url}/auth/register", json=dataIn2)
    return_data = r.json()
    assert return_data['message'] == "<p>Email entered is not a valid email</p>"

