import pytest
from database import *
from utility import *
from user import *
from error import AccessError, InputError
from auth import *
from other import clear


def test_user_profile_invalid_u_id():
    clear()
    with pytest.raises(InputError):
        user_profile(0, 0)


def test_user_profile_success():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    user = auth_register('validee@gmail.com', '124abc!@#', 
    'Hay', 'Eve')
    assert user_profile(user['token'], 1) == {
        'user': {
        	'u_id': 1,
        	'email': 'validee@gmail.com',
        	'name_first': 'Hay',
        	'name_last': 'Eve',
        	'handle_str': 'hayeve',
        },
    }


def test_user_profile_setname_first_name_too_long():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    with pytest.raises(InputError):
        user_profile_setname(user['token'], 'Haydennnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn', 'Jaycob')


def test_user_profile_setname_last_name_too_long():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    with pytest.raises(InputError):
        user_profile_setname(user['token'], 'Hay', 'Evvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')


def test_user_profile_setname_success():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    user_profile_setname(user['token'], 'John', 'Smith')
    newuser = data_user(user['u_id'])
    assert newuser['name_first'] == 'John'
    assert newuser['name_last'] == 'Smith'


def test_user_profile_setemail_invalid_email():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], 'invalidemailgmail.com')


def test_user_profile_setemail_already_used():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth_register('validemail2@gmail.com', '123abc!@#', 
    'Dennis', 'Lin')
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], 'validemail2@gmail.com')


def test_user_profile_setemail_success():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    assert len(data['users']) == 1
    user_profile_setemail(user['token'], 'abcdefg@gmail.com')
    assert data['users'][0]['email'] == 'abcdefg@gmail.com'


def test_user_profile_sethandle_too_long():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], 'abcdefghijklmnopqrstuvwxyz')


def test_user_profile_sethandle_too_short():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], 'ab')


def test_user_profile_sethandle_already_used():
    clear()
    auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    assert len(data['users']) == 1
    user = data['users'][0]
    auth_register('validemail2@gmail.com', '123abc!@#', 
    'Dennis', 'Lin')
    handle_been_used = data['users'][1]['handle']
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], handle_been_used)


def test_user_profile_sethandle_success():
    clear()
    auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    user = data['users'][0]
    user_profile_sethandle(user['token'], 'abcdefg')
    assert user['handle'] == 'abcdefg'

def test_user_profile_uploadphoto_wrong_dimension():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    user_uploadphoto(user['token'], 'http://images.tritondigitalcms.com/6616/sites/356/2017/07/28103713/Rick-Astley.jpg', x_start, y_start, x_end, y_end)