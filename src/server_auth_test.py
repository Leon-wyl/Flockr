import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
from other import clear
from utility import token_generate


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

'''def test_server_auth_register():
    clear()
    dataIn1 = {
        'email': "leonwu@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Yilang",
        'name_last': "Wu",
    }
    r = requests.post(f"{url}/auth/register", json=dataIn1)
    return_data = r.json()
    assert return_data['u_id'] == 0
    assert return_data['token'] == token_generate(return_data[u_id])

    dataIn2 = {
        'email': "ufhsdfkshfdhfsfhiw",
        'password': "uf89rgu",
        'name_first': "Andrew",
        'name_last': "Williams",
    }
    with pytest.raises(InputError):
        r = requests.post(f"{url}/auth/register", json=dataIn2)

def test_server_auth_logout():
    clear()
    # Register a user
    dataIn1 = {
        'email': "leonwu@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Yilang",
        'name_last': "Wu",
    }
    r = requests.post(f"{url}/auth/register", data=dataIn1)
    return_data1 = r.json()

    # Logout the user
    dataIn2 = {
        'token': return_data1['token']
    }
    r = requests.post(f"{url}/auth/logout", data=dataIn2)
    return_data2 = r.json()
    assert return_data2['is_success'] == True

    # Logout again
    r = requests.post(f"{url}/auth/logout", data=dataIn2)
    return_data3 = r.json()
    assert return_data3['is_success'] == False

    # Logout an invalid u_id
    dataIn3 = {
        'token': token_generate(5)
    }
    r = requests.post(f"{url}/auth/logout", data=dataIn3)
    return_data4 = r.json()
    assert return_data4['is_success'] == False

def test_server_auth_login():
    clear()

    # Register a user
    dataIn1 = {
        'email': "leonwu@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Yilang",
        'name_last': "Wu",
    }
    r = requests.post(f"{url}/auth/register", data=dataIn1)
    return_data1 = r.json()

    # Log out this user
    dataIn2 = {
        'token': return_data1['token']
    }
    r = requests.post(f"{url}/auth/logout", data=dataIn2)

    # Log in this user with a wrong password
    dataIn3 = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3h",
    }
    with pytest.raises(InputError):
        r = requests.post(f"{url}/auth/login", data=dataIn3)

    # Login this user again
    dataIn4 = {
        'email': "leonwu@gmail.com",
        'password': "ihfeh3hgi00d",
    }
    r = requests.post(f"{url}/auth/login", data=dataIn4)
    return_data1 = r.json()
    assert return_data1['u_id'] == 0
    assert return_data1['token'] == token_generate(return_data1['u_id'])

def test_server_addowner():
    clear()

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
    
'''