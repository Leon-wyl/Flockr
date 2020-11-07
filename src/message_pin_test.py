from auth import auth_register
from channels import channels_create
from channel import channel_join, channel_messages
from message import message_send, message_pin
from other import clear
from error import InputError, AccessError
import pytest
from database import data

def test_message_pin_valid0():
    '''Owner of the channel pin the message sent by a member'''
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
    # USer 1 send a message
    message_send(user1_info['token'], channel1_info['channel_id'], "Hi")
    # User 1 pin the message sent by user 2
    message_pin(user1_info['token'], message0_info['message_id'])
    # User 0 get all channel messages
    all_message_info = channel_messages(user0_info['token'], channel1_info['channel_id'], 0)
    assert all_message_info['message_list'][0]['is_pinned'] == True

def test_message_pin_valid1():
    '''Owner of the flockr joins the channel and pin a message sent by a member'''
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
    # User 0 pin the message sent by user 2
    message_pin(user0_info['token'], message0_info['message_id'])
    # User 0 get all channel messages
    all_message_info = channel_messages(user0_info['token'], channel1_info['channel_id'], 0)
    assert all_message_info['message_list'][0]['is_pinned'] == True

def test_message_pin_invalid0():
    '''message_id is not a valid message'''
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
    message_send(user2_info['token'], channel1_info['channel_id'], "Hello")
    # User 1 send a message
    message_send(user1_info['token'], channel1_info['channel_id'], "Hi")
    with pytest.raises(InputError):
        # User 0 pin a message with wrong message_id
        message_pin(user0_info['token'], 2)

def test_message_pin_invalid1():
    '''Message with ID message_id is already pinned'''
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
    # USer 1 send a message
    message_send(user1_info['token'], channel0_info['channel_id'], "Hi")
    # User 1 pin the message sent by user 2
    message_pin(user1_info['token'], message0_info['message_id'])
    with pytest.raises(InputError):
        # User 1 pin that message again
        message_pin(user1_info['token'], message0_info['message_id'])

def test_message_pin_invalid2():
    '''The authorised user is not a member of the channel that the message is within'''
    clear()

    # Register user 0
    user0_info = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    # Register user 1
    user1_info = auth_register("billgates@outlook.com", "VukkFs", "Bill", "Gates")
    # Register user 2
    user2_info = auth_register("johnson@icloud.com", "RFVtgb45678", "M", "Johnson")
    # User 0 create channel0
    channel0_info = channels_create(user0_info['token'], "channel0", True)
    # User 1 join channel0
    channel_join(user1_info['token'], channel0_info['channel_id'])
    # User 1 create channel1
    channel1_info = channels_create(user1_info['token'], "channel1", True)
    # User 2 join channel1
    channel_join(user2_info['token'], channel1_info['channel_id'])
    # User 2 send a message
    message0_info = message_send(user2_info['token'], channel1_info['channel_id'], "Hello")
    # USer 1 send a message
    message_send(user1_info['token'], channel0_info['channel_id'], "Hi")
    with pytest.raises(AccessError):
        # User 0 pin a message in channel1 which he is not in
        message_pin(user0_info['token'], message0_info['message_id'])

def test_message_pin_invalid3():
    '''The authorised user is not an owner'''
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
    with pytest.raises(AccessError):
        # User 2 pin the message sent by himself
        message_pin(user2_info['token'], message0_info['message_id'])
