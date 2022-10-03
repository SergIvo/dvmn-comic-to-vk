import os
from urllib.parse import urlparse, urlencode, urlunparse, urljoin
from random import randint
import requests
from dotenv import load_dotenv


def download_image(url, path):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def get_image_url(base_url):
    response = requests.get(f'{base_url}/info.0.json')
    response.raise_for_status()
    image_details = response.json()
    return image_details['img']


def get_image_comment(base_url):
    response = requests.get(f'{base_url}/info.0.json')
    response.raise_for_status()
    image_details = response.json()
    return image_details['alt']


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
    data = {
        'access_token': token,
        'v': '5.194',
        'user_id': user_id,
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': photo_hash
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()['response']


def post_on_wall(token, group_id, photo_owner_id, photo, message):
    url = 'https://api.vk.com/method/wall.post'
    data = {
        'access_token': token,
        'v': '5.194',
        'owner_id': - group_id,
        'from_group': 1,
        'message': message,
        'attachments': f'photo{photo_owner_id}_{photo}',
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()['response']


def get_random_comic_url(limit):
    url = 'https://xkcd.com'
    comic_number = randint(1, limit)
    return urljoin(url, str(comic_number))


def repost_random_comic(token, user_id):
    comic_url = get_random_comic_url(2679)
    image_url = get_image_url(comic_url)
    image_path = os.path.join(os.getcwd(), 'comic.png')
    download_image(image_url, image_path)
    comment = get_image_comment(comic_url)
    try:
        groups = get_user_groups(token)
        group_id = groups['items'][0]
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
    client_id = os.getenv('CLIENT_ID')
    token = os.getenv('ACCESS_TOKEN')
    if token:
        repost_random_comic(token, client_id)
        print('Комикс опубликован в группе.')
    else:
        print(f'Follow this link to get the authentication token \n{make_url_for_token(client_id)}')
