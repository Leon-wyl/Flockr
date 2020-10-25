from other import *
from auth import *
from channels import *
from channel import *
from database import *
from error import AccessError, InputError
from other import clear
from message import message_send
import pytest

# Test users_all function
def test_users_all():
    clear()
    auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    info2 = auth_register("johnson@icloud.com", "RFVtgb45678", "M", "Johnson")
    auth_login("johnson@icloud.com", "RFVtgb45678")
    assert users_all(info2['token']) == {'users': [
        {
            'u_id': 0,
            'email': "leonwu@gmail.com",
            'name_first': "Yilang",
            'name_last': "W",
            'handle_str': 'yilangw',
         },
         {
            'u_id': 1,
            'email': "johnson@icloud.com",
            'name_first': "M",
            'name_last': "Johnson",
            'handle_str': 'mjohnson',
         }
        
    ]}
    
# Test invalid token    
def test_users_all_except():
    clear()
    auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    info2 = auth_register("johnson@icloud.com", "RFVtgb45678", "M", "Johnson")
    auth_login("johnson@icloud.com", "RFVtgb45678")
    with pytest.raises(AccessError):
        users_all(info2['token'] + 'a')
    
# test the number of channels and users in database
def test_clear():
    clear()
    assert channel_numbers() == 0
    assert data_u_id() == 0       
 
# test if the admin_userpermission_change correctly
def test_admin_userpermission_change():
    clear()
    info1 = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    auth_register("johnson@icloud.com", "RFVtgb45678", "M", "Johnson")
    auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    assert data_permission(1) == 2
    admin_userpermission_change(info1['token'], 1, 1)
    assert data_permission(1) == 1
 
def test_admin_userpermission_change_invalid_token():
    clear()
    info1 = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    auth_register("johnson@icloud.com", "RFVtgb45678", "M", "Johnson")
    auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    with pytest.raises(AccessError):
        admin_userpermission_change(info1['token'] + 'a', 1, 1)
 
def test_admin_userpermission_change_invalid_user():
    clear()
    info1 = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    auth_register("johnson@icloud.com", "RFVtgb45678", "M", "Johnson")
    auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    with pytest.raises(InputError):
        admin_userpermission_change(info1['token'], 3, 1) 
 
def test_admin_userpermission_change_invalid_permission():
    clear()
    info1 = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    auth_register("johnson@icloud.com", "RFVtgb45678", "M", "Johnson")
    auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    with pytest.raises(InputError):
        admin_userpermission_change(info1['token'], 1, 3) 
 
def test_admin_userpermission_change_not_owner():
    clear()
    auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    info2 = auth_register("johnson@icloud.com", "RFVtgb45678", "M", "Johnson")
    auth_login("johnson@icloud.com", "RFVtgb45678")
    with pytest.raises(AccessError):
        admin_userpermission_change(info2['token'], 0, 2)    
    
# test if the function return correct messages   
def test_search():
    clear()
    info1 = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    info2 = auth_register("johnson@icloud.com", "RFVtgb45678", "M", "Johnson")
    auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    auth_login("johnson@icloud.com", "RFVtgb45678")
    channels_create(info2['token'], 'first', True)
    channels_create(info2['token'], 'second', True)
    channels_create(info1['token'], 'third', True)
    channels_create(info1['token'], 'fourth', True)
    message_send(info2['token'], 0, "I am ok haha")
    message_send(info2['token'], 0, "he is ok haha")
    message_send(info2['token'], 0, "Old man and sea")
    message_send(info2['token'], 1, "bangindgdliok")
    message_send(info2['token'], 1, "Fast and furious")
    message_send(info2['token'], 1, "ok in abcdefg")
    assert search(info2['token'], 'ok') == {'messages': [
        {
            'message_id': 0,
            'u_id': 1,
            'message': "I am ok haha",
            'time_created': 0,
        },
        {
            'message_id': 1,
            'u_id': 1,
            'message': "he is ok haha",
            'time_created': 0,
        },
        {
            'message_id': 3,
            'u_id': 1,
            'message': "bangindgdliok",
            'time_created': 0,
        },
        {
            'message_id': 5,
            'u_id': 1,
            'message': "ok in abcdefg",
            'time_created': 0,
        },   
    ]}

# test if function raises Exception if the token is invalid
def test_search_except():
    clear()
    info1 = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    info2 = auth_register("johnson@icloud.com", "RFVtgb45678", "M", "Johnson")
    auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    auth_login("johnson@icloud.com", "RFVtgb45678")
    channels_create(info2['token'], 'first', True)
    channels_create(info2['token'], 'second', True)
    channels_create(info1['token'], 'third', True)
    channels_create(info1['token'], 'fourth', True)
    message_send(info2['token'], 0, "I am ok haha")
    message_send(info2['token'], 0, "he is ok haha")
    message_send(info2['token'], 0, "Old man and sea")
    message_send(info2['token'], 1, "bangindgdliok")
    with pytest.raises(AccessError):
        search(info2['token'] + 'a', 'ok')

