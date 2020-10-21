import pytest
import channels
import channel
import auth
from error import InputError
from error import AccessError
from database import data
from other import clear

# test if channels can be created successfully
def test_channels_create():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    assert channels.channels_create(info['token'], 'first', True) == {'channel_id' : 0}
    assert channels.channels_create(info['token'], 'second', False) == {'channel_id' : 1}
    assert channel_numbers() == 2

# test if the function raises an Exception if the input is invalid or token is
# invalid
def test_channels_create_except():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    with pytest.raises(AccessError):
        channels.channels_create(info['token'] + 'a', 'first', True)
    with pytest.raises(InputError):
        channels.channels_create(info['token'], "jdjdkdidnekdmedkwdemdkeimd", False)

# test if the function returns the correct list of channels that the user is
# a member of
def test_channels_list():
    clear()
    info1 = auth.auth_register("eviedunstone@gmail.com", "Qwerty6", "Evie", "Dunstone")
    info2 = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    auth.auth_login("eviedunstone@gmail.com", "Qwerty6")
    channels.channels_create(info1['token'], 'first', True)
    channels.channels_create(info1['token'], 'second', True)
    channels.channels_create(info1['token'], 'third', True)
    channels.channels_create(info1['token'], 'fourth', True)
    channel.channel_join(info2['token'], 0)
    channel.channel_join(info2['token'], 2)
    assert channels.channels_list(info2['token'])['channels'] == \
    [{'channel_id': 0, 'name': 'first'},
     {'channel_id': 2, 'name': 'third'}]


# test if the function raises an Exception if token is invalid
def test_channels_list_except():
    clear()
    info1 = auth.auth_register("eviedunstone@gmail.com", "Qwerty6", "Evie", "Dunstone")
    info2 = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    auth.auth_login("eviedunstone@gmail.com", "Qwerty6")
    channels.channels_create(info1['token'], 'first', True)
    channels.channels_create(info1['token'], 'second', True)
    channels.channels_create(info1['token'], 'third', True)
    channels.channels_create(info1['token'], 'fourth', True)
    channel.channel_join(info2['token'], 0)
    channel.channel_join(info2['token'], 2)
    with pytest.raises(AccessError):
        channels.channels_list(info2['token'] + 'a')

# test if the function returns the correct list of channels
def test_channels_listall():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channels.channels_create(info['token'], 'first', True)
    channels.channels_create(info['token'], 'second', True)
    channels.channels_create(info['token'], 'third', True)
    channels.channels_create(info['token'], 'fourth', True)
    assert channels.channels_listall(info['token'])['channels'] == \
    [{'channel_id': 0, 'name': 'first'},
     {'channel_id': 1, 'name': 'second'},
     {'channel_id': 2, 'name': 'third'},
     {'channel_id': 3, 'name': 'fourth'}]


# test if the function raises an Exception if token is invalid
def test_channels_listall_except():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channels.channels_create(info['token'], 'first', True)
    channels.channels_create(info['token'], 'second', True)
    with pytest.raises(AccessError):
        channels.channels_listall(info['token'] + 'a')



