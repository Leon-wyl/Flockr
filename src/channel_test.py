import auth
import channel
import pytest
from error import InputError
from error import AccessError
import channels
from database import data
from other import clear
import message

# Test if the function raises an Input Error if the channel id is invalid.
def test_invalid_id_channel_details():
    clear()
    info = auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    with pytest.raises(InputError):
        assert channel.channel_details(info['token'], channel_id)

# Test if the function raises an Access Error if user is unauthorised to view the channel details.      
def test_unauthorised_channel_details():
    clear()
    info = auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    secondinfo = auth.auth_register('newemail@gmail.com', '234abc!@#', 
    'Guanbin', 'Wen')
    with pytest.raises(AccessError):
        assert channel.channel_details(secondinfo['token'], channel_id['channel_id'])  
        
# Test if the function functions normally with two member in the channel.   
def test_channel_details():
    clear()
    info = auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    channels.channels_create(info['token'], 'validchannelname', True)
    second_channel_id = channels.channels_create(info['token'], 'secondchannelname', True)
    assert channel.channel_details(info['token'], second_channel_id['channel_id']) == {
        'name':'secondchannelname',
        'owner_members': [{'name_first': 'Hayden', 'name_last': 'Everest', 'u_id': 0}],
        'all_members': [{'name_first': 'Hayden', 'name_last': 'Everest', 'u_id': 0}],
    }

# Test if the function raises an Input Error if the channel id is invalid.    
def test_invalid_id_channel_messages():
    clear()
    info = auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    with pytest.raises(InputError):
        assert channel.channel_messages(info['token'], channel_id['channel_id'] + 1, 0)

# Test if the function raises an Input Error if the start of message is invalid.        
def test_invalid_start_channel_messages():
    clear()
    info = auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    with pytest.raises(InputError):
        assert channel.channel_messages(info['token'], channel_id['channel_id'], 5)

# Test if the function raises an Access Error if user is unauthorised to view the channel messages.          
def test_unauthorised_channel_messages():
    clear()
    info = auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    channel_id = channels.channels_create(info['token'], 'validchannelname', True)
    secondinfo = auth.auth_register('newemail@gmail.com', '234abc!@#', 
    'Guanbin', 'Wen')
    with pytest.raises(AccessError):
        assert channel.channel_messages(secondinfo['token'], channel_id['channel_id'], 0) 
        
# Test normal channel_messages
 
def test_channel_messages():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    channels.channels_create(info['token'], 'validchannelname', True)
    second_channel_id = channels.channels_create(info['token'], 'secondchannelname', True)
    message.message_send(info['token'], second_channel_id['channel_id'], 'hello')
    message.message_send(info['token'], second_channel_id['channel_id'], 'My name')
    message.message_send(info['token'], second_channel_id['channel_id'], '1s sam!')
    assert channel.channel_messages(info['token'], second_channel_id['channel_id'], 1) == {'end': -1, 'message_list': [{'message': 'My name', 'message_id': 1, 'time_created': 0, 'u_id': 0}, {'message': '1s sam!', 'message_id': 2, 'time_created': 0, 'u_id': 0}], 'start': 1}
    i = 0
    while i < 50:
        message.message_send(info['token'], second_channel_id['channel_id'], 'hello')
        i += 1
    assert channel.channel_messages(info['token'], second_channel_id['channel_id'], 1) == {'message_list': [{'message_id': 1, 'u_id': 0, 'message': 'My name', 'time_created': 0}, {'message_id': 2, 'u_id': 0, 'message': '1s sam!', 'time_created': 0}, {'message_id': 3, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 4, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 5, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 6, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 7, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 8, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 9, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 10, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 11, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 12, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 13, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 14, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 15, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 16, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 17, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 18, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 19, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 20, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 21, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 22, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 23, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 24, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 25, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 26, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 27, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 28, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 29, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 30, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 31, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 32, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 33, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 34, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 35, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 36, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 37, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 38, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 39, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 40, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 41, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 42, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 43, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 44, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 45, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 46, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 47, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 48, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 49, 'u_id': 0, 'message': 'hello', 'time_created': 0}, {'message_id': 50, 'u_id': 0, 'message': 'hello', 'time_created': 0}], 'start': 1, 'end': 51}
