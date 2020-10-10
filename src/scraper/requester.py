import logging
import urllib.parse

import requests
from fake_useragent import UserAgent

import src.scraper.constant as constant


def get(url: str):
    user_agent = UserAgent().random
    headers = {'User-Agent': user_agent}
    url = urllib.parse.unquote(url)
    request = requests.get(url, headers=headers, timeout=constant.REQUEST_TIMEOUT)

    if request.status_code != requests.codes.ok:
        logging.error('Bad response code: ' + str(request.status_code))
        request.raise_for_status()

    request.encoding = constant.ENCODING_UTF8
    return request.text
