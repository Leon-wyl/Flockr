Project Assumption
auth.py
An empty dictionary which has two list items, ‘users’ and ‘channels’, has been created to store information of users and channels.
u_ids start from 0.
tokens are the strings form of u_ids


channels.py
Assume channel_id start from 0. 
Assume members and owners are stored in two lists.
u_ids are used as tokens.
channels_list function and lchannels_listall function only return lists of dictionaries containing channel ids and channel names.

channel.py
Assuming if users are already in a channel, they cannot rejoin the same channel, otherwise the same member details would appear one time more each time the user joins
An user has to register (if not yet registered) & login before he/she can join or create or leave any channel
User 
