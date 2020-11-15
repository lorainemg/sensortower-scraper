import requests
import json
import re, os
from scraper import get_page

def process_file(error_filename: str):
    err_file = open(error_filename)
                        #  ERROR: https://sensortower.com/api/android/rankings/get_category_rankings?category=all&country=BR&date=2020-11-13T00%3A00%3A00.000Z&device=MOBILE&limit=100&offset=0\n''
    pattern = re.compile(r'https://sensortower\.com/api/(?P<type>(android|ios))/rankings/get_category_rankings\?category=(?P<category>.+)&country=(?P<country>\w{2})&date=(?P<day>(\d{4}-\d{2}-\d{2}))T00%3A00%3A00\.000Z&device=(?P<phone>(MOBILE|IPHONE))&limit=100&offset=0')
    lines = err_file.readlines()
    open(error_filename, 'w').close()
    for err in lines:
        m = pattern.search(err)
        process_page(**m.groupdict())    
    return True if len(err_file.readlines()) == 0 else False

def process_page(type, category, country, day, phone):
    page_info = get_page(type, country, category, day)
    c_name = get_category_code(category, type)
    filename = f'db/{type}/{country}.json'
    create_file(filename)
    with open(filename, 'r+') as file_json:
        try:
            info = json.load(file_json)
            print('-------------------------------' + str(info) + '-------------------------------')
            if c_name not in info:
                info[c_name] = {}
        except json.JSONDecodeError:
            info = {c_name: {}}
        info[c_name][day] = page_info
    with open(f'db/{type}/{country}.json', 'w+') as file_json:
        json.dump(info, file_json)

def create_file(filename:str):
    if not os.path.exists(filename):
        open(filename, 'w').close()

def get_category_code(category_code, type):
    if type == 'android':
        categories = json.load(open('db/compress_android_categories.json'))
    elif type == 'ios':
        categories = json.load(open('db/compress_ios_categories.json'))
    for k, v in categories.items():
        if v == category_code:
            return k 

if __name__ == "__main__":
    n = 3
    while n > 0 and not process_file('db/error.txt'): 
        n -= 1