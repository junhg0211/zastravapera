import requests

from const import get_secret

URL = 'https://openapi.naver.com/v1/papago/n2mt'

CLIENT_ID = get_secret('naver_client_id')
CLIENT_SECRET = get_secret('naver_client_secret')


def translate(text: str, source: str, target: str):
    data = {'source': source, 'target': target, 'text': text}
    headers = {'X-Naver-Client-Id': CLIENT_ID, 'X-Naver-Client-Secret': CLIENT_SECRET}

    r = requests.post(URL, data=data, headers=headers)
    j = r.json()

    return j['message']['result']['translatedText']
