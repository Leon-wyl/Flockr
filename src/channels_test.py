import pytest
import channels
import channel
import auth
from database import data
from other import clear


def test_channels_create():
    clear()
    auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    assert channels.channels_create(1, first, True) == {'channel_id' : 1}
    assert channels.channels_create(1, second, False) == {'channel_id' : 2}
    assert len(data['channels']) == 2

def test_channels_create_except():
    clear()
    auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    with pytest.raises(Exception):
        channels.channels_create(6, first, True)
    with pytest.raises(Exception):
        channels.channels_create(1, "jdjdkdidnekdmedkwdemdkeimd", False)

def test_channels_list():
    clear()
    auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channels.channels_create(1, first, True)
    channels.channels_create(1, second, True)
    channels.channels_create(1, third, True)
    channels.channels_create(1, fourth, True)
    channel.channel_join(1, 1)
    channel.channel_join(1, 3)
    user_channel = []
    for single in data['channels']:
        if single['channel_id'] == 1 or single['channel_id'] == 3:
            user_channel.append(single)
    assert user_channel == channels.channels_list(1)['channels']
            
    
    
def test_channels_list_except():
    clear()
    auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channels.channels_create(1, first, True)
    channels.channels_create(1, second, True)
    channels.channels_create(1, third, True)
    channels.channels_create(1, fourth, True)
    channel.channel_join(1, 1)
    channel.channel_join(1, 3)
    with pytest.raises(Exception):
        channels.channels_list(2)
    

def test_channels_listall():
    clear()
    auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channels.channels_create(1, first, True)
    channels.channels_create(1, second, True)
    channels.channels_create(1, third, True)
    channels.channels_create(1, fourth, True)
    assert data['channels'] == channels.channels_listall(1)['channels']
    
    
    
    
def test_channels_listall_except():
    clear()
    auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channels.channels_create(1, first, True)
    channels.channels_create(1, second, True)
    with pytest.raises(Exception):
        channels.channels_listall(2)['channels']

