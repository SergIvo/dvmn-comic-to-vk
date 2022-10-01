import os
from urllib.parse import urlparse, urlencode, urlunparse
import requests
from dotenv import load_dotenv


def download_image(url, path, params=None):
    response = requests.get(url, params=params)
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    print(make_url_for_token(client_id))
    token = os.getenv('ACCESS_TOKEN')
    groups = get_user_groups(token)
    group_id = groups['items'][0]
    server = get_wall_upload_server(token, group_id)
    upload_url = server['upload_url']

    uploaded_photo = upload_photo(upload_url, 'comic.png')
    print(uploaded_photo)
