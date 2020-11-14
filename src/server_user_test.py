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

# test user_profile, user_setname, user_setemail, user_sethandle
def test_server_user_set(url):
    requests.delete(f"{url}/clear")
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
    token1 = return_data['token']

    FirstUser = {
        'token': return_data['token'],
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
            'profile_img_url': return_data['user']['profile_img_url'],
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
        'token': token1,
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
            'profile_img_url': return_data['user']['profile_img_url'],
        }
    }

    # test_user_profile_setname_first_name_too_long
    TooLongName = {
        'token': token1,
        'name_first': 'Dennissssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss',
        'name_last': 'Lin',
    }

    r = requests.put(f"{url}/user/profile/setname", json=TooLongName)
    return_data = r.json()
    assert return_data['message'] == '<p>Firstname is too long!</p>'

    # test_user_profile_setname_last_name_too_long
    TooLongName = {
        'token': token1,
        'name_first': 'Dennis',
        'name_last': 'Linnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn',
    }

    r = requests.put(f"{url}/user/profile/setname", json=TooLongName)
    return_data = r.json()
    assert return_data['message'] == '<p>Lastname is too long!</p>'

    # test server user_profile_setemail

    ChangedEmail = {
        'token': token1,
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
            'profile_img_url': return_data['user']['profile_img_url'],
        }
    }

    # test_user_profile_setemail_invalid_email
    InvalidEmail = {
        'token': token1,
        'email': '2071807612qq.com'
    }

    r = requests.put(f"{url}/user/profile/setemail", json=InvalidEmail)
    return_data = r.json()
    assert return_data['message'] == '<p>Email entered is not a valid email</p>'

    # test_user_profile_setemail_already_used
    InvalidEmail = {
        'token': token1,
        'email': '2071807612@qq.com'
    }

    r = requests.put(f"{url}/user/profile/setemail", json=InvalidEmail)
    return_data = r.json()
    assert return_data['message'] == '<p>The email has already been used by another user</p>'

    # server test user_profile_sethandle

    ChangedHandle = {
        'token': token1,
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
            'profile_img_url': return_data['user']['profile_img_url'],
        }
    }

    # test_user_profile_sethandle_too_long
    ChangedHandle = {
        'token': token1,
        'handle_str': 'dennislinnnnnnnnnnnnnnnnnn'
    }

    r = requests.put(f"{url}/user/profile/sethandle", json=ChangedHandle)
    return_data = r.json()
    assert return_data['message'] == '<p>Handle is too long!</p>'

    # test_user_profile_sethandle_too_short
    ChangedHandle = {
        'token': token1,
        'handle_str': 'de'
    }

    r = requests.put(f"{url}/user/profile/sethandle", json=ChangedHandle)
    return_data = r.json()
    assert return_data['message'] == '<p>Handle is too short!</p>'

    # test_user_profile_sethandle_already_used
    SecondUser = {
        'email': "leonwu@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Zixiang", # the handle string of this user would be zixianglin
        'name_last': "Lin",
    }
    r = requests.post(f"{url}/auth/register", json=SecondUser)
    return_data = r.json()
    assert return_data['u_id'] == 1
    token2 = return_data['token']
    assert return_data['token'] == token2

    ChangedHandle = {
        'token': token2,
        'handle_str': 'zixianglin'
    }

    r = requests.put(f"{url}/user/profile/sethandle", json=ChangedHandle)
    return_data = r.json()
    assert return_data['message'] == '<p>Handle is already used by another user</p>'


