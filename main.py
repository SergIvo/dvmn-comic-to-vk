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


def save_photo_on_wall(token, user_id, group_id, photo, server, hash):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    data = {
        'access_token': token,
        'v': '5.194',
        'user_id': user_id,
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': hash
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()['response']


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

    uploaded_photo = {
        'server': 858304,
        'photo': '[{"markers_restarted":true,"photo":"ae166ae2ff:x","sizes":[],"latitude":0,"longitude":0,"kid":"98afe2b0ffff3b76d8907f1f81c00482","sizes2":[["s","a7d3f77708d80f6a41f407245a695dabb2cabf8fc71bd146080ec5ec","-753876056311895214",66,75],["m","3c29460dbf6e5bd878c664b965825c2c04981f9dc2389cac8f475494","2358693047503707460",115,130],["x","7dcc52e33e45ef9de2065dd120eeb29dda4b8738224de28f599ea240","-577043286504466372",518,588],["o","79c62f5271f6dba2dd20da641e7449e1ce4b7f022f1217f4e3bc24ba","-2142673292812803421",130,148],["p","876174c5973dcdfb1f107259621dada25f5de039e18b399da852e573","5606191029542540541",200,227],["q","14448a3918b458e6f4909c2ae982a1e6da50b367ed67a126ffa44118","-394116693926416371",320,363],["r","707a94d8bb3677736941fe262dbda44514d110f234973a6e1cffcbed","6557630725174129977",510,579]],"urls":[],"urls2":["p9P3dwjYD2pB9AckWmldq7LKv4_HG9FGCA7F7A/UmvbkrixifU.jpg","PClGDb9uW9h4xmS5ZYJcLASYH53COJysj0dUlA/RF2kbtTCuyA.jpg","fcxS4z5F753iBl3RIO6yndpLhzgiTeKPWZ6iQA/PJjgLzDu_fc.jpg","ecYvUnH226LdINpkHnRJ4c5LfwIvEhf047wkug/oyItGP6xQ-I.jpg","h2F0xZc9zfsfEHJZYh2tol9d4DnhizmdqFLlcw/_VTd2gkxzU0.jpg","FESKORi0WOb0kJwq6YKh5tpQs2ftZ6Em_6RBGA/DfB2evTQh_o.jpg","cHqU2Ls2d3NpQf4mLb2kRRTREPI0lzpuHP_L7Q/OfUwlmZiAVs.jpg"]}]',
        'hash': 'ece5a9b78c1a75a9be3e1fe91aadbb1a'
    }
    server, photo, hash = uploaded_photo['server'], uploaded_photo['photo'], uploaded_photo['hash']
    published = save_photo_on_wall(token, client_id, group_id, photo, server, hash)
    print(published)
