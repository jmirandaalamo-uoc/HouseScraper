from bs4 import BeautifulSoup


def transform_html_to_data(html):
    soup = BeautifulSoup(html)
    print(soup.prettify())