def test_user_profile_uploadphoto(url):
    requests.delete(f"{url}/clear")
    # register a user
    FirstUser = {
        'email': "leonwu@gmail.com", 
        'password': "ihfeh3hgi00d", 
        'name_first': "Yilang",
        'name_last': "Wu",
    }
    r = requests.post(f"{url}/auth/register", json=FirstUser)
    return_data = r.json()
    assert return_data['u_id'] == 0     # check if user has been created
    token1 = return_data['token']

    correct_input = {
        'token': token1, 
        'img_url': 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg', 
        'x_start': 0, 
        'y_start': 0, 
        'x_end': 600, 
        'y_end': 300,
    }
    r = requests.post(f"{url}/user/profile/uploadphoto", json=correct_input)
    return_data = r.json()
    assert return_data == {}

    # Wrong HTTP status
    wrong_url = {
        'token': token1, 
        'img_url': 'http://images.abcde.jpg', 
        'x_start': 0, 
        'y_start': 0, 
        'x_end': 0, 
        'y_end': 0,
    }
    r = requests.post(f"{url}/user/profile/uploadphoto", json=wrong_url)
    return_data = r.json()
    assert return_data['message'] == '<p>url is invalid</p>'


    # wrong dimension
    x_end_exceed = {
        'token': token1, 
        'img_url': 'http://images.tritondigitalcms.com/6616/sites/356/2017/07/28103713/Rick-Astley.jpg', 
        'x_start': 0, 
        'y_start': 0, 
        'x_end': 500000, 
        'y_end': 1000,
    }
    r = requests.post(f"{url}/user/profile/uploadphoto", json=x_end_exceed)
    return_data = r.json()
    assert return_data['message'] == '<p>Dimension is out of range!</p>'
    
    y_end_exceed = {
        'token': token1, 
        'img_url': 'http://images.tritondigitalcms.com/6616/sites/356/2017/07/28103713/Rick-Astley.jpg', 
        'x_start': 0, 
        'y_start': 0, 
        'x_end': 500, 
        'y_end': 500000,
    }
    r = requests.post(f"{url}/user/profile/uploadphoto", json=y_end_exceed)
    return_data = r.json()
    assert return_data['message'] == '<p>Dimension is out of range!</p>'

    x_start_exceed = {
        'token': token1, 
        'img_url': 'http://images.tritondigitalcms.com/6616/sites/356/2017/07/28103713/Rick-Astley.jpg', 
        'x_start': 100000, 
        'y_start': 0, 
        'x_end': 500, 
        'y_end': 500,
    }
    r = requests.post(f"{url}/user/profile/uploadphoto", json=x_start_exceed)
    return_data = r.json()
    assert return_data['message'] == '<p>Dimension is out of range!</p>'

    y_start_exceed = {
        'token': token1, 
        'img_url': 'http://images.tritondigitalcms.com/6616/sites/356/2017/07/28103713/Rick-Astley.jpg', 
        'x_start': 0, 
        'y_start': 100000, 
        'x_end': 500, 
        'y_end': 500,
    }
    r = requests.post(f"{url}/user/profile/uploadphoto", json=y_start_exceed)
    return_data = r.json()
    assert return_data['message'] == '<p>Dimension is out of range!</p>'
    

    negative_x_start = {
        'token': token1, 
        'img_url': 'http://images.tritondigitalcms.com/6616/sites/356/2017/07/28103713/Rick-Astley.jpg', 
        'x_start': -1, 
        'y_start': 0, 
        'x_end': 500, 
        'y_end': 500,
    }
    r = requests.post(f"{url}/user/profile/uploadphoto", json=negative_x_start)
    return_data = r.json()
    assert return_data['message'] == '<p>Dimension is out of range!</p>'

    negative_y_start = {
        'token': token1, 
        'img_url': 'http://images.tritondigitalcms.com/6616/sites/356/2017/07/28103713/Rick-Astley.jpg', 
        'x_start': 0, 
        'y_start': -1, 
        'x_end': 500, 
        'y_end': 500,
    }
    r = requests.post(f"{url}/user/profile/uploadphoto", json=negative_y_start)
    return_data = r.json()
    assert return_data['message'] == '<p>Dimension is out of range!</p>'


    # Image url is not a jpg
    not_jpg = {
        'token': token1, 
        'img_url': 'http://images.tritondigitalcms.com/6616/sites/356/2017/07/28103713/Rick-Astley.img', 
        'x_start': 0, 
        'y_start': 0, 
        'x_end': 0, 
        'y_end': 0,
    }
    r = requests.post(f"{url}/user/profile/uploadphoto", json=not_jpg)
    return_data = r.json()
    assert return_data['message'] == '<p>Image url is not a jpg!</p>'
    
