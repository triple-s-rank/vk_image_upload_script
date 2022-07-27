import os
import random
from pathlib import Path

import requests
from dotenv import load_dotenv


def get_upload_data(access_token, api_version, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
            'access_token': access_token,
            'v': api_version,
            'group_id': group_id,
    }
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    decoded_response = response.json()['response']
    upload_url = decoded_response.get('upload_url')
    return upload_url


def upload_image(upload_url, comics_name):
    photo = f'images/{comics_name}.png'
    with open(photo, 'rb') as file:
        photo = {'photo': file}
        response = requests.post(url=upload_url, files=photo)
        response.raise_for_status()
    decoded_response = response.json()
    return decoded_response['server'], decoded_response['hash'], decoded_response['photo']


def save_on_wall(server, photo, photo_hash, access_token, api_version, group_id):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': photo_hash,
        'access_token': access_token,
        'v': api_version,
    }
    response = requests.post(url=url, data=params)
    response.raise_for_status()
    decoded_response = response.json()['response']
    return decoded_response[0]['id'], decoded_response[0]['owner_id']


def post_on_wall(owner_id, photo_id, message, access_token, api_version, group_id):
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'owner_id': access_token,
        'from_group': 0,
        'message': message,
        'attachments': f'photo{owner_id}_{photo_id}',
        'v': api_version,
        'access_token': group_id,
    }
    response = requests.get(url=url, params=params)
    response.raise_for_status()


def download_image(image_number):
    url = f'https://xkcd.com/{comics_number}/info.0.json'
    response = requests.get(url=url)
    response.raise_for_status()
    decoded_response = response.json()
    message = decoded_response['alt']
    title = decoded_response['safe_title']
    image_response = requests.get(url=decoded_response['img'])
    image_response.raise_for_status()
    with open(f'images/{title}.png', 'wb') as file:
        file.write(image_response.content)
    return message, title


def main():
    load_dotenv()
    access_token = os.environ.get('ACCESS_TOKEN')
    api_version = os.environ.get('API_VERSION')
    group_id = os.environ.get('GROUP_ID')
    Path(f'{Path.cwd()}/images').mkdir(parents=True, exist_ok=True)
    random_image_number = random.randint(1, 2648)
    message, comics_name = download_image(random_image_number)
    server, photo_hash, photo = upload_image(get_upload_data(access_token, api_version, group_id), comics_name)
    photo_id, owner_id = save_on_wall(server, photo, photo_hash, access_token, api_version, group_id)
    post_on_wall(owner_id, photo_id, message, access_token, api_version, group_id)
    os.remove(f'images/{comics_name}.png')


if __name__ == '__main__':
    main()

