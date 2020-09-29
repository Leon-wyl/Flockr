# Tests of channel_invite, channel_join and channel_leave implemented


def test_channel_invite_success():
    channel_id = channels.channels_create('token', 'validchannelname', 'is_public') # return channel_id
    user = auth.auth_register('email', '123abc!@#', 'Dennis', 'Lin')              # return u_id and token
    assert channel.channel_invite(user.token, channel_id, user.u_id) == "Invite successful"

other.clear(user)   # clear user data
other.clear(channel_id) # clear channel data
def test_channel_invite_user_not_exsist():
    channel_id = channels.channels_create('token', 'validchannelname', 'is_public') # return channel_id
    assert channel.channel_invite(user.token, channel_id, user.u_id) == "Invite failed, user does not exsist"

# def test_channel_invite_inviter_not_in_channel():

other.clear(channel_id)
def test_channel_invite_user_already_joint():
    user = auth.auth_register('email', '123abc!@#', 'Dennis', 'Lin')              # return u_id and token
    channel_id = channels.channels_create('token', 'validchannelname', 'is_public') # return channel_id

    assert channel.channel_invite(user.token, channel_id, user.u_id) == "Invitatio failed, user is already in the channel"

other.clear(user)
other.clear(channel_id)
def test_channel_invite_channel_not_created():
    user = auth.auth_register('email', '123abc!@#', 'Dennis', 'Lin')              # return u_id and token
    assert channel.channel_invite(user.token, channel_id, user.u_id) == "Invitation failed, channel has not been created"

other.clear(user)
def test_channel_join_successful():
    channel_id = channels.channels_create('token', 'validchannelname', 'is_public') # return channel_id
    user = auth.auth_register('email', '123abc!@#', 'Dennis', 'Lin')                # return u_id and token
    assert channel.channel_join(user.token, channel_id) == "join successful!"

other.clear(user)
other.clear(channel_id)
def test_channel_join_channel_not_created():
    user = auth.auth_register('email', '123abc!@#', 'Dennis', 'Lin')                # return u_id and token
    assert channel.channel_join(user.token, channel_id) == "join failed, channel does not exsist"

other.clear(user)
def test_channel_leave():
    channel_id = channels.channels_create('token', 'validchannelname', 'is_public') # return channel_id
    channel.channel_join(user.token, channel_id)
    user = auth.auth_register('email', '123abc!@#', 'Dennis', 'Lin')                # return u_id and token
    assert channel.channel_join(user.token, channel_id) == "leave successful"

other.clear(user)
other.clear(channel_id)
def test_channel_leave_not_joint():
    channel_id = channels.channels_create('token', 'validchannelname', 'is_public') # return channel_id
    user = auth.auth_register('email', '123abc!@#', 'Dennis', 'Lin')                # return u_id and token
    assert channel.channel_join(user.token, channel_id) == "leave failed, user have not joined the channel yet"

other.clear(user)
other.clear(channel_id)