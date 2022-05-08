from datetime import datetime
from typing import List, Optional

import requests
import xmltodict
from pytz import utc

JWIKI_API = 'https://jwiki.kr/wiki/api.php'


def get_categories(title: str) -> List[str]:
    """ 제이위키 문서의 분류 이름들을 반환합니다. """

    r = requests.get(f'{JWIKI_API}?action=parse&page={title}&prop=categories&format=json')
    j = r.json()
    try:
        return list(map(lambda x: x['*'], j['parse']['categories']))
    except KeyError:
        return list()


def get_recent_changes(*, from_: Optional[datetime] = None):
    """
    ``from_``으로부터 지금까지 제이위키의 모든 문서 변경 사항을 반환합니다.
    ``from_``이 정의되어있지 않으면 제이위키 API에 기반한 기본 기간동안의 변경 사항을 반환합니다.

    :param from_: 변경 사항을 조회할 시작 시각
    :return: 변경 사항
    :type: Dict화 xml
    """

    url = f'{JWIKI_API}?action=feedrecentchanges'
    if from_ is not None:
        time = from_.astimezone(utc).strftime('%Y-%m-%d %H:%M:%S')
        url += f'&from={time}'
    r = requests.get(url)
    return xmltodict.parse(r.text)
