import logging
import time

from selenium.webdriver.common.keys import Keys
import src.scraper.soup_transformer as transformer
from src.scraper.constant import *
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


# Use selenium to load a web
# IMPORTANT: The driver included is for Chrome version 86
# If you use another version you can download it from https://chromedriver.chromium.org/downloads
def human_get(url: str, city: str):
    url_list = []

    browser = init_browser()

    browser.get(url)
    time.sleep(SELENIUM_SLEEP_TIME)

    action_accept_cookies(browser)
    action_select_city(browser, city)
    action_change_sort(browser)
    action_close_modal(browser)
    html = action_get_pages(browser, url_list)

    print('url_list: {}'.format(url_list))
    transformer.transform_html_to_data(html)
    browser.quit()


def init_browser():
    # Use a random user agent and init selenium
    options = Options()
    user_agent = UserAgent()
    random_user_agent = user_agent.random

    options.add_argument(f'user-agent={user_agent}')
    browser = webdriver.Chrome(chrome_options=options, executable_path=r'../resources/selenium/chromedriver.exe')
    return browser


def action_accept_cookies(browser):
    cookies_button = browser.find_elements_by_xpath(build_path_for_cookies())[0]
    cookies_button.click()

    logging.info('Cookies accepted')
    time.sleep(SELENIUM_SLEEP_TIME)


def action_select_comprar(browser):
    alquilar_button = browser.find_elements_by_xpath(build_path_for_comprar)[0]
    alquilar_button.click()

    logging.info('Comprar selected')
    time.sleep(SELENIUM_SLEEP_TIME)


def action_select_city(browser, city: str):
    placeholder_area = browser.find_element_by_xpath(build_path_for_city_placeholder())
    placeholder_area.send_keys(city)

    logging.info('City selected')
    time.sleep(SELENIUM_SLEEP_TIME)

    buscar_button = browser.find_element_by_xpath(build_path_for_search_button())
    buscar_button.click()

    time.sleep(SELENIUM_SLEEP_TIME)


def action_change_sort(browser):
    select_option = browser.find_element_by_xpath(build_path_for_sort())
    select_option.click()

    time.sleep(SELENIUM_SLEEP_TIME)


def action_close_modal(browser):
    modal_news = browser.find_elements_by_xpath(build_path_for_modal())
    modal_news[len(modal_news) - 1].click()

    time.sleep(SELENIUM_SLEEP_TIME)


def action_get_pages(browser, url_list: list):
    elem = browser.find_element_by_tag_name('body')

    # Hago AvPág 20 veces
    no_of_pagedowns = 20

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)

        time.sleep(1)
        no_of_pagedowns -= 1

    pages_from_paginator = browser.find_elements_by_xpath(build_path_for_pages())
    for post in pages_from_paginator:
        url_list.append(post.get_attribute('href'))

    html = browser.page_source

    return html


def build_path_for_cookies():
    return f'/html/body/div[{POS_FIRST}]/footer/div[{POS_SECOND}]/div/div/div/div/div[{POS_SECOND}]' \
           f'/div/div[{POS_SECOND}]/button[{POS_SECOND}]'


def build_path_for_comprar():
    return f'/html/body/div[{POS_FIRST}]/div[{POS_SECOND}]/div[{POS_FIRST}]/div[{POS_FIRST}]/div[{POS_SECOND}]' \
           f'/div[{POS_FIRST}]/div[{POS_FIRST}]/label'


def build_path_for_city_placeholder():
    return '//input[@class="sui-AtomInput-input sui-AtomInput-input-m"]'


def build_path_for_search_button():
    return '//button[@type="submit"]'


def build_path_for_sort():
    return '//option[@value="publicationDate,true"]'


def build_path_for_modal():
    return '//span[@class="sui-AtomIcon sui-AtomIcon--medium sui-AtomIcon--currentColor"]'


def build_path_for_pages():
    return '//a[@class="sui-LinkBasic sui-PaginationBasic-link"]'
