import logging
import src.scraper.constant as constant
from datetime import datetime


# Remove points, spaces and currency from a string and convert it to int
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


# Get the house id from the url
def transform_url_to_id(url: str):
    house_id = None
    url_split_list = url.split('/')
    if len(url_split_list) >= 2:
        try:
            house_id = int(url_split_list[len(url_split_list) - 2])
        except ValueError:
            logging.error('The url [' + url + '] cannot be converted to int')

    return house_id


# Add to the dictionary the values of the features
def transform_features_to_fields(data: dict, feature_list: list):
    data['habitaciones'] = None
    data['baños'] = None
    data['metros_cuadrados'] = None
    data['otros'] = None

    for feature in feature_list:
        if 'hab' in feature:
            data['habitaciones'] = feature
        elif 'baño' in feature:
            data['baños'] = feature
        elif 'm²' in feature:
            data['metros_cuadrados'] = feature
        else:
            data['otros'] = feature


# Convert a datetime to string
def transform_date_to_string(date: datetime):
    return date.strftime(constant.DATETIME_FORMAT)
