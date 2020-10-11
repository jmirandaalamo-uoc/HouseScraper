import logging

from bs4 import BeautifulSoup
from datetime import datetime
import src.scraper.raw_transformer as transformer
import src.scraper.constant as constant
import src.scraper.storage as storage


def transform_html_to_data(html, data_list, datetime_now: datetime):
    soup = BeautifulSoup(html, 'html.parser')

    house_items = soup.find('div', attrs={'class': 're-Searchresult'}).find_all(True, recursive=False)
    logging.info('House data items: ' + str(house_items))

    for house_item in house_items:
        if len(house_item['class']) == 1:
            data = {}

            raw_url = get_raw_url(house_item)
            raw_price = get_raw_price(house_item)
            raw_description = get_raw_description(house_item)
            raw_features = get_raw_features(house_item)
            raw_location = get_raw_location(house_item)
            raw_type = get_raw_type(house_item)
            raw_phone = get_raw_phone(house_item)

            data['id'] = transformer.transform_url_to_id(raw_url)
            data['scrap_date'] = transformer.transform_date_to_string(datetime_now)
            data['price'] = transformer.transform_price(raw_price)
            data['description'] = raw_description
            data['location'] = raw_location
            data['type'] = raw_type
            data['phone'] = raw_phone
            data['url'] = constant.BASE_URL + raw_url
            transformer.transform_features_to_fields(data, raw_features)

            if not is_id_added(data_list, data['id'], data['scrap_date']):
                data_list.append(data)

    storage.list_to_csv(data_list, 'data')


def get_raw_url(house_item):
    url_item = house_item.find('a', attrs={'class': 're-Card-link'})
    return url_item['href']


def get_raw_price(house_item):
    price_item = house_item.find('span', attrs={'class': 're-Card-price'})
    return price_item.get_text()


def get_raw_description(house_item):
    description_item = house_item.find('span', attrs={'class': 're-Card-description'})
    if description_item is not None:
        return description_item.get_text()
    return None


def get_raw_features(house_item):
    feature_items = house_item.find('div', attrs={'class': 're-CardFeatures-wrapper'})
    feature_span_items = feature_items.find_all('span', attrs={'class': 're-CardFeatures-feature'})
    raw_features = []
    for span_item in feature_span_items:
        raw_features.append(span_item.get_text())
    return raw_features


def get_raw_location(house_item):
    title_item = house_item.find('h3', attrs={'class': 're-Card-title'})
    raw_location = None
    if len(title_item.contents) > 1:
        raw_location = str(title_item.contents[1])
    return raw_location


def get_raw_type(house_item):
    title_item = house_item.find('h3', attrs={'class': 're-Card-title'})
    raw_type = None
    if len(title_item.contents) > 0:
        raw_type = title_item.contents[0].get_text()
    return raw_type


def get_raw_phone(house_item):
    contact_item = house_item.find('div', attrs={'class': 're-Card-contact'})
    contact_span_items = contact_item.find_all('span', attrs={'class': 'sui-AtomButton-text'})
    raw_phone = None
    if len(contact_span_items) > 1:
        raw_phone = contact_span_items[1].get_text()
    return raw_phone


def is_id_added(data_list: list, house_id: int, datetime_now: str):
    filtered = list(filter(lambda x: (x['id'] == house_id) and (x['scrap_date'] == datetime_now), data_list))
    return len(filtered) > 0
