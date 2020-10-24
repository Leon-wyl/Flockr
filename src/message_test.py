import auth
import channel
import channels
import pytest
import message
from error import InputError
from error import AccessError
from database import data
from other import clear

# Test if message_send function raises an InputError when the message is more than 1000 characters. 
def test_invalid_long_message():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    with pytest.raises(InputError):
        assert message.message_send(info['token'], channel_id, 'abcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghio') 

# Test if message_send function raises an AccessError when the authorised user has not joined the channel they are trying to post to
def test_unauthorised_message_send():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    secondinfo = auth.auth_register("guanbin@gmail.com", "ttteh3hgi00d", "Billy", "Gale")  
    auth.auth_login("guanbin@gmail.com", "ttteh3hgi00d") 
    with pytest.raises(AccessError):
        assert message.message_send(secondinfo['token'], channel_id, 'hello') 

def test_message_send():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    assert message.message_send(info['token'], channel_id, 'hello') == 0
    assert message.message_send(info['token'], channel_id, 'My name') == 1
    assert message.message_send(info['token'], channel_id, '1s sam!') == 2
    assert channel.channel_messages(info['token'], channel_id, 0) == {{ 0, 0, 'hello' }, { 1, 0, 'My name' }, { 2, 0, '1s sam!' }}
            
# Test if message_remove function raises an InputError when the message (based on ID) no longer exists
def test_invalid_message_remove():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    with pytest.raises(InputError):
        assert message.message_remove(info['token'], 0)
    firstmessage = message.message_send(info['token'], channel_id, 'hello')
    message.message_remove(info['token'], firstmessage)
    with pytest.raises(InputError):
        assert message.message_remove(info['token'], firstmessage)
            
# Test if message_remove function raises an AccessError when the user is not the authorised user making this request nor an owner of this channel or the flockr
def test_unauthorised_message_remove():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    firstmessage = message.message_send(info['token'], channel_id, 'hello')
    secondinfo = auth.auth_register("guanbin@gmail.com", "ttteh3hgi00d", "Billy", "Gale")  
    auth.auth_login("guanbin@gmail.com", "ttteh3hgi00d") 
    with pytest.raises(AccessError):
        assert message.message_remove(secondinfo['token'], firstmessage)
         
def test_message_remove():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    secondinfo = auth.auth_register("guanbin@gmail.com", "ttteh3hgi00d", "Billy", "Gale")  
    auth.auth_login("guanbin@gmail.com", "ttteh3hgi00d")
    channel.channel_join(info['token'], channel_id)
    firstmessage = message.message_send(secondinfo['token'], channel_id, 'hello')
    secondmessage = message.message_send(secondinfo['token'], channel_id, 'second')
    thirdmessage = message.message_send(secondinfo['token'], channel_id, 'third')
    message.message_remove(secondinfo['token'], firstmessage)
    message.message_remove(info['token'], secondmessage)
    assert len(data['channels'][0]['messages']) == 1

# Test if message_edit function raises an AccessError when the user is not the authorised user making this request nor an owner of this channel or the flockr
def test_unauthorised_message_edit():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    firstmessage = message.message_send(info['token'], channel_id, 'hello')
    secondinfo = auth.auth_register("guanbin@gmail.com", "ttteh3hgi00d", "Billy", "Gale")  
    auth.auth_login("guanbin@gmail.com", "ttteh3hgi00d") 
    with pytest.raises(AccessError):
        assert message.message_edit(secondinfo['token'], firstmessage)
        
def test_message_edit():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    auth.auth_login("leonwu@gmail.com", "ihfeh3hgi00d")
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    secondinfo = auth.auth_register("guanbin@gmail.com", "ttteh3hgi00d", "Billy", "Gale")  
    auth.auth_login("guanbin@gmail.com", "ttteh3hgi00d")
    channel.channel_join(info['token'], channel_id)
    firstmessage = message.message_send(secondinfo['token'], channel_id, 'first')
    secondmessage = message.message_send(secondinfo['token'], channel_id, 'second')
    thirdmessage = message.message_send(secondinfo['token'], channel_id, 'third')
    message.message_edit(secondinfo['token'], firstmessage, 'changed1st')
    message.message_edit(info['token'], secondmessage, 'changed2nd')
    message.message_edit(info['token'], thirdmessage, '')
    assert len(data['channels'][0]['messages']) == 2
    assert channel.channel_messages(info['token'], channel_id, 0) == {}
        
