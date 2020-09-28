import pytest
from src.auth import auth_register
from src.database import data

def test_register():
    # Valid information has been summitted to register from the first user
    info = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "Wu")
    assert info =={'u_id': 0}

    # Vadid information has been summitted to register from the second user
    info = auth_register("billgates@outlook.com", "VukkFsrwa", "Bill", "Gates")
    assert info =={'u_id': 1}

    # Vadid information has been summitted to register from the third user
    info = auth_register("Monique.Johnson@icloud.com", "RFVtgb45678", "Monique", "Johnson")
    assert info =={'u_id': 2}

    # Test the number of users
    assert len(data['users']) == 3

    # Invalid email
    with pytest.raise(Exception):
        auth_register("ufhsdfkshfdhfsfhiw", "uf89rgu", "Andrew", "Williams")    

    # Email has already used to register by another users
    auth_register("uniisfun@ad.unsw.edu.au", "ILoveUniversity", "Hayden", "Smith")
    with pytest.raise(Exception):
        auth_register("uniisfun@ad.unsw.edu.au", "uf89rgus", "Andrew", "Williams")
    
    # Password is below 8 characters in length
    with pytest.raise(Exception):
        auth_register("Flora.Lamb@hotmail.com", "uf89rgu", "Andrew", "Williams")

    # Password is above 50 characters in length
    with pytest.raise(Exception):
        auth_register("xiaolonglin@qq.com", "i" * 51, "Xiaolong", "Lin")

    # First name is above 50 characters in length
    with pytest.raise(Exception):
        auth_register("KeisekuKagawa@yahoo.com", "jdsfjigI8dfsa", "K" * 51, "Honda")

    # First name is empty
    with pytest.raise(Exception):
        auth_register("RealCR7@outlook.com", "djasdfsaffiogo9kjjf", "", "Ronaldo")    

    # Last name is above 50 characters in length
    with pytest.raise(Exception):
        auth_register("josemourinho@gmail.com", "ParktheBus", "Jose", "m" * 51)  

    # Last name is empty
    with pytest.raise(Exception):
        auth_register("Mino.Raiola", "BestAgentEver", "Mino", "")   
    
