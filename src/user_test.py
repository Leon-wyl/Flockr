import user
from database import data
from error import AccessError, InputError
import auth
from other import clear

def user_profile_invalid_u_id():
    clear()
    with pytest.raises(InputError):
        assert user.user_profile(0, 0)

def user_profile_success():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    assert user.user_profile(0, 0) == {
        'user': {
        	'u_id': 0,
        	'email': 'validemail@gmail.com',
        	'name_first': 'Hayden',
        	'name_last': 'Everest',
        	'handle_str': 'hjacobs',
        },
    }
def user_profile_setname_first_name_too_long():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    user = auth.auth_login('validemail@gmail.com', '123abc!@#')
    with pytest.raises(InputError):
        user_profile_setname(user['token'], Haydennnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn, Jaycob)

def user_profile_setname_last_name_too_long():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    user = auth.auth_login('validemail@gmail.com', '123abc!@#')
    with pytest.raises(InputError):
        user_profile_setname(user['token'], Hay, Evvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv)

def user_profile_setname_success():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    user = auth.auth_login('validemail@gmail.com', '123abc!@#')
    user_profile_setname(user['token'], 'John', 'Smith')
    newuser = valid_user(user['u_id'])
    assert newuser['name_first'] == 'John'
    assert newuser['name_last'] == 'Smith'

def user_profile_setemail_invalid_email():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    user = auth.auth_login('validemail@gmail.com', '123abc!@#')
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], 'invalidemailgmail.com')

def user_profile_setemail_already_used():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    user = auth.auth_login('validemail@gmail.com', '123abc!@#')
    auth.auth_register('validemail2@gmail.com', '123abc!@#', 
    'Dennis', 'Lin')
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], 'valid2email@gmail.com')

def user_profile_setemail_success():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    user = auth.auth_login('validemail@gmail.com', '123abc!@#')
    user_profile_setemail(user['token'], 'valid2email@gmail.com')
    newemail = valid_user(user['u_id'])
    assert newemail['email'] == 'valid2email@gmail.com'

def user_profile_sethandle_too_long():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    user = auth.auth_login('validemail@gmail.com', '123abc!@#')
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], 'abcdefghijklmnopqrstuvwxyz')

def user_profile_sethandle_too_short():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    user = auth.auth_login('validemail@gmail.com', '123abc!@#')
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], 'ab')

def user_profile_sethandle_already_used():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    user = auth.auth_login('validemail@gmail.com', '123abc!@#')
    auth.auth_register('validemail2@gmail.com', '123abc!@#', 
    'Dennis', 'Lin')
    handle_been_used = valid_user(user['handle'])
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], handle_been_used)

def user_profile_sethandle_success():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    user = auth.auth_login('validemail@gmail.com', '123abc!@#')
    user_profile_sethandle(user['token'], 'abcdefg')
    handle_changed = valid_user(user['handle'])
    assert handle_changed == 'abcdefg'