# Test if the function raises an Input Error if the channel id is invalid.
def test_invalid_id_channel_addowner():
    clear()
    user = auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    
    channels.channels_create(user['token'], 'validchannelname', True)
    with pytest.raises(InputError):
        assert channel.channel_addowner(user['token'], 6, 0)

# Test if the function raises an Input Error if the user is already an owner of the channel.

def test_already_owner_channel_addowner():
    clear()
    user = auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    channels.channels_create(user['token'], 'validchannelname', True)
    new_owner = data['users'][0]
    data['channels'][0]['owners'].append(new_owner)
    with pytest.raises(InputError):
        assert channel.channel_addowner(user['token'], 0, 0)

# Test if the function raises an Access Error if user is unauthorised to add owner to this channel.      
def test_unauthorised_channel_addowner():
    clear()
    user = auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    channels.channels_create(user['token'], 'validchannelname', True)
    new_owner = data['users'][0]
    data['channels'][0]['owners'].append(new_owner)
    user = auth.auth_register('newemail@gmail.com', '234abc!@#', 
    'Guanbin', 'Wen')
    channel.channel_join(user['token'],0) 
    with pytest.raises(AccessError):
        assert channel.channel_addowner(user['token'], 0, 1)  

# Test if the function functions normally with one owner and one member in the channel.   
def test_channel_addowner():
    clear()
    user1 = auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    channels.channels_create(user1['token'], 'validchannelname', True)
    assert len(data['channels'][0]['owners']) == 1
    user2 = auth.auth_register('newemail@gmail.com', '234abc!@#', 
    'Guanbin', 'Wen')
    channel.channel_join(user2['token'],0) 
    channel.channel_addowner(user1['token'], 0, 1)
    assert len(data['channels'][0]['owners']) == 2

# Test if the function raises an Input Error if the channel id is invalid.
def test_invalid_id_channel_removeowner():
    clear()
    user = auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    channels.channels_create(user['token'], 'validchannelname', True)
    with pytest.raises(InputError):
        assert channel.channel_removeowner(user['token'], 6, 0)

# if the user is not yet an owner of the channel
def test_not_owner_channel_removeowner():
    clear()
    user = auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    channels.channels_create(user['token'], 'validchannelname', True)

    user2 = auth.auth_register('validemail2@gmail.com', '123abc!@#', 
    'Hayden2', 'Everest2')
    channel.channel_join(user2['token'],0)
    with pytest.raises(AccessError):
        assert channel.channel_removeowner(user2['token'], 0, 0)

# Test if the function raises an Access Error if user is unauthorised to remove owner from this channel.      
def test_unauthorised_channel_removeowner():
    clear()
    user = auth.auth_register('validemail@gmail.com', '123abc!@#', 
    'Hayden', 'Everest')
    channels.channels_create(user['token'], 'validchannelname', True)
    user2 = auth.auth_register('newemail@gmail.com', '234abc!@#', 'Guanbin', 'Wen')
    channel.channel_join(user2['token'],0)
    with pytest.raises(AccessError):
        assert channel.channel_removeowner(user2['token'], 0, 0)

# Test if the function functions normally with one owner and one member in the channel.
def test_channel_removeowner():
    clear()
    info = auth.auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Bill", "Gates")
    channels.channels_create(info['token'], 'validchannelname', True)
    secondinfo = auth.auth_register("guanbin@gmail.com", "ttteh3hgi00d", "Billy", "Gale")
    second_channel_id = channels.channels_create(info['token'], 'secondchannelname', True) 
    channel.channel_join(secondinfo['token'], second_channel_id['channel_id'])
    second_u_id = auth.auth_u_id_from_token(secondinfo['token'])
    channel.channel_addowner(info['token'], second_channel_id['channel_id'], second_u_id)
    assert len(data['channels'][1]['owners']) == 2
    channel.channel_removeowner(info['token'], second_channel_id['channel_id'], second_u_id)
    assert len(data['channels'][1]['owners']) == 1

# Test chanel_invite
#
#

