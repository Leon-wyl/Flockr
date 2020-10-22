import user
from database import data
from error import AccessError, InputError
import auth
from other import clear

'''def user_profile_invalid_u_id():
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
'''
    