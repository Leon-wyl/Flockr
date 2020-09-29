import channel
import pytest
import error
import channels

def test_echo():
    assert echo.echo("1") == "1", "1 == 1"
    assert echo.echo("abc") == "abc", "abc == abc"
    assert echo.echo("trump") == "trump", "trump == trump"

def test_echo_except():
    with pytest.raises(InputError) as e:
        assert echo.echo("echo")

def test_invalid_channel():
    result = channels.channels_create('token', 
             'validchannelname', 'is_public')
    with pytest.raises(InputError) as e:
        channel.channel_details('token', 'channel_id')
        
def test_unauthorised_channel():
    result = channels.channels_create('anothertoken', 
             'validchannelname', 'is_private')
    with pytest.raises(AccessError) as a:
        channel.channel_details('token', 'channel_id')  
      
def test_channel_details():
    result = channels.channels_create('token', 
             'validchannelname', 'is_public')
    assert channel.channel_details("token", "channel_id") == "validchannelname", "{ name, owner_members, all_members }"
    assert echo.echo("abc") == "abc", "abc == abc"
    assert echo.echo("trump") == "trump", "trump == trump"        

