import auth
import channel
import pytest
import error
import channels
from message import message_send

def test_invalid_id_channel_details():
    result = auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channel_id = channels.channels_create('result.token', 
             'validchannelname', 'is_public')
    with pytest.raises(InputError) as e:
        assert channel.channel_details('result.token', 'channel_id + 1')
        
def test_unauthorised_channel_details():#needs help
    result = auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channel_id = channels.channels_create('anothertoken', 
             'validchannelname', 'is_private')
    with pytest.raises(AccessError) as a:
        assert channel.channel_details('result.token', 'channel_id')  
      
def test_channel_details():
    channel_id = channels.channels_create('token', 
             'validchannelname', 'is_public')
    assert channel.channel_details("token", "channel_id") == "validchannelname", "owner_members", "all_members"

def test_invalid_id_channel_messages():
    channel_id = channels.channels_create('token', 
             'validchannelname', 'is_public')
    with pytest.raises(InputError) as e:
        assert channel.channel_messages('token', 'wrong_channel_id',
                                        'start')
        
def test_invalid_start_channel_messages():
    channel_id = channels.channels_create('token', 
             'validchannelname', 'is_public')
    with pytest.raises(InputError) as e:
        assert channel.channel_messages('token', 'channel_id', '999')
        
def test_unauthorised_channel_messages():
    channel_id = channels.channels_create('anothertoken', 
             'validchannelname', 'is_private')
    with pytest.raises(AccessError) as a:
        assert channel.channel_messages('token', 'channel_id', 'start') 
        
def test_channel_messages():
    channel_id = channels.channels_create('token', 
             'validchannelname', 'is_public')
    message.message_send('token', 'channel_id', 'message')
    assert channel.channel_messages("token", "channel_id", 'start') ==  
                                    "message", 'start', 'end'
 
    
    
    
    
    
    
    
    
    
           

