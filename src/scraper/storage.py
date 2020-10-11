import csv

from src.scraper.constant import ENCODING_UTF8


def list_to_csv(data_list: list, filename: str):
    with open('../resources/' + filename + '.csv', 'a', encoding=ENCODING_UTF8, newline='\n') as f:
        wr = csv.DictWriter(f, delimiter=',', fieldnames=list(data_list[0].keys()))
        wr.writeheader()
        wr.writerows(data_list)
