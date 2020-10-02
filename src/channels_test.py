import pytest
import channels
import channel
import auth
from database import data
from other import clear

# test if channels can be created successfully
def test_channels_create():
    clear()
    auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    assert channels.channels_create(0, 'first', True) == {'channel_id' : 0}
    assert channels.channels_create(0, 'second', False) == {'channel_id' : 1}
    assert len(data['channels']) == 2

# test if the function raises an Exception if the input is invalid or token is
# invalid
def test_channels_create_except():
    clear()
    auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    with pytest.raises(Exception):
        channels.channels_create(6, 'first', True)
    with pytest.raises(Exception):
        channels.channels_create(0, "jdjdkdidnekdmedkwdemdkeimd", False)

# test if the function returns the correct list of channels that the user is 
# a member of
def test_channels_list():
    clear()
    auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channels.channels_create(0, 'first', True)
    channels.channels_create(0, 'second', True)
    channels.channels_create(0, 'third', True)
    channels.channels_create(0, 'fourth', True)
    channel.channel_join(0, 0)
    channel.channel_join(0, 2)
    user_channel = []
    for single in data['channels']:
        if single['channel_id'] == 0 or single['channel_id'] == 2:
            user_channel.append(single)
    assert user_channel == channels.channels_list(0)['channels']
            
    
# test if the function raises an Exception if token is invalid    
def test_channels_list_except():
    clear()
    auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channels.channels_create(0, 'first', True)
    channels.channels_create(0, 'second', True)
    channels.channels_create(0, 'third', True)
    channels.channels_create(0, 'fourth', True)
    channel.channel_join(0, 0)
    channel.channel_join(0, 2)
    with pytest.raises(Exception):
        channels.channels_list(2)
    
# test if the function returns the correct list of channels
def test_channels_listall():
    clear()
    auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channels.channels_create(0, 'first', True)
    channels.channels_create(0, 'second', True)
    channels.channels_create(0, 'third', True)
    channels.channels_create(0, 'fourth', True)
    assert data['channels'] == channels.channels_listall(0)['channels']
    
  
# test if the function raises an Exception if token is invalid       
def test_channels_listall_except():
    clear()
    auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channels.channels_create(0, 'first', True)
    channels.channels_create(0, 'second', True)
    with pytest.raises(Exception):
        channels.channels_listall(2)['channels']




