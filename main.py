import requests


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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    image_url = get_image_url('https://xkcd.com/353/')
    download_image(image_url, 'comic.png')

