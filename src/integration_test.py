from auth import *
from channel import *
from channels import *
from message import *
from user import *
from other import *
from database import data
import pytest

def test_integration():
    clear()

    # Valid information has been summitted to register from the first user
    info1 = auth_register("yilangwu@gmail.com", "516haha289dfdf", "Yilang", "Wu")
    assert (info1['u_id'] == 0 and info1['token'] == token_generate(0))

    # Vadid information has been summitted to register from the second user
    info2 = auth_register("moniquejohnson@outlook.com", "MMMoneyyy", "Monique", "Jonhson")
    assert (info2['u_id'] == 1 and info2['token'] == token_generate(1))

    # Vadid information has been summitted to register from the third user
    info3 = auth_register("ilovemaths@icloud.com", "Ihateenglish", "Maths", "English")
    assert (info3['u_id'] == 2 and info3['token'] == token_generate(2))

    # Invalid information has been summitted
    with pytest.raises(InputError):
        auth_register("andrew.hotmail.com", "Andrrrreeeeesfd", "Andrew", "Taylor")
    
    # User 0 create a channel
    info4 = channels_create(info1['token'], "The first channel", True)
    assert (info4['channel_id'] == 0)

    # User 0 invite user 1 to join the channel
    channel_invite(info1['token'], info4['channel_id'], info2['u_id'])

    # User 2 join the channel
    channel_join(info3['token'], info4['channel_id'])

    # User 0 add user 1 as owner
    channel_addowner(info1['token'], info4['channel_id'], info2['u_id'])

    # User 1 add user 2 as owner
    channel_addowner(info2['token'], info4['channel_id'], info3['u_id'])
    assert (len(data['channels'][0]['members']) == 3)

    # User 0 delete user 2's identity as an owner
    channel_removeowner(info2['token'], info4['channel_id'], info3['u_id'])

    # Show channel details of channel 0
    info5 = channel_details(info2['token'], info4['channel_id'])
    assert (info5['name'] == data['channels'][0]['name'] and info5['owner_members'] == 
    [
        {
            'u_id': 0,
            'name_first': 'Yilang',
            'name_last': 'Wu'
        },
        {
            'u_id': 1,
            'name_first': 'Monique',
            'name_last': 'Jonhson'
        }
    ])

    # User 2 leaves the channel 0
    channel_leave(info3['token'], info4['channel_id'])
    assert (len(data['channels'][0]['members']) == 2)

    # User 0 changes the names
    user_profile_setname(info1['token'], "Zixiang", "Lin")

    # User 0 changes the email
    user_profile_setemail(info1['token'], "zilxianglin@google.com")

    # The first user changes the handle
    user_profile_sethandle(info1['token'], "lizixiang")
    assert user_profile(info1['token'], info1['u_id']) == \
    {
        'user': {
            'u_id': 0,
            'email': 'zilxianglin@google.com',
            'name_first': 'Zixiang',
            'name_last': 'Lin',
            'handle_str': 'lizixiang'
        }
    }

    # User 0 obtain all users information
    assert users_all(info1['token']) == \
    {
        'users': [
            {
                'u_id': 0,
                'email': 'zilxianglin@google.com',
                'name_first': 'Zixiang',
                'name_last': 'Lin',
                'handle_str': 'lizixiang'
            }, 
            {
                'u_id': 1,
                'email': 'moniquejohnson@outlook.com',
                'name_first': 'Monique',
                'name_last': 'Jonhson',
                'handle_str': 'moniquejonhson'
            },
            {
                'u_id': 2,
                'email': 'ilovemaths@icloud.com',
                'name_first': 'Maths',
                'name_last': 'English',
                'handle_str': 'mathsenglish'
            }
        ]
    }

    # User 0 set user 1's permission_id to 1
    admin_userpermission_change(info1['token'], info2['u_id'], 1)
    assert data['users'][1]['permission_id'] == 1

    # User 0 send message to channel 0
    message_send(info1['token'], info4['channel_id'], "Hello?")

    # User 1 send message to channel 0
    message_send(info2['token'], info4['channel_id'], "My name is Monique")

    # User 0 obtain the messages the channel 0
    assert channel_messages(info1['token'], info4['channel_id'], 0) == \
    {
        'message_list': 
        [
            {
                'message_id': 0,
                'u_id': 0,
                'message': 'Hello?',
                'time_created': 0,
                'is_pinned': False,
            },
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'My name is Monique',
                'time_created': 0,
                'is_pinned': False,
            }
        ],
        'start': 0,
        'end': -1,
    }

    # User 0 search message that includes "Monique"
    assert search(info1['token'], "Monique") == \
    {
        'messages': 
        [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'My name is Monique',
                'time_created': 0,
            }
        ]
    }

    # User 0 remove the message 'My name is Monique'
    message_remove(info1['token'], 1)

    # User 0 edit the message 'Hello?' to 'Sorry'
    message_edit(info1['token'], 0, "Sorry")

    # User 0 obtain the message in the channel 0 again
    assert channel_messages(info1['token'], info4['channel_id'], 0) == \
    {
        'message_list':
        [
            {
                'message_id': 0,
                'u_id': 0,
                'message': 'Sorry',
                'time_created': 0,
                'is_pinned': False,
            }
        ],
        'start': 0,
        'end': -1,
    }


    # User 1 view the channel informations
    assert channels_list(info2['token']) == \
    {
        'channels': 
        [
            {
                'channel_id': 0,
                'name': 'The first channel',
            }
        ]
    }

    # User 1 create an new private channel
    info6 = channels_create(info2['token'], "The private Channel", False) 
    assert info6 == \
    {
        'channel_id': 1
    }

    # User 2 want to join this newly created channel, which is invalid
    with pytest.raises(AccessError):
        channel_join(info3['token'], 1)

    # User 0 obtain the infomation of all channels without being add in channel 1
    print(channels_listall(info1['token']))
    assert channels_listall(info1['token']) == \
    {
        'channels':
        [
            {
                'channel_id': 0,
                'name': 'The first channel'
            },
            {
                'channel_id': 1,
                'name': 'The private Channel'
            }
        ]
    }

    # User 2 log out
    assert auth_logout(info3['token']) == \
    {
        'is_success': True,
    }

    # User 2 login again
    info4 = auth_login("ilovemaths@icloud.com", "Ihateenglish")
    assert info4['u_id'] == 2 and info4['token'] == token_generate(info4['u_id'])

            
    
