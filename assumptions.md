Project Assumption for iteration 1

auth.py
1. An empty dictionary contains two list items, ‘users’ and ‘channels’. This dictionary is stored in database.py to store information of users and channels
2. User ID (u_ids) start from 0.
3. Token is currently equivalent to the string form of u_id
4. In the function auth_register, the inputs of the function (email, password, name_first and name_last) are of type string
5. Users have to remember their login credentials (email, password) in order to login as there are no functions to reset their password as of iteration 1.

channels.py
1. Channel ID (channel_id) starts from 0
2. Channel ID is unique among all channels
3. Members and owners are stored in two lists
4. User ID (u_ids) are used as tokens.
5. Channels_list function and channels_listall function only return lists of dictionaries containing channel ids and channel names
6. The members and owners lists are empty when channels are created

channel.py
1. An authorised user cannot rejoin the same channel if they are currently in the channel
2. A user has to register (if not yet registered) and login before the user can join,  create or leave any channel. 
3. The user does not have to login to be invited into a channel
4. User can have 0 or more channels 
5. You have to be added into the channel before you can become an owner of the channel
6. If you are removed as an owner of the channel, you can still exist as a member in the channel

channel_message
1. For the channel_message function, as the ability to send messages in the channel(through the usage of message.message_send function) is not yet implemented, it is assumed that when the channel_message is called, the function works as intended.


