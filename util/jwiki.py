from datetime import datetime
from typing import List, Optional

import requests
import xmltodict
from pytz import utc

JWIKI_API = 'https://jwiki.kr/wiki/api.php'


def get_categories(title: str) -> List[str]:
    r = requests.get(f'{JWIKI_API}?action=parse&page={title}&prop=categories&format=json')
    j = r.json()
    return list(map(lambda x: x['*'], j['parse']['categories']))


def get_recent_changes(*, from_: Optional[datetime] = None):
    url = f'{JWIKI_API}?action=feedrecentchanges'
    if from_ is not None:
        time = from_.astimezone(utc).strftime('%Y-%m-%d %H:%M:%S')
        url += f'&from={time}'
    r = requests.get(url)
    return xmltodict.parse(r.text)
