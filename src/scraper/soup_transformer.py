import logging

from bs4 import BeautifulSoup, NavigableString


def transform_html_to_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    house_items = soup.find('div', attrs={'class': 're-Searchresult'}).find_all(True, recursive=False)
    logging.info('House data items: ' + str(house_items))

    raw_data_list = []

    for house_item in house_items:
        if len(house_item['class']) == 1:
            data = {}

            url_item = house_item.find('a', attrs={'class': 're-Card-link'})
            raw_url = url_item['href']

            price_item = house_item.find('span', attrs={'class': 're-Card-price'})
            raw_price = price_item.get_text()

            description_item = house_item.find('span', attrs={'class': 're-Card-description'})
            raw_description = description_item.get_text()

            feature_items = house_item.find('div', attrs={'class': 're-CardFeatures-wrapper'})
            feature_span_items = feature_items.find_all('span', attrs={'class': 're-CardFeatures-feature'})
            raw_features = []
            for span_item in feature_span_items:
                raw_features.append(span_item.get_text())

            title_item = house_item.find('h3', attrs={'class': 're-Card-title'})
            raw_location = None
            raw_type = None
            if len(title_item.contents) > 1:
                raw_location = str(title_item.contents[1])
                raw_type = title_item.contents[0].get_text()

            contact_item = house_item.find('div', attrs={'class': 're-Card-contact'})
            contact_span_items = contact_item.find_all('span', attrs={'class': 'sui-AtomButton-text'})
            raw_phone = None
            if len(contact_span_items) > 1:
                raw_phone = contact_span_items[1].get_text()

            data['raw_url'] = raw_url
            data['raw_price'] = raw_price
            data['raw_description'] = raw_description
            data['raw_features'] = raw_features
            data['raw_location'] = raw_location
            data['raw_type'] = raw_type
            data['raw_phone'] = raw_phone
            raw_data_list.append(data)
