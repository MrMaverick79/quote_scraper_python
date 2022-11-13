import os
import requests  #makes http requests
from bs4 import BeautifulSoup #parser for html
import pandas as pd 



base_url="https://quotes.toscrape.com" #the base url for all queries

#Get the all of the tag names from the main page
def get_tag_names(doc):

    top_tags = doc.find_all('span', {'class': 'tag-item'}) #these are the top ten tags from the webpage

    #get the titles of the top tags
    top_tag_list = []
    for tag in top_tags:
        top_tag_list.append(tag.text.strip())
    return top_tag_list

#get the url for the tags
def get_tag_urls(doc):

    top_tags = doc.find_all('span', {'class': 'tag-item'}) #these are the top ten tags from the webpage
    #get the urls for the top tags
    top_tag_urls = []
    for tag in top_tags:
        top_tag_urls.append(base_url +'/tag/{}'.format(tag.text.strip()))

    return top_tag_urls


def scrape_tags():
    base_url="https://quotes.toscrape.com" #the base url for all queries
    response = requests.get(base_url)
    
    #check if success
      #check success
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(tag_url))
    
    tag_doc = BeautifulSoup(response.text, 'html.parser')


    tag_dict = {
        'name': get_tag_names(tag_doc),
        'url': get_tag_urls(tag_doc)
    }

    return pd.DataFrame(tag_dict)


def get_tag_page(tag_url):

    response = requests.get(tag_url)
    #check success
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(tag_url))
    
    #parse using BS
    tag_doc = BeautifulSoup(response.text, 'html.parser')
    return tag_doc

def get_tag_details(tag_doc):

    tag_details_dict = {
        'quotes' : get_quote(tag_doc),
        'by': get_by(tag_doc)
    }

    return pd.DataFrame(tag_details_dict)

#scrape a specific tag
def scrape_tag(tag_url, tag_name):

    fname = tag_name 
    if os.path.exists(fname):
        print("The file {} already exists. Skipping...".format(fname))
        return
    
    tag_df = get_tag_details(get_tag_page(tag_url))
    tag_df.to_csv(fname, index=None)


def get_quote(doc):
    #get the quotes from a tag page
    quote_class = "text"
    all_quote_tags = doc.find_all('span', {'class': quote_class})

    all_quotes = []
    for quote in all_quote_tags:
        all_quotes.append(quote.text.strip())
    
    return all_quotes

def get_by(doc):
    #get the 'speakers' (by) of the quotes from a tag page
    by_class = 'author'
    all_by_tags = doc.find_all('small', {'class': by_class})

    all_by = []
    for by in all_by_tags:
        all_by.append(by.text.strip())

    return all_by
 
#Activate the functions above

def scrape_tag_pages():
    print('Scraping the quotes from the top 10 tags...')
    tags_df= scrape_tags()

    #create a folder to store them
    os.makedirs('tags', exist_ok=True)
    for index, row in tags_df.iterrows():
        print('Scraping quotes from "{}" at "{}"'.format(row['name'], row['url']))
        scrape_tag(row['url'], 'tags/{}.csv'.format(row['name']))

if __name__ == "__main__":
    scrape_tag_pages()

