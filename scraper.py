from datetime import date, timedelta
import requests
import json
from random import random

def get_page(xtype:str, country:str, category:str, day:str):
    '''
    Function to get a page from sensortower given a specific format.
    xtype: str. Type of mobile ios or android
    contry: str. Country code of 2 letters. 
    categories: str. Category of the apps list: all, game, education, etc !! las categorías varían de acuedo al tipo de movil que sean. is an int if its iphone
    date: date of the query in format: yy-mm-dd.
    '''
    if xtype == 'android':
        phone = 'MOBILE'
    elif xtype == 'ios':
        phone = 'IPHONE'
    else:
        raise Exception('Invalid Arguments')
    url = f'https://sensortower.com/api/{xtype}/rankings/get_category_rankings?category={category}&country={country}&date={day}T00%3A00%3A00.000Z&device={phone}&limit=100&offset=0'
    print(f'Downloading {url}')
    try: 
        info = requests.get(url).text
        info = json.loads(info)
        return parse_response(info) 
    except Exception as e:
        with open('db/error.txt', 'a') as fd:
            fd.write(f'ERROR: {url}\n')
        print(f'ERROR: {url}')
        print(e)
        return {}
    
def parse_response(info):
    app_info = {'Free': [], 'Paid': []}
    columns = ['Free', 'Paid']
    for pos, row in enumerate(info):
        for i, column in enumerate(row[:-1]):
            if i >= 2: break
            app_info[columns[i]].append({
                'name': try_get_field(column, 'name'),
                'publisher': try_get_field(column, 'publisher_name'),
                'downloads': try_get_field(column, 'rating_count'),
                'price': try_get_field(column, 'price'),
                # 'original_country': column['canonical_country'],
                'release_date': try_get_field(column, 'release_date'),
                'content_rating': try_get_field(column, 'content_rating'),
                'position': pos 
            }) 
    return app_info

def try_get_field(column, field):
    try:
        return column[field]
    except:
        return 'UNKNOWN'

def get_dates():
    'Gets the last 90 days'
    days = []
    current_day = date.today()
    last_day = current_day - timedelta(90)
    while current_day > last_day:
        days.append(str(current_day))
        current_day -= timedelta(1)
    return days

def get_all_pages():
    dates = get_dates()
    countries = json.load(open('db/countries.json'))
    # obtiene la informacion de iphone
    # categories_ios = json.load(open('db/compress_ios_categories.json')) 
    # get_pages(countries, dates, categories_ios, 'ios')
    # obtiene la informacion de android
    android_categories = json.load(open('db/compress_android_categories.json'))
    get_pages(countries, dates, android_categories, 'android')

    
def get_pages(countries, dates, categories, xtype):
    for country in countries:
        current_country = {}
        for c_name, c_code in categories.items():
            current_country[c_name] = {}
            for d in dates:
                current_country[c_name][d] = get_page(xtype, country, c_code, d)
        json.dump(current_country, open(f'db/{xtype}/{country}.json', 'w+'))


if __name__ == "__main__":
    open('db/error.txt', 'w').close()       # truncates file
    get_all_pages()