import auth
import error
import channels

def channel_invite(token, channel_id, u_id):
    return {
    }

def channel_details(token, channel_id):
    #Given a Channel with ID channel_id that the authorised user is part of, provide basic details about the channel({ name, owner_members, all_members } token is string, channel_id is integer
    
    for channels in channels.channels_list(token):
        if channel_id == channels.channel_id: 
            for u_id in channels.all_members:
                if token == all_members.u_id:
                    channel_name = channels.name
                    owners = channels.owner_members 
                    members = channels.all_members
                    return channel_name, owners, members
                else :
                    raise AccessError("You are unauthorised to obtain the details of this channel")
                    
        else :
            raise InputError("You have entered an invalid channel ID")
            
            
        
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages(token, channel_id, start):
    #Given a Channel with ID channel_id that the authorised user is part of, return up to 50 messages between index "start" and "start + 50". Message with index 0 is the most recent message in the channel. This function returns a new index "end" which is the value of "start + 50", or, if this function has returned the least recent messages in the channel, returns -1 in "end" to indicate there are no more messages to load after this return.
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave(token, channel_id):
    return {
    }

def channel_join(token, channel_id):
    return {
    }

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    return {
    }
