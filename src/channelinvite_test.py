# Tests of channel_invite, channel_join and channel_leave implemented
import auth
import channels
import channel
import pytest
import other
from database import data

# Test chanel_invite
#
#

def test_channel_invite_success():
    other.clear()
    # register the user who invites people
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')              # return u_id and token
    # let the user login 
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    # register and join the channel
    newchannel = channels.channels_create(userA['u_id'], 'validchannelname', True) # return channel_id
    channel.channel_join(userA['u_id'], newchannel['channel_id'])
    # register for the user being invited
    userB = auth.auth_register('validemail2@gmail.com', '123abc!@#', 'Guanbin', 'Wen')
    channel.channel_invite(userA['u_id'], newchannel['channel_id'], userB['u_id']) 
    assert len(data['channels'][0]['members']) == 2
       # clear user data


# InputError: u_id does not refer to a valid user
def test_channel_invite_invalid_user():
    other.clear()
    # register the user who invites people
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')              # return u_id and token
    # let the user login 
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    # register and join the channel
    newchannel = channels.channels_create(userA['u_id'], 'validchannelname', True) # return channel_id
    channel.channel_join(userA['u_id'], newchannel['channel_id'])
    with pytest.raises(Exception):
        channel.channel_invite(userA['u_id'], newchannel['channel_id'], 2) 
    
 

# AccessError: when the authorised user is not already a member of the channel
def test_channel_invite_unauthorised():
    other.clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    newchannel = channels.channels_create(userA['u_id'], 'validchannelname', True) # return channel_id
    # register for the user being invited
    userB = auth.auth_register('validemail2@gmail.com', '123abc!@#', 'Guanbin', 'Wen')
    with pytest.raises(Exception):
        channel.channel_invite(userA['u_id'], newchannel['channel_id'], userB['u_id']) 


'''
other.clear(channel_id)
def test_channel_invite_user_already_joined():
    user = auth.auth_register('email', '123abc!@#', 'Dennis', 'Lin')              # return u_id and token
    channel_id = channels.channels_create('token', 'validchannelname', True) # return channel_id

    assert channel.channel_invite(user.token, channel_id, user.u_id) == 'Invitation failed, user is already in the channel'
'''

# InputError: channel_id does not refer to a valid channel.
def test_channel_invite_invalid_channel():
    other.clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')              # return u_id and token
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    userB = auth.auth_register('validemail2@gmail.com', '123abc!@#', 'Guanbin', 'Wen')
    with pytest.raises(Exception):
        channel.channel_invite(userA['u_id'], 0, userB['u_id'])


# test channel_join
#
#

# join successful
def test_channel_join_successful():
    other.clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    newchannel = channels.channels_create(userA['u_id'], 'validchannelname', True) # return channel_id
    channel.channel_join(userA['u_id'], newchannel['channel_id']) 
    assert len(data['channels'][0]['members']) == 1


# InputError: Channel ID is not a valid channel
def test_channel_join_invalid_channel():
    other.clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin') 
    auth.auth_login('validemail@gmail.com', '123abc!@#') 
    with pytest.raises(Exception):
        channel.channel_join(userA['u_id'], 0)




'''
def test_channel_join_channel_already_joined():
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')                # return u_id and token
    channel_id = channels.channels_create('token', 'validchannelname', 'is_public') # return channel_id
    channel.channel_join(user.token, channel_id)
    assert channel.channel_join(user.token, channel_id) == 'join failed, you already joined this channel'
'''


# AccessError: when channel_id refers to a channel that is private (when the authorised user is not a global owner)
def test_channel_join_is_private():
    other.clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin') 
    auth.auth_login('validemail@gmail.com', '123abc!@#') 
    newchannel = channels.channels_create(userA['u_id'], 'validchannelname', False) # this channel is private
    with pytest.raises(Exception):
        channel.channel_join(userA['u_id'], newchannel['chanel_id'])


# test channel_leave
#
#


# leave successfully
def test_channel_leave():
    other.clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')
    auth.auth_login('validemail@gmail.com', '123abc!@#')
    newchannel = channels.channels_create(userA['u_id'], 'validchannelname', True) # return channel_id
    channel.channel_join(userA['u_id'], newchannel['channel_id'])
    for single in data['channels']:
        assert len(single['members']) == 1
    channel.channel_leave(userA['u_id'], newchannel['channel_id'])
    for single in data['channels']:
        assert len(single['members']) == 0

# AccessError: when Authorised user is not a member of channel with channel_id
def test_channel_leave_unauthorised():
    other.clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')  
    auth.auth_login('validemail@gmail.com', '123abc!@#')      
    newchannel = channels.channels_create(userA['u_id'], 'validchannelname', True) # return channel_id
    with pytest.raises(Exception):
        channel.channel_leave(userA['u_id'], newchannel['channel_id'])



# InputError: Channel ID is not a valid channel
def test_channel_leave_invalid_channel():
    other.clear()
    userA = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Dennis', 'Lin')  
    auth.auth_login('validemail@gmail.com', '123abc!@#')      
    newchannel = channels.channels_create(userA['u_id'], 'validchannelname', True) 
    channel.channel_join(userA['u_id'], newchannel['channel_id'])
    with pytest.raises(Exception):
        channel.channel_leave(userA['u_id'], 1) # channel_id = 1 does not exsist