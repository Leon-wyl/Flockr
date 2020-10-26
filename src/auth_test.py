import pytest
from auth import auth_register, auth_login, auth_logout
from other import clear
from database import data
from utility import token_generate
from error import InputError, AccessError

def test_register():
    clear()

    # Valid information has been summitted to register from the first user
    info = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    assert (info['u_id'] == 0 and info['token'] == token_generate(0))

    # Vadid information has been summitted to register from the second user
    info = auth_register("billgates@outlook.com", "VukkFs", "Bill", "Gates")
    assert (info['u_id'] == 1 and info['token'] == token_generate(1))

    # Vadid information has been summitted to register from the third user
    info = auth_register("johnson@icloud.com", "RFVtgb45678", "M", "Johnson")
    assert (info['u_id'] == 2 and info['token'] == token_generate(2))

    # Test the number of users
    assert len(data['users']) == 3

    # Invalid email
    with pytest.raises(InputError):
        auth_register("ufhsdfkshfdhfsfhiw", "uf89rgu", "Andrew", "Williams")


    # Email has already used to register by another users
    auth_register("uniisfun@gmail.com", "ILoveUniversity", "Hayden", "Smith")
    with pytest.raises(InputError):
        auth_register("uniisfun@gmail.com", "uf89rgus", "Andrew", "Williams")

    # Password is below 6 characters in length
    with pytest.raises(InputError):
        auth_register("floralamb@hotmail.com", "uf9du", "Andrew", "Williams")

    # First name is less than 1 characters in length
    with pytest.raises(InputError):
        auth_register("xiaolonglin@qq.com", "ijdhfjhfwehf", "", "Lin")

    # Last name is less than 1 characters in length
    with pytest.raises(InputError):
        auth_register("raymond@gmail.com", "ijdhfjhfwehf", "Raymond", "")

    # First name is above 50 characters in length
    with pytest.raises(InputError):
        auth_register("KeisekuKagawa@yahoo.com", "jdsfjigI8dfsa", "K" * 51, "Honda")

    # Last name is above 50 characters in length
    with pytest.raises(InputError):
        auth_register("josemourinho@gmail.com", "ParktheBus", "Jose", "m" * 51)


    # Test the number of users again
    assert len(data['users']) == 4

    # User's new handle when there is a equivalent name of existent user in the data base
    auth_register("uniisnotfunatall@gmail.com", "IHateUniversity", "Hayden", "Smith")
    assert data['users'][4]['handle'] == 'hayden4'

def test_login():
    clear()

    # Register then logout then normal login
    info = auth_register("france@germany.com", "sdfage9sgdfff", "France", "Germany")
    auth_logout(info['token'])
    assert auth_login("france@germany.com", "sdfage9sgdfff") == info

    # Register then logout then provided an invalid email to log in
    info = auth_register("iloveyou@gmail.com", "Idontloveyou", "Jonh", "Sheppard")
    auth_logout(info['token'])
    with pytest.raises(InputError):
        auth_login("iloveyou.gmail.com", "Idontloveyou")

    # Register then logout then provided an email which has not been registered
    info = auth_register("francoise@gmail.com", "Idfasdjfksdj0dfd", "Francoise", "Sheppard")
    auth_logout(info['token'])
    with pytest.raises(InputError):
        auth_login("francois@gmail.com", "Idfasdjfksdj0dfd")

    # Register then provided an email with a wrong password to login
    info = auth_register("eviedunstone@gmail.com", "Qwerty6", "Evie", "Dunstone")
    auth_logout(info['token'])
    with pytest.raises(InputError):
        auth_login("eviedunstone@gmail.com", "Qwerty8")

    # Register then logout then login the login again
    info = auth_register("hello@gmail.com", "fsdfsdfsDS23", "Hello", "Hi")
    auth_logout(info['token'])
    auth_login("hello@gmail.com", "fsdfsdfsDS23")
    with pytest.raises(AccessError):
        auth_login("hello@gmail.com", "fsdfsdfsDS23")

def test_logout():
    clear()

    # Register then logout
    info = auth_register("linliangming@163.com", "edfjkjfkdjfked", "Liangming", "Lin")
    assert auth_logout(info['token']) == {'is_success': True}

    # Register then logout 
    info = auth_register("yhn@abc.com", "ujmsdfwer", "Younghyie", "Ngo")
    assert auth_logout(info['token']) == {'is_success': True}

    # Register logout then logout again
    info = auth_register("skysport@gmail.com", "Welovesport", "Sky", "Sport")
    assert auth_logout(info['token']) == {'is_success': True}
    assert auth_logout(data['users'][2]['token']) == {'is_success': False}

    # An invalid token given to logout, which should be fail
    with pytest.raises(AccessError):
        assert auth_logout(token_generate(5))
