import requests
import json
import re
from scraper import get_page

def process_file():
    err_file = open('db/error.txt')
                        #  ERROR: https://sensortower.com/api/android/rankings/get_category_rankings?category=all&country=BR&date=2020-11-13T00%3A00%3A00.000Z&device=MOBILE&limit=100&offset=0\n''
    pattern = re.compile(r'ERROR: https://sensortower\.com/api/(?P<type>(android|ios))/rankings/get_category_rankings\?category=(?P<category>.+)&country=(?P<country>\w{2})&date=(?P<day>(\d{4}-\d{2}-\d{2}))T00%3A00%3A00\.000Z&device=(?P<phone>(MOBILE|IPHONE))&limit=100&offset=0\n')
    for err in err_file.readlines():
        m = pattern.search(err)
        process_page(**m.groupdict())

def process_page(type, category, country, day, phone):
    page_info = get_page(type, category, country, day)
    with open(f'db/{type}/{country}.json', 'w+') as file_json:
        info = json.load(file_json)
        c_name = get_category_code(category, type)
        info[c_name][day] = page_info
        json.dump(info, file_json)

def get_category_code(category_code, type):
    if type == 'android':
        categories = json.load(open('db/compress_android_categories.json'))
    elif type == 'ios':
        categories = json.load(open('db/compress_ios_categories.json'))
    for k, v in categories.items():
        if v == category_code:
            return k 

if __name__ == "__main__":
    process_file()