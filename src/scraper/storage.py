import csv
import os

from src.scraper.constant import ENCODING_UTF8


# Save a json list into a csv
def list_to_csv(data_list: list, filename: str):
    csv_exist = os.path.exists('../resources/' + filename + '.csv')
    with open('../resources/' + filename + '.csv', 'a', encoding=ENCODING_UTF8, newline='\n') as f:
        wr = csv.DictWriter(f, delimiter=',', fieldnames=list(data_list[0].keys()))
        if not csv_exist:
            wr.writeheader()
        wr.writerows(data_list)
