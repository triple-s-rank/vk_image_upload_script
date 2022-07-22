import os

import requests
from dotenv import load_dotenv


def get_upload_data():
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {'access_token': os.environ.get('ACCESS_TOKEN'), 'v': 5.131, 'group_id': 214645742}
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    decoded_response = response.json()['response']
    upload_url = decoded_response.get('upload_url')
    return upload_url


def upload_photo(upload_url, photo):
    with open(photo, 'rb') as file:
        photo = {
            'photo': file,
        }
        response = requests.post(url=upload_url, files=photo)
    decoded_response = response.json()
    return decoded_response['server'], decoded_response['hash'], decoded_response['photo']
    # return server, hash, photo


def save_to_wall(server, photo, p_hash):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'group_id': 214645742,
        'photo': photo,
        'server': server,
        'hash': p_hash,
        'access_token': os.environ.get('ACCESS_TOKEN'),
        'v': 5.131,
    }
    response = requests.post(url=url, data=params)
    print(response.json())


def main():
    load_dotenv()
    photo = 'images/chemicals.png'
    server, p_hash, photo = upload_photo(get_upload_data(), photo)
    save_to_wall(server, photo, p_hash)


if __name__=='__main__':
    main()