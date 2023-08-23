from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from tqdm import tqdm

USER_AGENT = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}



def data_manipulation():
    first_url, soup = get_url()  #1 = page
    last_page = get_last_pagination(soup)
    paginated_links = get_paginated_links(last_page)
    prod_links = get_product_links(paginated_links)
    save_csv = get_save_data(prod_links)


def get_url():

    # Goal: Get Bol Search Product URL
    # Return Search_URL & soup for other function

    search_url = 'https://www.efloorball.net/c/443/floorball-sticks'
    #search_url = 'https://www.efloorball.net/c/443/floorball-sticks?pg-start=' + str(item_num) + '#paging'
    headers = USER_AGENT
    page = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    return search_url, soup


def get_last_pagination(soup):

    # Gets the last page of the pagination
    # each page url adds nr. 21
    last_page = soup.find(True, {'class':['paging-sorting']},).get_text().split()[-2]

    return last_page

# Get a list of links to use
def get_paginated_links(last_page):

    link_list = []
    print("===================!| Get Page Links |!===================")
    for num in tqdm(range(int(last_page))):
        x = num * 21       
        link = 'https://www.efloorball.net/c/443/floorball-sticks?pg-start=' + str(x) + '#paging'
        link_list.append(link)

    return link_list


def get_product_links(paginated_links):

    all_prod_list = []
    print("===================!| Get Product Links |!===================")
    for url in tqdm(paginated_links):

        headers = USER_AGENT
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        #print(f'page {url}')


        prod_class = soup.find(True, {'class':['product-listing']},)
        link = [link['href'] for link in prod_class.findAll("a", {"class": "index-product-small"})]

        count = len(link)

        for num in range(count):          
            links = 'https://www.efloorball.net' + str(link[num])
            all_prod_list.append(links)


    return all_prod_list



def get_save_data(prod_links):

    df_product_row = []
    print("===================!| Get Product Details & Save to CSV |!===================")
    for links in tqdm(prod_links):
        headers = USER_AGENT
        page = requests.get(links, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        try:
            name = soup.select('h1[class="product-name"]')[0].get_text()
        except:
            name = ''
        try:
            price = soup.select('p[class="product_variants_price"]')[0].get_text()
        except:
            price = ''

        try:
            color = soup.select('div[class="js-parameter-value parameter-value-div parameter-value-selected"]')[0].get_text()
        except:
            color = ''

        try:
            features = soup.find("table", {"class": "parameter-table text-base mobile-table",})
            features_rows = features.findAll('tr', {})

            feature_dict = {"Name": [],"Key": []}
            for x in features_rows:
                test_list = x.find('td', {}).get_text().replace('\n', ';').split(';')
                y = [i for i in test_list if i]

                feature_dict['Name'].append(y[0])
                feature_dict['Key'].append(y[1])
        except:
            features = ''
            features_rows = ''
            feature_dict = ''

        #print(f"==== {name} ====")

        product_detail = {
            'name': name,
            'price': price,
            'color': color,
            'feature_dict': feature_dict,
            'link': links,
        }

        df_product_row.append(product_detail)


    new_df = pd.DataFrame(df_product_row)
    new_df.to_csv('stick.csv', index=True, header=[
        'name', 'price', 'color', 'feature_dict', 'link'])


