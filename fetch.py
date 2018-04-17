import argparse
import logging
import random
import re
import time

import requests
from bs4 import BeautifulSoup

import db
import models


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RequestError(Exception):
    pass


def get_anime(mal_id, url):
    logger.info(f'Getting {url}')
    response = requests.get(url)
    if response.status_code != 200:
        raise RequestError
    try:
        bs = BeautifulSoup(response.text, 'html.parser')
        title = bs.select('h1 span')[0].text
        synopsis = bs.select('span[itemprop=description]')
        if not synopsis:
            return
        synopsis = synopsis[0].text.replace('[Written by MAL Rewrite]', '').strip()
    except Exception as e:
        blah = e
        import pdb; pdb.set_trace()
    return models.Anime(mal_id=mal_id, title=title, synopsis=synopsis)


def get_page(session, page=0):
    logger.info(f'Getting page {page}')
    limit = page * 50
    response = requests.get(f'https://myanimelist.net/topanime.php?limit={limit}')
    bs = BeautifulSoup(response.text, 'html.parser')
    for anchor in bs.select('td.title > a'):
        url = anchor.attrs['href']
        match = re.match(r'https://myanimelist.net/anime/(\d+)/.*', url)
        if not match:
            import pdb; pdb.set_trace()
        mal_id = int(match.group(1))
        if not session.query(models.Anime).get(mal_id):
            for attempt in range(3):
                try:
                    yield get_anime(mal_id, url)
                except RequestError:
                    time.sleep(random.uniform(0.5, 1))
                    continue
                else:
                    break


def main(start_page, end_page):
    session = db.Session()
    for page in range(start_page, end_page):
        for i, anime in enumerate(get_page(session, page)):
            if anime:
                session.add(anime)
            if i > 0 and i % 5 == 0:
                logger.info('Committing')
                session.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_page', type=int)
    parser.add_argument('--end_page', type=int)
    args = parser.parse_args()
    main(args.start_page, args.end_page)
