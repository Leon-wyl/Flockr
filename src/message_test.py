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
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    with pytest.raises(InputError):
        assert message.message_send(info['token'], channel_id['channel_id'], 'abcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghioabcdefghio') 

# Test if message_send function raises an AccessError when the authorised user has not joined the channel they are trying to post to
def test_unauthorised_message_send():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    secondinfo = auth.auth_register("guanbin@gmail.com", "ttteh3hgi00d", "Billy", "Gale")  
    with pytest.raises(AccessError):
        assert message.message_send(secondinfo['token'], channel_id['channel_id'], 'hello') 

def test_message_send():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    assert message.message_send(info['token'], channel_id['channel_id'], 'hello') == {'message_id':0}
    assert message.message_send(info['token'], channel_id['channel_id'], 'My name') == {'message_id':1}
    assert message.message_send(info['token'], channel_id['channel_id'], '1s sam!') == {'message_id':2}
    assert channel.channel_messages(info['token'], channel_id['channel_id'], 0) == {'end': -1, 'message_list': [{'message': 'hello', 'message_id': 0, 'time_created': 0, 'u_id': 0}, {'message': 'My name', 'message_id': 1, 'time_created': 0, 'u_id': 0}, {'message': '1s sam!', 'message_id': 2, 'time_created': 0, 'u_id': 0}], 'start': 0}

def test_message_send2():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    i = 0
    while i < 51:
        message.message_send(info['token'], channel_id['channel_id'], 'hello')
        i += 1
    print(channel.channel_messages(info['token'], channel_id['channel_id'], 0))
    assert len(channel.channel_messages(info['token'], channel_id['channel_id'], 0)['message_list']) \
        == 50

# Test if message_remove function raises an InputError when the message (based on ID) no longer exists
def test_invalid_message_remove():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    with pytest.raises(InputError):
        assert message.message_remove(info['token'], 0)
    firstmessage = message.message_send(info['token'], channel_id['channel_id'], 'hello')
    message.message_remove(info['token'], firstmessage['message_id'])
    with pytest.raises(InputError):
        assert message.message_remove(info['token'], firstmessage['message_id'])
            
# Test if message_remove function raises an AccessError when the user is not the authorised user making this request nor an owner of this channel or the flockr
def test_unauthorised_message_remove():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    firstmessage = message.message_send(info['token'], channel_id['channel_id'], 'hello')
    secondinfo = auth.auth_register("guanbin@gmail.com", "ttteh3hgi00d", "Billy", "Gale")  
    with pytest.raises(AccessError):
        assert message.message_remove(secondinfo['token'], firstmessage['message_id'])
         
def test_message_remove():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    second_channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    secondinfo = auth.auth_register("guanbin@gmail.com", "ttteh3hgi00d", "Billy", "Gale")  
    channel.channel_join(secondinfo['token'], second_channel_id['channel_id'])
    firstmessage = message.message_send(secondinfo['token'], second_channel_id['channel_id'], 'hello')
    message.message_remove(secondinfo['token'], firstmessage['message_id'])
    assert len(data['channels'][1]['messages']) == 0
    secondmessage = message.message_send(secondinfo['token'], second_channel_id['channel_id'], 'second')
    message.message_remove(info['token'], secondmessage['message_id'])
    assert len(data['channels'][1]['messages']) == 0
    thirdmessage = message.message_send(secondinfo['token'], second_channel_id['channel_id'], 'third')
    assert len(data['channels'][1]['messages']) == 1

# Test if message_edit function raises an AccessError when the user is not the authorised user making this request nor an owner of this channel or the flockr
def test_unauthorised_message_edit():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    firstmessage = message.message_send(info['token'], channel_id['channel_id'], 'hello')
    secondinfo = auth.auth_register("guanbin@gmail.com", "ttteh3hgi00d", "Billy", "Gale")  
    with pytest.raises(AccessError):
        assert message.message_edit(secondinfo['token'], firstmessage['message_id'], 'changing')
        
def test_message_edit():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    second_channel_id = channels.channels_create(info['token'], 'validchannel', True)
    secondinfo = auth.auth_register("guanbin@gmail.com", "ttteh3hgi00d", "Billy", "Gale")  
    channel.channel_join(secondinfo['token'], second_channel_id['channel_id'])
    firstmessage = message.message_send(secondinfo['token'], second_channel_id['channel_id'], 'first')
    secondmessage = message.message_send(secondinfo['token'], second_channel_id['channel_id'], 'second')
    thirdmessage = message.message_send(secondinfo['token'], second_channel_id['channel_id'], 'third')
    message.message_edit(secondinfo['token'], firstmessage['message_id'], 'changed1st')
    message.message_edit(info['token'], secondmessage['message_id'], 'changed2nd')
    message.message_edit(info['token'], thirdmessage['message_id'], '')
    assert len(data['channels'][1]['messages']) == 2
    assert channel.channel_messages(info['token'], second_channel_id['channel_id'], 0) == \
    {
        'message_list': 
            [{
                'message_id': 0,
                'u_id': 1,
                'message': 'changed1st',
                'time_created': 0,
            }, 
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'changed2nd',
                'time_created': 0,
            }],
        'start': 0,
        'end': -1,
    }

        