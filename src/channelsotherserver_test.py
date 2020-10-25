import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
from database import *

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

def test_channels_list(url):
    requests.delete(f"{url}/clear")
    info1 = requests.post(f"{url}/auth/register", json={'email': 'leonwu@gmail.com', 'password': 'ihfeh3hgi00d', 'name_first': 'Bill', 'name_last': 'Gates'})
    info1 = info1.json()
    info2 = requests.post(f"{url}/auth/register", json={'email': "eviedunstone@gmail.com", 'password': 'Qwerty6', 'name_first': 'Evie', 'name_last': 'Dunstone'})
    info2 = info2.json()
    requests.post(f"{url}/auth/login", json={'email': 'leonwu@gmail.com', 'password': 'ihfeh3hgi00d'})
    requests.post(f"{url}/auth/login", json={'email': "eviedunstone@gmail.com", 'password': 'Qwerty6'})
    requests.post(f"{url}/channels/create", json={'token': info1['token'], 'name': 'first', 'is_public': True})
    requests.post(f"{url}/channels/create", json={'token': info1['token'], 'name': 'second', 'is_public': True})
    requests.post(f"{url}/channels/create", json={'token': info1['token'], 'name': 'third', 'is_public': True})
    requests.post(f"{url}/channels/create", json={'token': info1['token'], 'name': 'fourth', 'is_public': True})   
    requests.post(f"{url}/channel/join", json={'token': info2['token'], 'channel_id': 0})
    requests.post(f"{url}/channel/join", json={'token': info2['token'], 'channel_id': 2})
    resp = requests.get(f"{url}/channels/list", params={'token': info2['token']})
    resp = resp.json()
    assert resp['channels'] == [{'channel_id': 0, 'name': 'first'}, {'channel_id': 2, 'name': 'third'}]


def test_channels_listall(url):
    requests.delete(f"{url}/clear")
    info = requests.post(f"{url}/auth/register", json={'email': 'leonwu@gmail.com', 'password': 'ihfeh3hgi00d', 'name_first': 'Bill', 'name_last': 'Gates'})
    info = info.json()
    requests.post(f"{url}/auth/login", json={'email': 'leonwu@gmail.com', 'password': 'ihfeh3hgi00d'})
    requests.post(f"{url}/channels/create", json={'token': info['token'], 'name': 'first', 'is_public': True})
    requests.post(f"{url}/channels/create", json={'token': info['token'], 'name': 'second', 'is_public': True})
    requests.post(f"{url}/channels/create", json={'token': info['token'], 'name': 'third', 'is_public': True})
    requests.post(f"{url}/channels/create", json={'token': info['token'], 'name': 'fourth', 'is_public': True}) 
    resp = requests.get(f"{url}/channels/listall", params={'token': info['token']})
    resp = resp.json()
    assert resp['channels'] == [
        {'channel_id': 0, 'name': 'first'},
        {'channel_id': 1, 'name': 'second'},
        {'channel_id': 2, 'name': 'third'},
        {'channel_id': 3, 'name': 'fourth'}
    ]




def test_channels_create(url):
    # Register a user
    dataIn1 = {
        'email': "leonwu@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Yilang",
        'name_last': "Wu",
    }
    r = requests.post(f"{url}/auth/register", json=dataIn1)
    return_data1 = r.json()
    resp = requests.post(f"{url}/channels/create", json={'token': return_data1['token'], 'name': 'first', 'is_public': True})
    assert resp.json() == {'channel_id' : 0}
    resp = requests.post(f"{url}/channels/create", json={'token': return_data1['token'], 'name': 'second', 'is_public': True})
    assert resp.json() == {'channel_id' : 1}
    

def test_clear(url):
    requests.delete(f"{url}/clear")  





def test_users_all(url):
    requests.delete(f"{url}/clear")
    info1 = requests.post(f"{url}/auth/register", json={'email': 'leonwu@gmail.com', 'password': 'ihfeh3hgi00d', 'name_first': 'Yilang', 'name_last': 'W'})
    info1 = info1.json()
    info2 = requests.post(f"{url}/auth/register", json={'email': "johnson@icloud.com", 'password': 'RFVtgb45678', 'name_first': 'M', 'name_last': 'Johnson'})
    info2 = info2.json()
    requests.post(f"{url}/auth/login", json={'email': "johnson@icloud.com", 'password': 'RFVtgb45678'})
    resp = requests.get(f"{url}/users/all", params={'token': info2['token']})
    resp = resp.json()
    assert resp == {'users': [
        {
            'u_id': 0,
            'email': "leonwu@gmail.com",
            'name_first': "Yilang",
            'name_last': "W",
            'handle_str': 'yilangw',
         },
         {
            'u_id': 1,
            'email': "johnson@icloud.com",
            'name_first': "M",
            'name_last': "Johnson",
            'handle_str': 'mjohnson',
         }
        
    ]}




def test_admin_userpermission_change(url):
    requests.delete(f"{url}/clear")
    info1 = requests.post(f"{url}/auth/register", json={'email': 'leonwu@gmail.com', 'password': 'ihfeh3hgi00d', 'name_first': 'Yilang', 'name_last': 'W'})
    info1 = info1.json()
    info2 = requests.post(f"{url}/auth/register", json={'email': "johnson@icloud.com", 'password': 'RFVtgb45678', 'name_first': 'M', 'name_last': 'Johnson'})
    info2 = info2.json()
    requests.post(f"{url}/auth/login", json={'email': 'leonwu@gmail.com', 'password': 'ihfeh3hgi00d'})
    requests.post(f"{url}/admin/userpermission/change", json={'token': info1['token'], 'u_id': 1, 'permission_id': 1})

    



def test_search(url):
    requests.delete(f"{url}/clear")
    info1 = requests.post(f"{url}/auth/register", json={'email': 'leonwu@gmail.com', 'password': 'ihfeh3hgi00d', 'name_first': 'Yilang', 'name_last': 'W'})
    info1 = info1.json()
    requests.post(f"{url}/auth/login", json={'email': 'leonwu@gmail.com', 'password': 'ihfeh3hgi00d'})
    requests.post(f"{url}/channels/create", json={'token': info1['token'], 'name': 'first', 'is_public': True})
    requests.post(f"{url}/message/send", json={'token': info1['token'], 'channel_id': 0, 'message': "I am ok haha"})
    resp = requests.get(f"{url}/search", params={'token': info1['token'], 'query_str': 'ok'})
    resp = resp.json()
    assert resp == {'messages': [
        {
            'message_id': 0,
            'u_id': 0,
            'message': "I am ok haha",
            'time_created': 0,
        }         
    ]}



