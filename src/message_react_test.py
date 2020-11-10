from auth import auth_register
from channels import channels_create
from channel import channel_join, channel_messages
from message import message_send, message_react, message_unreact
from other import clear
from error import InputError, AccessError
import pytest

def test_message_react_valid():
    '''Test if authorised users can react to messages and receive correct channel messages return'''
    clear()

    # Register user 0
    user0_info = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    # Register user 1
    user1_info = auth_register("billgates@outlook.com", "VukkFs", "Bill", "Gates")
    # Register user 2
    user2_info = auth_register("johnson@icloud.com", "RFVtgb45678", "M", "Johnson")
    # User 0 create a channel
    channel0_info = channels_create(user0_info['token'], "channel0", True)
    # User 1 join the channel
    channel_join(user1_info['token'], channel0_info['channel_id'])
    # User 1 create another channel
    channel1_info = channels_create(user1_info['token'], "channel1", True)
    # User 2 join channel1
    channel_join(user2_info['token'], channel1_info['channel_id'])
    # User 0 join channel1
    channel_join(user0_info['token'], channel1_info['channel_id'])
    # User 2 send a message
    message0_info = message_send(user2_info['token'], channel1_info['channel_id'], "Hello")
    # User 1 send a message
    message_send(user1_info['token'], channel1_info['channel_id'], "Hi")
    # User 1 reacts the message sent by user 2
    message_react(user1_info['token'], message0_info['message_id'], 1)
    # User 0 get all channel messages
    all_message_info = channel_messages(user0_info['token'], channel1_info['channel_id'], 0)
    assert all_message_info['message_list'][0]['reacts'] == [{
        'is_this_user_reacted': False, 
        'react_id': 1, 
        'u_ids': [1]
    }  ]
    # User 0 reacts the message sent by user 2
    message_react(user0_info['token'], message0_info['message_id'], 1)
    
    # User 0 get all channel messages
    all_message_info1 = channel_messages(user0_info['token'], channel1_info['channel_id'], 0)
    assert all_message_info1['message_list'][0]['reacts'] == [{
        'is_this_user_reacted': True, 
        'react_id': 1, 
        'u_ids': [1, 0]
    }  ]
    # User 2 get all channel messages
    all_message_info2 = channel_messages(user2_info['token'], channel1_info['channel_id'], 0)
    assert all_message_info2['message_list'][0]['reacts'] == [{
        'is_this_user_reacted': False, 
        'react_id': 1, 
        'u_ids': [1, 0]
    }  ]
   
def test_message_react_invalid_message_id():
    '''Test if function raises an input error when an invalid message_id is given'''
    clear()
    # Register user 0
    user0_info = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    # Register user 1
    user1_info = auth_register("billgates@outlook.com", "VukkFs", "Bill", "Gates")
    # User 0 create a channel
    channel0_info = channels_create(user0_info['token'], "channel0", True)
    # User 1 join the channel
    channel_join(user1_info['token'], channel0_info['channel_id'])
    # User 0 send a message
    message0_info = message_send(user0_info['token'], channel0_info['channel_id'], "Hello")
    # Invalid message_id
    with pytest.raises(InputError):
        assert message_react(user1_info['token'], message0_info['message_id'] + 1, 1)

def test_message_react_invalid_react_id():
    '''Test if function raises an input error when an invalid react_id is given'''
    clear()
    # Register user 0
    user0_info = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    # Register user 1
    user1_info = auth_register("billgates@outlook.com", "VukkFs", "Bill", "Gates")
    # User 0 create a channel
    channel0_info = channels_create(user0_info['token'], "channel0", True)
    # User 1 join the channel
    channel_join(user1_info['token'], channel0_info['channel_id'])
    # User 0 send a message
    message0_info = message_send(user0_info['token'], channel0_info['channel_id'], "Hello")
    # Invalid message_id
    with pytest.raises(InputError):
        assert message_react(user1_info['token'], message0_info['message_id'] , 2)

def test_message_react_already_reacted():
    '''Test if function raises an input error when the message is reacted again'''
    clear()
    # Register user 0
    user0_info = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    # Register user 1
    user1_info = auth_register("billgates@outlook.com", "VukkFs", "Bill", "Gates")
    # User 0 create a channel
    channel0_info = channels_create(user0_info['token'], "channel0", True)
    # User 1 join the channel
    channel_join(user1_info['token'], channel0_info['channel_id'])
    # User 0 send a message
    message0_info = message_send(user0_info['token'], channel0_info['channel_id'], "Hello")
    # User 1 reacts to the message
    message_react(user1_info['token'], message0_info['message_id'] , 1)
    # Message already reacted by user 1
    with pytest.raises(InputError):
        assert message_react(user1_info['token'], message0_info['message_id'] , 1)

