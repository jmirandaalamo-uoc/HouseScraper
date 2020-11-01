import logging
import time

from selenium.webdriver.common.keys import Keys
import src.scraper.soup_transformer as transformer
from src.scraper import storage
from src.scraper.constant import *
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from datetime import datetime


# Use selenium to load a web
# IMPORTANT: The driver included is for Chrome version 86
# If you use another version you can download it from https://chromedriver.chromium.org/downloads
def human_get(url: str, city: str, number_of_pages: int):
    # Init
    data_list = []
    datetime_now = datetime.now()

    browser = init_browser()

    # Go to the url
    browser.get(url)
    time.sleep(SELENIUM_SLEEP_TIME)

    # Do actions to navigate through the houses
    action_select_rent(browser)
    action_accept_cookies(browser)
    action_select_city(browser, city)
    action_change_sort(browser)
    action_close_modal(browser)

    # Get the html and transform the data
    html = action_get_page(browser)
    transformer.transform_html_to_data(html, data_list, datetime_now)

    # Go to next page and scroll and repeat the process
    i = 1
    while i < number_of_pages:
        action_next_page(browser)
        html = action_get_page(browser)
        transformer.transform_html_to_data(html, data_list, datetime_now)
        i += 1

    # Stop selenium
    browser.quit()

    # Save the data into a csv
    storage.list_to_csv(data_list, 'data')


def init_browser():
    # Use a random user agent and init selenium
    options = Options()
    user_agent = UserAgent()
    random_user_agent = user_agent.random

    options.add_argument(f'user-agent={user_agent}')
    browser = webdriver.Chrome(chrome_options=options, executable_path=r'../resources/selenium/chromedriver.exe')
    return browser


# Action to change to rent
def action_select_rent(browser):
    rent_input = browser.find_element_by_xpath(build_path_for_rent())
    rent_input.click()

    time.sleep(SELENIUM_SLEEP_TIME)


# Action to accept the cookies
def action_accept_cookies(browser):
    cookies_button = browser.find_elements_by_xpath(build_path_for_cookies())[0]
    cookies_button.click()

    logging.info('Cookies accepted')
    time.sleep(SELENIUM_SLEEP_TIME)


# Action to select the city
def action_select_city(browser, city: str):
    placeholder_area = browser.find_element_by_xpath(build_path_for_city_placeholder())
    placeholder_area.send_keys(city)

    logging.info('City selected')
    time.sleep(SELENIUM_SLEEP_TIME)

    buscar_button = browser.find_element_by_xpath(build_path_for_search_button())
    buscar_button.click()

    time.sleep(SELENIUM_SLEEP_TIME)


# Action to select the type of sorting
def action_change_sort(browser):
    select_option = browser.find_element_by_xpath(build_path_for_sort())
    select_option.click()

    time.sleep(SELENIUM_SLEEP_TIME)


# Action to close the modal that is opened
def action_close_modal(browser):
    modal_news = browser.find_elements_by_xpath(build_path_for_modal())
    modal_news[len(modal_news) - 1].click()

    time.sleep(SELENIUM_SLEEP_TIME)


# Action to scroll down and get the html code
def action_get_page(browser):
    elem = browser.find_element_by_tag_name('body')

    # Scroll to the end of the page
    no_of_pagedowns = 20

    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)

        time.sleep(1)
        no_of_pagedowns -= 1

    # Go to the paginator
    ActionChains(browser).move_to_element(browser.find_element_by_xpath(build_path_for_paginator())).perform()
    time.sleep(SELENIUM_SLEEP_TIME)

    html = browser.page_source

    return html


# Action to go to the next page
def action_next_page(browser):
    next_page_list = browser.find_elements_by_xpath(build_path_for_next_page())
    next_page = next_page_list[len(next_page_list)-1]
    next_page.click()

    time.sleep(SELENIUM_SLEEP_TIME)


# Get the xpath for the cookies button
def build_path_for_cookies():
    return '//button[@class="sui-AtomButton sui-AtomButton--primary "]'


# Get the xpath for the city input
def build_path_for_city_placeholder():
    return '//input[@class="sui-AtomInput-input sui-AtomInput-input-m"]'


# Get the xpath for the search button
def build_path_for_search_button():
    return '//button[@type="submit"]'


# Get the xpath for sorting
def build_path_for_sort():
    return '//option[@value="publicationDate,true"]'


# Get the xpath for closing the modal
def build_path_for_modal():
    return '//span[@class="sui-AtomIcon sui-AtomIcon--medium sui-AtomIcon--currentColor"]'


# Get the xpath for the next page
def build_path_for_next_page():
    return '//a[ancestor::li[@class="sui-PaginationBasic-item sui-PaginationBasic-item--control"]]'


# Get the xpath for the paginator
def build_path_for_paginator():
    return '//div[@class="re-Pagination"]'


def build_path_for_rent():
    return '//label[ancestor::div[@class="re-Search-selectorContainer re-Search-selectorContainer--rent"]]'
