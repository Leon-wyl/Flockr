from other import *
from auth import *
from channels import *
from channel import *
from database import *
from error import AccessError, InputError
from other import clear
import pytest

def test_users_all():
    clear()
    auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    auth_register("johnson@icloud.com", "RFVtgb45678", "M", "Johnson")
    auth_login("johnson@icloud.com", "RFVtgb45678")
    assert users_all('1') == {'users': [
        {
            'u_id': 0,
            'email': "leonwu@gmail.com",
            'name_first': "Yilang",
            'name_last': "W",
            'handle_str': 'hjacobs',
         },
         {
            'u_id': 1,
            'email': "johnson@icloud.com",
            'name_first': "M",
            'name_last': "Johnson",
            'handle_str': 'hjacobs',
         }
        
    ]}
    
    
def test_users_all_except():
    clear()
    info1 = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    info2 = auth_register("johnson@icloud.com", "RFVtgb45678", "M", "Johnson")
    auth_login("johnson@icloud.com", "RFVtgb45678")
    with pytest.raises(AccessError):
        users_all(info1['token'] + 'a')
    
    

    
    
    
    
    
    
    
    
    
    
