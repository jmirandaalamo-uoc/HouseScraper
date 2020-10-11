# Remove points, spaces, currency and convert to int
import logging
import src.scraper.constant as constant
from datetime import datetime


def transform_price(raw_price: str):
    price = None

    if raw_price is not None:
        try:
            price = raw_price \
                .replace('.', '') \
                .replace(' ', '') \
                .replace('€', '')

            price = int(price)
        except ValueError:
            price = None
            logging.error('The price [' + raw_price + '] cannot be converted to int')

    return price


def transform_url_to_id(url: str):
    house_id = None
    url_split_list = url.split('/')
    if len(url_split_list) >= 2:
        try:
            house_id = int(url_split_list[len(url_split_list) - 2])
        except ValueError:
            logging.error('The url [' + url + '] cannot be converted to int')

    return house_id


def transform_features_to_fields(data: dict, feature_list: list):
    feature_list_len = len(feature_list)
    if feature_list_len > 0:
        data['habitaciones'] = feature_list[0]
    if feature_list_len > 1:
        data['baños'] = feature_list[1]
    if feature_list_len > 2:
        data['metros_cuadrados'] = feature_list[2]
    if feature_list_len > 3:
        data['otros'] = feature_list[3]


def transform_date_to_string(date: datetime):
    return date.strftime(constant.DATETIME_FORMAT)