def test_message_unreact_valid():
    '''Test if authorised users can unreact to messages and receive correct channel messages return'''
    clear()

    # Register user 0
    user0_info = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    # Register user 1
    user1_info = auth_register("billgates@outlook.com", "VukkFs", "Bill", "Gates")
    # Register user 2
    user2_info = auth_register("johnson@icloud.com", "RFVtgb45678", "M", "Johnson")
    # User 0 create a channel
    channel0_info = channels_create(user0_info['token'], "channel0", True)
    # User 1 join the channel
    channel_join(user1_info['token'], channel0_info['channel_id'])
    # User 1 create another channel
    channel1_info = channels_create(user1_info['token'], "channel1", True)
    # User 2 join channel1
    channel_join(user2_info['token'], channel1_info['channel_id'])
    # User 0 join channel1
    channel_join(user0_info['token'], channel1_info['channel_id'])
    # User 2 send a message
    message0_info = message_send(user2_info['token'], channel1_info['channel_id'], "Hello")
    # User 1 send a message
    message_send(user1_info['token'], channel1_info['channel_id'], "Hi")
    # User 1 reacts the message sent by user 2
    message_react(user1_info['token'], message0_info['message_id'], 1)
    # User 0 reacts the message sent by user 2
    message_react(user0_info['token'], message0_info['message_id'], 1)
    # User 2 reacts the message sent by user 2
    message_react(user2_info['token'], message0_info['message_id'], 1)
    # User 0 get all channel messages
    all_message_info0 = channel_messages(user0_info['token'], channel1_info['channel_id'], 0)
    assert all_message_info0['message_list'][0]['reacts'] == [{
        'is_this_user_reacted': True, 
        'react_id': 1, 
        'u_ids': [1, 0, 2]
    }  ]
    # User 0 unreact the message sent by user 2
    message_unreact(user0_info['token'], message0_info['message_id'], 1)
    # User 0 get all channel messages
    all_message_info1 = channel_messages(user0_info['token'], channel1_info['channel_id'], 0)
    assert all_message_info1['message_list'][0]['reacts'] == [{
        'is_this_user_reacted': False, 
        'react_id': 1, 
        'u_ids': [1, 2]
    }  ]
    # User 1 unreact the message sent by user 2
    message_unreact(user1_info['token'], message0_info['message_id'], 1)
    # User 2 unreact the message sent by user 2
    message_unreact(user2_info['token'], message0_info['message_id'], 1)
    # User 1 get all channel messages
    all_message_info2 = channel_messages(user1_info['token'], channel1_info['channel_id'], 0)
    assert all_message_info2['message_list'][0]['reacts'] == []

def test_message_unreact_invalid_message_id():
    '''Test if function raises an input error when an invalid message_id is given'''
    clear()
    # Register user 0
    user0_info = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    # Register user 1
    user1_info = auth_register("billgates@outlook.com", "VukkFs", "Bill", "Gates")
    # User 0 create a channel
    channel0_info = channels_create(user0_info['token'], "channel0", True)
    # User 1 join the channel
    channel_join(user1_info['token'], channel0_info['channel_id'])
    # User 0 send a message
    message0_info = message_send(user0_info['token'], channel0_info['channel_id'], "Hello")
    # Invalid message_id
    with pytest.raises(InputError):
        assert message_unreact(user1_info['token'], message0_info['message_id'] + 1, 1)

def test_message_unreact_invalid_react_id():
    '''Test if function raises an input error when an invalid react_id is given'''
    clear()
    # Register user 0
    user0_info = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    # Register user 1
    user1_info = auth_register("billgates@outlook.com", "VukkFs", "Bill", "Gates")
    # User 0 create a channel
    channel0_info = channels_create(user0_info['token'], "channel0", True)
    # User 1 join the channel
    channel_join(user1_info['token'], channel0_info['channel_id'])
    # User 0 send a message
    message0_info = message_send(user0_info['token'], channel0_info['channel_id'], "Hello")
    # Invalid react_id
    with pytest.raises(InputError):
        assert message_unreact(user1_info['token'], message0_info['message_id'], 2)

def test_message_unreact_no_active_react():  
    '''Test if function raises an input error when the message is not reacted'''
    clear()
    # Register user 0
    user0_info = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    # Register user 1
    user1_info = auth_register("billgates@outlook.com", "VukkFs", "Bill", "Gates")
    # User 0 create a channel
    channel0_info = channels_create(user0_info['token'], "channel0", True)
    # User 1 join the channel
    channel_join(user1_info['token'], channel0_info['channel_id'])
    # User 0 send a message
    message0_info = message_send(user0_info['token'], channel0_info['channel_id'], "Hello")
    # Message not reacted yet
    with pytest.raises(InputError):
        assert message_unreact(user1_info['token'], message0_info['message_id'] , 1) 
    # User 1 reacts to the message
    message_react(user1_info['token'], message0_info['message_id'] , 1)
    message_unreact(user1_info['token'], message0_info['message_id'] , 1)
    # Message already unreacted by user 1
    with pytest.raises(InputError):
        assert message_unreact(user1_info['token'], message0_info['message_id'] , 1)      
