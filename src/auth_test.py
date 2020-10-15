import pytest
from auth import auth_register, auth_login, auth_logout
from database import data

def test_register():
    global data
    data['users'].clear()

    # Valid information has been summitted to register from the first user
    info = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    assert info == {'u_id': 0, 'token': '0'}

    # Vadid information has been summitted to register from the second user
    info = auth_register("billgates@outlook.com", "VukkFs", "Bill", "Gates")
    assert info == {'u_id': 1, 'token': '1'}

    # Vadid information has been summitted to register from the third user
    info = auth_register("johnson@icloud.com", "RFVtgb45678", "M", "Johnson")
    assert info == {'u_id': 2, 'token': '2'}

    # Test the number of users
    assert len(data['users']) == 3

    # Invalid email
    with pytest.raises(Exception):
        auth_register("ufhsdfkshfdhfsfhiw", "uf89rgu", "Andrew", "Williams")    


    # Email has already used to register by another users
    auth_register("uniisfun@gmail.com", "ILoveUniversity", "Hayden", "Smith")
    with pytest.raises(Exception):
        auth_register("uniisfun@gmail.com", "uf89rgus", "Andrew", "Williams")

    # Password is below 6 characters in length
    with pytest.raises(Exception):
        auth_register("floralamb@hotmail.com", "uf9du", "Andrew", "Williams")

    # First name is less than 1 characters in length
    with pytest.raises(Exception):
        auth_register("xiaolonglin@qq.com", "ijdhfjhfwehf", "", "Lin")

    # Last name is less than 1 characters in length
    with pytest.raises(Exception):
        auth_register("raymond@gmail.com", "ijdhfjhfwehf", "Raymond", "")

    # First name is above 50 characters in length
    with pytest.raises(Exception):
        auth_register("KeisekuKagawa@yahoo.com", "jdsfjigI8dfsa", "K" * 51, "Honda")

    # Last name is above 50 characters in length
    with pytest.raises(Exception):
        auth_register("josemourinho@gmail.com", "ParktheBus", "Jose", "m" * 51)


    # Test the number of users again
    assert len(data['users']) == 4

    # User's new handle when there is a equivalent name of existent user in the data base
    auth_register("uniisnotfunatall@gmail.com", "IHateUniversity", "Hayden", "Smith")
    assert data['users'][4]['handle'] == 'hayden4'

def test_login():
    global data
    data['users'].clear()


    # Register then normal login
    info = auth_register("france@germany.com", "sdfage9sgdfff", "France", "Germany")
    assert auth_login("france@germany.com", "sdfage9sgdfff") == info

    # Register then provided an invalid email to log in
    info = auth_register("iloveyou@gmail.com", "Idontloveyou", "Jonh", "Sheppard")
    with pytest.raises(Exception):
        auth_login("iloveyou.gmail.com", "Idontloveyou")

    # Register then provided an email which has not been registered
    info = auth_register("francoise@gmail.com", "Idfasdjfksdj0dfd", "Francoise", "Sheppard")
    with pytest.raises(Exception):
        auth_login("francois@gmail.com", "Idfasdjfksdj0dfd")

    # Register then provided an email with a wrong password to login
    info = auth_register("eviedunstone@gmail.com", "Qwerty6", "Evie", "Dunstone")
    with pytest.raises(Exception):
        auth_login("eviedunstone@gmail.com", "Qwerty8")

def test_logout():
    global data
    data['users'].clear()

    # Register, login then logout
    info = auth_register("linliangming@163.com", "edfjkjfkdjfked", "Liangming", "Lin")
    auth_login("linliangming@163.com", "edfjkjfkdjfked")
    assert auth_logout(info['token']) == {'is_success': True}

    # Register, then logout without log in
    info = auth_register("yhn@abc.com", "ujmsdfwer", "Younghyie", "Ngo")
    assert auth_logout(info['token']) == {'is_success': False}

    # Register, login, logout then logout again
    info = auth_register("skysport@gmail.com", "Welovesport", "Sky", "Sport")
    auth_login("skysport@gmail.com", "Welovesport")
    auth_logout(info['token'])
    assert auth_logout(info['token']) == {'is_success': False}

