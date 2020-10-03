import auth
import channel
import pytest
from error import InputError
from error import AccessError
import channels
from database import data
from other import clear

# Test if the function raises an Input Error if the channel id is invalid.
def test_invalid_id_channel_details():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    channel.channel_join(0,0)
    with pytest.raises(InputError) as e:
        assert channel.channel_details(0, 6)

# Test if the function raises an Access Error if user is unauthorised to view the channel details.      
def test_unauthorised_channel_details():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', False)
    auth.auth_register('newemail@gmail.com', '234abc!@#', 
    'Guanbin', 'Wen')
    auth.auth_login('newemail@gmail.com', '234abc!@#')
    with pytest.raises(AccessError) as a:
        assert channel.channel_details(1, 0)  
# Test if the function functions normally with two members in the channel.   
def test_channel_details():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    auth.auth_register('newemail@gmail.com', '234abc!@#', 
    'Guanbin', 'Wen')
    auth.auth_login('newemail@gmail.com', '234abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    channel.channel_join(0,0)
    channel.channel_join(1,0)
    assert channel.channel_details(0, 0) == {
        'name':'validchannelname',
        'owner_members': [],
        'all_members': [{'u_id': 0, 'name_first': 'Hayden', 'name_last': 'Everest'}, {'u_id': 1, 'name_first': 'Guanbin', 'name_last': 'Wen'}]
    }
    
def test_invalid_id_channel_messages():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    channel.channel_join(0,0)
    with pytest.raises(InputError) as e:
        assert channel.channel_messages(0, 6, 0)
        
def test_invalid_start_channel_messages():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    channel.channel_join(0,0)
    with pytest.raises(InputError) as e:
        assert channel.channel_messages(0, 0, 9)
       
def test_unauthorised_channel_messages():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    with pytest.raises(AccessError) as a:
        assert channel.channel_messages(1, 0, 0) 



'''   
def test_channel_messages():
    channel_id = channels.channels_create('token', 
             'validchannelname', 'is_public')
    message.message_send('token', 'channel_id', 'message')
    assert channel.channel_messages("token", "channel_id", 'start') ==  
                                    "message", 'start', 'end'
                                    ''''''
                                    '''   

