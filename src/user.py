from PIL import Image
from error import InputError
from error import AccessError
from database import *
from utility import *
from auth import *


def user_profile(token, u_id):
    check_valid_user(u_id)
    user = data_user(u_id)
    check_valid_token(token)
    return {
        'user': {
            'u_id': u_id,
            'email': user['email'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle'],
            'profile_img_url': user['profile_img_url']
        }
    }


def user_profile_setname(token, name_first, name_last):
    user = is_token_exist(token)
    check_name_length(name_first, name_last)
    user['name_first'] = name_first
    user['name_last'] = name_last
    return {
    }

def user_profile_setemail(token, email):
    email_check(email)
    if data_email_search(email) == None:    # if no one has the same email as this one
        user = is_token_exist(token)        # find the user with token
        user['email'] = email
        return {
        }
    raise InputError("The email has already been used by another user")


def user_profile_sethandle(token, handle_str):
    user = is_token_exist(token)        # find the user with token
    check_handle_length(handle_str)
    check_handle_exist(handle_str)
    user['handle'] = handle_str
    return {
    }


def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    user = is_token_exist(token)        # find the user with token
    u_id = user['u_id']
    check_img_is_jpg(img_url)
    # Fetching image via url
    fetch_img_check_valid_url(img_url, u_id)
    imageObject = Image.open(f'src/static/{u_id}.jpg')
    check_img_dimension(imageObject, x_start, y_start, x_end, y_end)
    # Crops the image and save in local
    cropped = imageObject.crop((x_start, y_start, x_end, y_end))
    cropped.save(f'src/static/{u_id}.jpg')
    user['profile_img_url'] = f'static/{u_id}.jpg'
    return {
    }
    
    