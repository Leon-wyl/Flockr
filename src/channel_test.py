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

# Test if the function raises an Input Error if the channel id is invalid.    
def test_invalid_id_channel_messages():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    channel.channel_join(0,0)
    with pytest.raises(InputError) as e:
        assert channel.channel_messages(0, 6, 0)

# Test if the function raises an Input Error if the start of message is invalid.        
def test_invalid_start_channel_messages():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    channel.channel_join(0,0)
    with pytest.raises(InputError) as e:
        assert channel.channel_messages(0, 0, 9)

# Test if the function raises an Access Error if user is unauthorised to view the channel messages.          
def test_unauthorised_channel_messages():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    with pytest.raises(AccessError) as a:
        assert channel.channel_messages(1, 0, 0) 
        
# This is not testable as message.message_send function is not yet implemented, will exclude this test for now and write in assumption 
'''  
def test_channel_messages():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    channel.channel_join(0,0)
    message.message_send()
    data['channels'][0]['messages'].append(new_message)
    assert channel.channel_messages(0, 0, 0) == {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': -1,
    }
'''
# Test if the function raises an Input Error if the channel id is invalid.
def test_invalid_id_channel_addowner():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    channel.channel_join(0,0)
    with pytest.raises(Exception) as e:
        assert channel.channel_addowner(0, 6, 0)

# Test if the function raises an Input Error if the user is already an owner of the channel.

def test_already_owner_channel_addowner():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    channel.channel_join(0,0)
    new_owner = data['users'][0]
    data['channels'][0]['owners'].append(new_owner)
    with pytest.raises(Exception) as e:
        assert channel.channel_addowner(0, 0, 0)

# Test if the function raises an Access Error if user is unauthorised to add owner to this channel.      
def test_unauthorised_channel_addowner():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    channel.channel_join(0,0)
    new_owner = data['users'][0]
    data['channels'][0]['owners'].append(new_owner)
    auth.auth_register('newemail@gmail.com', '234abc!@#', 
    'Guanbin', 'Wen')
    auth.auth_login('newemail@gmail.com', '234abc!@#')
    channel.channel_join(0,0) 
    with pytest.raises(Exception) as a:
        assert channel.channel_addowner(1, 0, 1)  

# Test if the function functions normally with one owner and one member in the channel.   
def test_channel_addowner():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    channel.channel_join(0,0)
    new_owner = data['users'][0]
    data['channels'][0]['owners'].append(new_owner)
    auth.auth_register('newemail@gmail.com', '234abc!@#', 
    'Guanbin', 'Wen')
    auth.auth_login('newemail@gmail.com', '234abc!@#')
    channel.channel_join(0,0) 
    assert channel.channel_addowner(0, 0, 1) == None

# Test if the function raises an Input Error if the channel id is invalid.
def test_invalid_id_channel_removeowner():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    channel.channel_join(0,0)
    new_owner = data['users'][0]
    data['channels'][0]['owners'].append(new_owner)
    with pytest.raises(Exception) as e:
        assert channel.channel_removeowner(0, 6, 0)

# Test if the function raises an Input Error if the channel id is invalid.
def test_not_owner_channel_removeowner():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    channel.channel_join(0,0)
    with pytest.raises(Exception) as e:
        assert channel.channel_removeowner(0, 0, 0)

# Test if the function raises an Access Error if user is unauthorised to remove owner from this channel.      
def test_unauthorised_channel_removeowner():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    channel.channel_join(0,0)
    new_owner = data['users'][0]
    data['channels'][0]['owners'].append(new_owner)
    auth.auth_register('newemail@gmail.com', '234abc!@#', 
    'Guanbin', 'Wen')
    auth.auth_login('newemail@gmail.com', '234abc!@#')
    channel.channel_join(0,0) 
    with pytest.raises(Exception) as a:
        assert channel.channel_removeowner(1, 0, 0)  

# Test if the function functions normally with one owner and one member in the channel.   
def test_channel_removeowner():
    clear()
    auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    channels.channels_create(0, 'validchannelname', True)
    channel.channel_join(0,0)
    new_owner = data['users'][0]
    data['channels'][0]['owners'].append(new_owner)
    auth.auth_register('newemail@gmail.com', '234abc!@#', 
    'Guanbin', 'Wen')
    auth.auth_login('newemail@gmail.com', '234abc!@#')
    channel.channel_join(0,0) 
    channel.channel_addowner(0, 0, 1)
    assert channel.channel_removeowner(0, 0, 1) == None

