
def test_channel_invite():
    channel_id = channels.channels_create('token', 'validchannelname', 'is_public') # return channel_id
    user = auth.auth_register('email', '123abc!@#', 'Dennis', 'Lin')                # return u_id and token
    assert channel.channel_invite(user.token, channel_id, user.u_id)                # ==

def test_channel_join():

    assert channel.channel_join(user.token, channel_id)

def test_channel_leave():

    assert channel.channel_join(user.token, channel_id)