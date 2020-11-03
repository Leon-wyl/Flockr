from auth import auth_register
from channels import channels_create
from channel import channel_join, channel_messages
from message import message_send, message_pin
from other import clear

def test_message_pin_valid0(){
    clear()

    # Register the user 0
    user0_info = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    # Register the user 1
    user1_info = auth_register("billgates@outlook.com", "VukkFs", "Bill", "Gates")
    # User 0 create a channel
    channel0_info = channels_create(user0_info['token'], "channel0", True)
    # User 1 join the channel
    channel_join(user1_info['token'], channel0_info['channel_id'])
    # User 1 send message
    message0_info = message_send(user1_info['token'], channel0_info['channel_id'], "Hi")
    # User 0 send message
    message_send(user0_info['token'], channel0_info['channel_id'], "Hello")
    # User 1 pin the message sent by himself
    message_pin(user1_info['token'], message0_info['message_id'])
    # User 0 get all channel messages
    all_message_info = channel_messages(user0_info['token'], channel0_info['channel_id'], 0)
    assert all_message_info['message_list'][0]['pin'] == True
}

def test_message_pin_valid1(){
    clear()

    # Register the user 0
    user0_info = auth_register("leonwu@gmail.com", "ihfeh3hgi00d", "Yilang", "W")
    # Register the user 1
    user1_info = auth_register("billgates@outlook.com", "VukkFs", "Bill", "Gates")
    # User 0 create a channel
    channel0_info = channels_create(user0_info['token'], "channel0", True)
    # User 1 join the channel
    channel_join(user1_info['token'], channel0_info['channel_id'])
    # User 1 send message
    message0_info = message_send(user1_info['token'], channel0_info['channel_id'], "Hi")
    # User 0 send message
    message_send(user0_info['token'], channel0_info['channel_id'], "Hello")
    # User 0 pin the message sent by user1
    message_pin(user0_info['token'], message0_info['message_id'])
    # User 0 get all channel messages
    all_message_info = channel_messages(user0_info['token'], channel0_info['channel_id'], 0)
    assert all_message_info['message_list'][0]['pin'] == True
}