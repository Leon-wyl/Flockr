'''from auth import *
from channel import *
from channels import *
from message import *
from user import *
from other import *
from database import data

def test_integration():
    clear();

    # Valid information has been summitted to register from the first user
    info1 = auth_register("yilangwu@gmail.com", "516haha289dfdf", "Yilang", "Wu")
    assert (info1['u_id'] == 0 and info['token'] == token_generate(0))

    # Vadid information has been summitted to register from the second user
    info2 = auth_register("moniquejohnson@outlook.com", "MMMoneyyy", "Monique", "Jonhson")
    assert (info2['u_id'] == 1 and info['token'] == token_generate(1))

    # Vadid information has been summitted to register from the third user
    info3 = auth_register("ilovemaths@icloud.com", "Ihateenglish", "Maths", "English")
    assert (info3['u_id'] == 2 and info['token'] == token_generate(2))

    # Invalid information has been summitted
    with pytest.raises(InputError):
        auth_register("andrew.hotmail.com", "Andrrrreeeeesfd", "Andrew", "Taylor")
    
    # User 0 create a channel
    info4 = channels_create(info1['token'], "The first channel", True)
    assert (info4['channel_id'] = 0)

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
    assert (info5['name'] == data['channels'][0]['name'] and info['owner_members'] == [
        {
            'u_id': info1['u_id'], 
            'name_first': "Yilang", 
            'name_last': "Wu",
        }, 
        {
            'u_id': info2['u_id'],
            'name_first': "Monique",
            'name_last': "Johnson",
        },
    ])

    # User 2 leaves the channel 0
    channel_leave(info3['token'], info4['channel_id'])
    assert (len(data['channels'][0]['members']) == 2)'''

