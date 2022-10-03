import os
from random import randint
from urllib.parse import urlparse, urlencode, urlunparse, urljoin

import requests
from dotenv import load_dotenv


def download_image(url, path):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def get_image_details(base_url):
    response = requests.get(f'{base_url}/info.0.json')
    response.raise_for_status()
    image_details = response.json()
    url = image_details['img']
    comment = image_details['alt']
    path = os.path.join(os.getcwd(), 'comic.png')
    return url, comment, path


def make_url_for_token(client_id):
    url = 'https://oauth.vk.com/authorize'
    params = {
        'client_id': client_id,
        'scope': 'photos,groups,wall,offline',
        'response_type': 'token'
    }
    url_parts = urlparse(url)
    url_parts = url_parts._replace(query=urlencode(params))
    return urlunparse(url_parts)


def get_user_groups(token):
    url = 'https://api.vk.com/method/groups.get'
    params = {'access_token': token, 'v': '5.194'}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['response']


def get_wall_upload_server(token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {'access_token': token, 'v': '5.194', 'group_id': group_id}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['response']


def upload_photo(url, path_to_photo):
    with open(path_to_photo, 'rb') as photo:
        files = {'photo': photo}
        response = requests.post(url, files=files)
    response.raise_for_status()
    return response.json()


def save_photo_to_vk(token, user_id, group_id, photo, server, photo_hash):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': token,
        'v': '5.194',
        'user_id': user_id,
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': photo_hash
    }
    response = requests.post(url, data=params)
    response.raise_for_status()
    return response.json()['response']


def post_on_wall(token, group_id, photo_owner_id, photo, message):
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': token,
        'v': '5.194',
        'owner_id': - group_id,
        'from_group': 1,
        'message': message,
        'attachments': f'photo{photo_owner_id}_{photo}',
    }
    response = requests.post(url, data=params)
    response.raise_for_status()
    return response.json()['response']


def get_random_comic_url():
    base_url = 'https://xkcd.com'
    api_url = 'https://xkcd.com/info.0.json'
    response = requests.get(api_url)
    response.raise_for_status()
    last_comic_number = response.json()['num']
    random_comic_number = randint(1, last_comic_number)
    return urljoin(base_url, str(random_comic_number))


def repost_random_comic(token, group_id, user_id):
    comic_url = get_random_comic_url()
    image_url, comment, image_path = get_image_details(comic_url)
    download_image(image_url, image_path)
    try:
        server = get_wall_upload_server(token, group_id)
        upload_url = server['upload_url']

        uploaded_photo = upload_photo(upload_url, image_path)
        photo, server, photo_hash = uploaded_photo['photo'], uploaded_photo['server'], uploaded_photo['hash']

        saved_photo = save_photo_to_vk(token, user_id, group_id, photo, server, photo_hash)
        photo_id = saved_photo[0]['id']
        photo_owner_id = saved_photo[0]['owner_id']
        post_on_wall(token, group_id, photo_owner_id, photo_id, comment)
    finally:
        os.remove(image_path)


if __name__ == '__main__':
    load_dotenv()
    client_id = os.getenv('VK_APP_ID')
    token = os.getenv('VK_IMPLICIT_FLOW_TOKEN')
    group_id = int(os.getenv('VK_GROUP_ID'))
    if token:
        repost_random_comic(token, group_id, client_id)
        print('Комикс опубликован в группе.')
    else:
        print(f'Follow this link to get the authentication token \n{make_url_for_token(client_id)}')
