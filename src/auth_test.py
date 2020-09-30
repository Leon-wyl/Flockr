import pytest
from src.auth import auth_register, auth_login, data

def test_register():
    data.clear()

    # Valid information has been summitted to register from the first user
    info = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "Wu")
    assert info == {'u_id': 0, 'token': 0}

    # Vadid information has been summitted to register from the second user
    info = auth_register("billgates@outlook.com", "VukkFsrwa", "Bill", "Gates")
    assert info == {'u_id': 1, 'token': 2}

    # Vadid information has been summitted to register from the third user
    info = auth_register("Monique.Johnson@icloud.com", "RFVtgb45678", "Monique", "Johnson")
    assert info == {'u_id': 2, 'token': 2}

    # Test the number of users
    assert len(data['users']) == 3

    # Invalid email
    with pytest.raises(Exception):
        auth_register("ufhsdfkshfdhfsfhiw", "uf89rgu", "Andrew", "Williams")    

    # Email has already used to register by another users
    auth_register("uniisfun@ad.unsw.edu.au", "ILoveUniversity", "Hayden", "Smith")
    with pytest.raises(Exception):
        auth_register("uniisfun@ad.unsw.edu.au", "uf89rgus", "Andrew", "Williams")
    
    # Password is below 6 characters in length
    with pytest.raises(Exception):
        auth_register("Flora.Lamb@hotmail.com", "uf9du", "Andrew", "Williams")

    # Password is above 50 characters in length
    with pytest.raises(Exception):
        auth_register("xiaolonglin@qq.com", "i" * 51, "Xiaolong", "Lin")

    # First name is above 50 characters in length
    with pytest.raises(Exception):
        auth_register("KeisekuKagawa@yahoo.com", "jdsfjigI8dfsa", "K" * 51, "Honda")  

    # Last name is above 50 characters in length
    with pytest.raises(Exception):
        auth_register("josemourinho@gmail.com", "ParktheBus", "Jose", "m" * 51)  

def test_login():
    data.clear()
    
    # Register then normal login
    info = auth_register("france@germany.com", "sdfage9sgdfff", "France", "Germany")
    assert auth_login("FranceGermany.com", "sdfage9sgdfff") == info

    # Register then provided an invalid email to log in
    info = auth_register("Iloveyou@gmail.com", "Idontloveyou", "Jonh", "Sheppard")
    with pytest.raises(Exception):
        auth_login("Iloveyou.gmail.com", "Idontloveyou")

    # Register then provided an email which has not been registered
    info = auth_register("Francoise@gmail.com", "Idfasdjfksdj0dfd", "Jonh", "Sheppard")
    with pytest.raises(Exception):
        auth_login("Francois@gmail.com", "Idfasdjfksdj0dfd")

    # Register then provided an email with a wrong password to login
    info = auth_register("Eviedunstone@gmail.com", "Qwerty6", "Evie", "dunstone")
    with pytest.raises(Exception):
        auth_login("Eviedunstone@gmail.com", "Qwerty8")
