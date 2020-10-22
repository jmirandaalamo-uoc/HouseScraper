import src.scraper.provider_fotocasa as provider
import src.scraper.constant as constant
import sys
import src.scraper.soup_transformer as transformer
from datetime import datetime


def is_first_arg_help(arg):
    if arg == '-h' or arg == '--help':
        print('handler.py [city_name] [pages_number]')
        sys.exit(2)
    return False


if __name__ == "__main__":
    city = constant.DEFAULT_CITY
    pages = constant.DEFAULT_PAGES

    args = sys.argv

    # Check arguments
    if len(args) >= 2:
        arg1 = args[1]
        # Check if the first arg is for help or the city
        is_help = is_first_arg_help(arg1)
        if not is_help:
            city = arg1

        # The second arg is the number of pages
        if len(args) == 3:
            pages = int(args[2])

    print('- City: ' + city)
    print('- Pages: ' + str(pages))
    print()
    print('Launching...')
    provider.human_get(constant.BASE_URL, city, pages)