def test_channel_invite_success():
    clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin') 
    newchannel = channels.channels_create(userA['token'], 'validchannelname', True)
    userB = auth.auth_register('validemail2@gmail.com', '123abc!@#', 'Guanbin', 'Wen')
    channel.channel_invite(userA['token'], newchannel['channel_id'], userB['u_id'])
    assert len(data['channels'][0]['members']) == 2



# InputError: u_id does not refer to a valid user
def test_channel_invite_invalid_user():
    clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')
    channels.channels_create(userA['token'], 'validchannelname', True)
    with pytest.raises(InputError):
        channel.channel_invite(userA['token'], 0, 1) 
    
 

# AccessError: when the authorised user is not already a member of the channel
def test_channel_invite_unauthorised():
    clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')
    newchannel = channels.channels_create(userA['token'], 'validchannelname', True)
    userB = auth.auth_register('validemail2@gmail.com', '123abc!@#', 'Guanbin', 'Wen')
    userC = auth.auth_register('validemail3@gmail.com', '123abc!@#', 'Zixiang', 'Wen')
    with pytest.raises(AccessError):
        channel.channel_invite(userC['token'], newchannel['channel_id'], userB['u_id']) 



def test_channel_invite_user_already_joined():
    clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')
    userB = auth.auth_register('validemail2@gmail.com', '123abc!@#', 'Guanbin', 'Wen')       
    channels.channels_create(userA['token'], 'validchannelname', True)
    channel.channel_join(userB['token'], 0)
    with pytest.raises(InputError):
        channel.channel_invite(userB['token'], 0, 1)


# InputError: channel_id does not refer to a valid channel.
def test_channel_invite_invalid_channel():
    clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')              # return u_id and token
    userB = auth.auth_register('validemail2@gmail.com', '123abc!@#', 'Guanbin', 'Wen')
    with pytest.raises(InputError):
        channel.channel_invite(userA['token'], 0, userB['u_id'])


# test channel_join
#
#

# join successful
def test_channel_join_successful():
    clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')
    userB = auth.auth_register('validemail2@gmail.com', '123abc!@#', 'Guanbin', 'Wen')
    newchannel = channels.channels_create(userA['token'], 'validchannelname', True) # return channel_id
    channel.channel_join(userB['token'], newchannel['channel_id']) 
    assert len(data['channels'][0]['members']) == 2


# InputError: Channel ID is not a valid channel
def test_channel_join_invalid_channel():
    clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')
    with pytest.raises(InputError):
        channel.channel_join(userA['token'], 0)

        

def test_channel_join_channel_already_joined():
    clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')                # return u_id and token
    channels.channels_create(userA['token'], 'validchannelname', True) # return channel_id
    with pytest.raises(InputError):
        channel.channel_join(userA['token'], 0)

# AccessError: when channel_id refers to a channel that is private (when the authorised user is not a global owner)
def test_channel_join_is_private():
    clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')
    userB = auth.auth_register('validemail2@gmail.com', '123abc!@#', 'Guanbin', 'Wen')
    newchannel = channels.channels_create(userA['token'], 'validchannelname', False) # this channel is private
    with pytest.raises(AccessError):
        channel.channel_join(userB['token'], newchannel['channel_id'])


# test channel_leave
#
#


# leave successfully
def test_channel_leave():
    clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')
    channels.channels_create(userA['token'], 'validchannelname', True) # return channel_id
    assert len(data['channels'][0]['members']) == 1
    channel.channel_leave(userA['token'], 0)
    assert len(data['channels'][0]['members']) == 0

# AccessError: when Authorised user is not a member of channel with channel_id
def test_channel_leave_unauthorised():
    clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')
    userB = auth.auth_register('validemail2@gmail.com', '123abc!@#', 'Guanbin', 'Wen')
    newchannel = channels.channels_create(userA['token'], 'validchannelname', True) # return channel_id
    with pytest.raises(AccessError):
        channel.channel_leave(userB['token'], newchannel['channel_id'])

# InputError: Channel ID is not a valid channel
def test_channel_leave_invalid_channel():
    clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')        
    channels.channels_create(userA['token'], 'validchannelname', True) 
    with pytest.raises(InputError):
        channel.channel_leave(userA['token'], 1) # channel_id = 1 does not exist