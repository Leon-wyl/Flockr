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
            'profile_img_url': data['users'][1]['profile_img_url']
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


def test_user_profile_uploadphoto_success():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    user_profile_uploadphoto(user['token'], 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg', 0, 0, 500, 500)
    assert data['users'][0]['profile_img_url'] == 'static/0.jpg'


# test if uploadphoto output wrong HTTP status when given invalid urls
def test_user_profile_uploadphoto_invalid_url():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], 'https://img1..jpg', 0, 0, 0, 0)

def test_user_profile_uploadphoto_not_jpg():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], 'https://cdn.vox-cdn.com/thumbor/J2XSqgAqREtpkGAWa6rMhkHA1Y0=/0x0:1600x900/1400x933/filters:focal(672x322:928x578):no_upscale()/cdn.vox-cdn.com/uploads/chorus_image/image/66320060/Tanjiro__Demon_Slayer_.0.png', 0, 0, 500, 500)

    
# wrong dimension
def test_user_profile_uploadphoto_x_end_exceeded():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg', 0, 0, 50000, 500)


def test_user_profile_uploadphoto_y_end_exceeded():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg', 0, 0, 500, 50000)


def test_user_profile_uploadphoto_x_end_negative():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg', 0, 0, -1, 500)


def test_user_profile_uploadphoto_y_end_negative():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg', 0, 0, 500, -1)


def test_user_profile_uploadphoto_x_start_exceeded():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg', 50000, 0, 500, 500)


def test_user_profile_uploadphoto_y_start_exceeded():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg', 0, 50000, 500, 500)


def test_user_profile_uploadphoto_x_start_negative():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg', -1, 0, 500, 500)


def test_user_profile_uploadphoto_x_start_negative():
    clear()
    user = auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    with pytest.raises(InputError):
        user_profile_uploadphoto(user['token'], 'https://img1.looper.com/img/gallery/things-only-adults-notice-in-shrek/intro-1573597941.jpg', 0, -1, 500, 500)

