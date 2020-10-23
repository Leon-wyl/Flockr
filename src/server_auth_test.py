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

def test_server_auth_register(url):

    dataIn1 = {
        'email': "leonwu@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Yilang",
        'name_last': "Wu",
    }
    r = requests.post(f"{url}/auth/register", json=dataIn1)
    return_data = r.json()
    assert return_data['u_id'] == 0
    assert return_data['token'] == token_generate(return_data['u_id'])

    dataIn2 = {
        'email': "ufhsdfkshfdhfsfhiw",
        'password': "uf89rgu",
        'name_first': "Andrew",
        'name_last': "Williams",
    }
    #with pytest.raises(InputError):
    r = requests.post(f"{url}/auth/register", json=dataIn2)
    return_data = r.json()
    assert return_data['message'] == "<p>Email entered is not a valid email</p>"

def test_server_auth_logout(url):

    # Register a user
    dataIn1 = {
        'email': "leonwu@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Yilang",
        'name_last': "Wu",
    }
    r = requests.post(f"{url}/auth/register", json=dataIn1)
    return_data1 = r.json()

    # Logout the user
    dataIn2 = {
        'token': return_data1['token']
    }
    r = requests.post(f"{url}/auth/logout", json=dataIn2)
    return_data2 = r.json()
    assert return_data2['is_success'] == True

    # Logout an invalid u_id
    dataIn3 = {
        'token': token_generate(5)
    }
    r = requests.post(f"{url}/auth/logout", json=dataIn3)
    return_data4 = r.json()
    assert return_data4['is_success'] == False

def test_server_auth_login(url):

    # Register a user
    dataIn1 = {
        'email': "leonwu@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Yilang",
        'name_last': "Wu",
    }
    r = requests.post(f"{url}/auth/register", json=dataIn1)
    return_data1 = r.json()

    # Log out this user
    dataIn2 = {
        'token': return_data1['token']
    }
    r = requests.post(f"{url}/auth/logout", json=dataIn2)

    # Log in this user with a wrong password
    dataIn3 = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3h",
    }
    r = requests.post(f"{url}/auth/login", json=dataIn3)
    return_data1 = r.json()
    assert return_data1['message'] == "<p>Password is not correct</p>"
    # Login this user again
    dataIn4 = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
    }
    r = requests.post(f"{url}/auth/login", json=dataIn4)
    return_data2 = r.json()
    assert return_data2['u_id'] == 0
    assert return_data2['token'] == token_generate(return_data2['u_id'])

def test_server_addowner():

    # Register a user
    dataIn1 = {
        'email': "leonwu@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Yilang",
        'name_last': "Wu",
    }
    r = requests.post(f"{url}/auth/register", data=dataIn1)
    return_data1 = r.json()

    # Register another user
    dataIn2 = {
        'email': "billgates@outlook.com",
        'password': "VukkFs",
        'name_first': "Bill",
        'name_last': "Gates",
    }
    r = requests.post(f"{url}/auth/register", data=dataIn2)
    return_data2 = r.json()

    # Channel created by the first user
    dataIn3 = {
        'token': return_data1['token'],
        'name': "group1",
        'is_public': True,
    }
    r = requests.post(f"{url}/channels/create", data=dataIn3)
    return_data3 = r.json()

    # The second user join the channel
    dataIn4 = {
        'token': return_data2['token'],
        'channel_id': 0,
    }
    r = requests.post(f"{url}/channel/join", data=dataIn4)
    
    # The first user add the second user as an owner
    dataIn5 = {
        'token': dataIn1['token'],
        'channel_id': 0,
        'u_id': dataIn2['u_id'],
    }
    r = requests.post(f"{url}/channel/addowner", data=dataIn4)
