import requests
from bs4 import BeautifulSoup
from utils import read_json, write_json
from tqdm import tqdm
from utils import aws_dynamodb

import pdb
import logging
logging.basicConfig(level=logging.ERROR,
                    filename='./logs/speech_scrape.log', filemode='w')


def process_speech_links():

    # # make data copy if it doesn't already exist
    # data_copy = read_json('./data/speech_links.json')
    # try:
    #     write_json('./data/speech_data.json', data_copy, mode='x')
    # except FileExistsError:
    #     logging.info("Copy file aborted as data exists\n")

    # data_dict = read_json('./data/speech_data.json')
    # speech_ids = data_dict.keys()

    dynamodb = aws_dynamodb()
    speech_ids = dynamodb.get_keys()
    for speech_id in tqdm(speech_ids):
        speech_dict = dynamodb.get_item(speech_id)

        # Only scrape if not already scraped
        if "speech_text" not in speech_dict.keys():
            scrape_speech(speech_dict, dynamodb)

            # # write every 100 iterations for safety
            # if (i != 0) and (i % 100) == 0:
            #     write_json('./data/speech_data.json', data_dict)

        else:
            logging.info(
                "speech with id: {}, has already been processed".format(speech_id))

    # write_json('./data/speech_data.json', data_dict)


def scrape_speech(speech_dict, dynamodb_obj):
    url = speech_dict['url']
    response = requests.get(url)
    if response.status_code == requests.codes.ok:
        try:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            content = soup.find(id="content")
            speech_dict["date_published"] = extract_date_published(content)
            speech_dict["speech_context"] = extract_speech_context(content)
            speech_dict["speech_text"] = extract_speech_text(content)
            dynamodb_obj.put_item(speech_dict)

        except Exception as e:
            logging.exception("Scraping Exception for url: {}\n".format(url))

    else:
        logging.error("The url: {}\n returned the status code: {}\n And has not been processed.\n".format(
            url, response.status_code))


def extract_date_published(content):
    time_tag = content.find('time', class_="published")
    timestamp = time_tag["datetime"]
    return timestamp


def extract_speech_text(content):
    content_tag = content.find('div', class_="entry-content")
    return content_tag.text


def extract_speech_context(content):
    content_tag = content.find('div', class_="entry-content")
    context_tag = content_tag.find('em')
    return context_tag.text


if __name__ == '__main__':
    process_speech_links()
