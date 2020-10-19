import string
import requests
from bs4 import BeautifulSoup
from utils import read_json, write_json
from tqdm import tqdm


def retrieve_links():
    letters = [letter for letter in string.ascii_lowercase if letter != 'x']
    base_urls = ['http://www.ukpol.co.uk/speeches/speeches-{}/'.format(
        letter) for letter in letters]

    # hardcode replacement of surname c as link is broken
    base_urls = ['http://www.ukpol.co.uk/speeches/c/' if url ==
                 'http://www.ukpol.co.uk/speeches/speeches-c/' else url for url in base_urls]

    speech_links = {}
    for base_url in tqdm(base_urls):
        page_links = scrape_page_links(base_url)
        for link_dict in page_links:
            speech_links.update(link_dict)

    write_json('./data/speech_links.json', speech_links)


def scrape_page_links(base_url):
    html = requests.get(base_url).content
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find(id="content")

    link_tags = content.find_all('a')
    speech_link_list = []

    for link_tag in link_tags:
        speech_url = link_tag.get('href')
        speech_title = link_tag.text
        speech_id = hash(speech_url)
        speech_dict = {speech_id: {'url': speech_url, 'title': speech_title}}
        speech_link_list.append(speech_dict)

    return speech_link_list


if __name__ == '__main__':
    retrieve_links()
