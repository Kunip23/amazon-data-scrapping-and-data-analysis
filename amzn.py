from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import csv
import json
import glob

HEADERS = ({'user-agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0',
            'Accept-Language':'en-US , en;q=0.5'})

print('Enter Amazon Search Term: ', end='')
sr = input()
SEARCH = sr


def generatesPages(search, count):
    links = []

    for i in range(count):
        link = 'https://www.amazon.in/s?k=' + search + '&page=' + str(i+1)
        links.append(link)
    return links


def extract_product_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    products = soup.find_all("div", attrs={"data-component-type": "s-search-result"})

    product_links = []
    for product in products:
        link = product.find("a", attrs={'class': "a-link-normal s-no-outline"})
        if link:
            product_links.append('https://www.amazon.in' + link.get('href'))

    return product_links


def extract_product_details(product_link):
    webpage = requests.get(product_link, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, 'html.parser')

    title = soup.find("span", attrs={'id': "productTitle"})
    rating = soup.find("span", attrs={'class': "a-icon-alt"})
    price = soup.find("span", attrs={'class': "a-price-whole"})

    review_class = 'a-expander-content reviewText review-text-content a-expander-partial-collapse-content'
    reviews = soup.find_all('div',attrs={'class': review_class})
    extracted_reviews = [review.get_text(strip=True) for review in reviews]
    
    extracted_tech = {}
    tech_table = soup.find('table', attrs={'id': "productDetails_techSpec_section_1"})
    
    if tech_table:
        rows = tech_table.find_all('tr')
        for row in rows:
            th = row.find('th')
            td = row.find('td')
            if th and td:
                column = th.get_text(strip=True)
                value = td.get_text(strip=True)
                extracted_tech[column] =value       

    details = {
        "title": title.get_text(strip=True) if title else None,
        "rating": rating.get_text(strip=True) if rating else None,
        "reviews":";" .join(extracted_reviews),
        "price": price.get_text(strip=True) if price else None,
        "link": product_link,
        **extracted_tech
    }
    return details
'''
    print("Title:", details['title'])
    print("Rating:", details['rating'])
    print("Price:", details['price'])
    print("Link:", details['link'])
    print(f"Review Count {len(details['reviews'])}")
    print("Reviews:")
    for review in details['reviews']:
        print("-", review)
    print("Technical Details:")
    for detail in details['tech_details']:
        print(detail)
    
    print("\n")'''

extracted_data =[]

pages = generatesPages(SEARCH, 10)
for page_link in tqdm(pages, desc="Processing pages"):
    html_content = requests.get(page_link, headers=HEADERS).content
    product_links = extract_product_links(html_content)
    for product_link in tqdm(product_links, desc="Extracting Products"):
        details = extract_product_details(product_link)
        extracted_data.append(details)

all_columns = set()
for data in extracted_data:
    all_columns.update(data.keys())

all_columns = sorted(all_columns)

amazon= f"{SEARCH.replace(' ', '_')}_amzn_data.json"
with open(amazon, 'w', encoding='utf-8') as json_file:
    json.dump(extracted_data, json_file, indent=4, ensure_ascii=False)
