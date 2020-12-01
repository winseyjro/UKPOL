import string
import requests
from bs4 import BeautifulSoup
from utils import aws_dynamodb
from tqdm import tqdm
from hashlib import blake2b
from array import array
import pdb


def retrieve_links():
    letters = [letter for letter in string.ascii_lowercase if letter != 'x']
    base_urls = ['http://www.ukpol.co.uk/speeches/speeches-{}/'.format(
        letter) for letter in letters]

    # hardcode replacement of surname c as link is broken
    base_urls = ['http://www.ukpol.co.uk/speeches/c/' if url ==
                 'http://www.ukpol.co.uk/speeches/speeches-c/' else url for url in base_urls]

    # speech_links = {}

    # instantiate DB class
    dynamodb = aws_dynamodb()
    for base_url in tqdm(base_urls):
        page_links = scrape_page_links(base_url, dynamodb)
        # for link_dict in page_links:
        #     speech_links.update(link_dict)

    # write_json('./data/speech_links.json', speech_links)


def scrape_page_links(base_url, dynamodb_obj):
    html = requests.get(base_url).content
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find(id="content")

    link_tags = content.find_all('a')

    for link_tag in link_tags:
        speech_url = link_tag.get('href')
        speech_title = link_tag.text

        speech_id = blake2b(speech_url.encode(),
                            digest_size=10).hexdigest()
        speech_dict = {'speech_id': speech_id,
                       'url': speech_url, 'title': speech_title}

        # only put if item not already in DB!
        if not dynamodb_obj.check_key(speech_dict['speech_id']):
            dynamodb_obj.put_item(speech_dict)


if __name__ == '__main__':
    retrieve_links()
