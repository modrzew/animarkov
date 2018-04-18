import json
import logging
import random

import markovify

from . import db
from . import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED = ' ,.!?;:-–—'


class ModelsNotGeneratedError(Exception):
    pass


def get_models(session):
    titles = None
    synopsises = None
    for i, anime in enumerate(session.query(models.Anime)):
        try:
            if ' ' in anime.title:
                title_model = markovify.Text(
                    ''.join(ch for ch in anime.title if ch.isalnum() or ch in ALLOWED),
                    state_size=1,
                )
                if titles:
                    titles = markovify.combine(models=[titles, title_model])
                else:
                    titles = title_model
            if len(anime.synopsis) > 50:
                synopsis = anime.synopsis.replace('\n', ' ').replace('\r', ' ')
                synopsis_model = markovify.Text(
                    ''.join(ch for ch in synopsis if ch.isalnum() or ch in ALLOWED),
                    state_size=3,
                )
                if synopsises:
                    synopsises = markovify.combine(models=[synopsises, synopsis_model])
                else:
                    synopsises = synopsis_model
        except Exception as e:
            import pdb; pdb.set_trace()
            continue
        if i > 0 and i % 50 == 0:
            logger.info(f'Added {i} entries')
    return titles, synopsises


def load_models(session=None):
    try:
        with open('models.json') as f:
            models = json.load(f)
        return markovify.Text.from_dict(models['titles']), markovify.Text.from_dict(models['synopsises'])
    except (FileNotFoundError, json.JSONDecodeError):
        if not session:
            raise ModelsNotGeneratedError
        titles, synopsises = get_models(session)
        models = {'titles': titles.to_dict(), 'synopsises': synopsises.to_dict()}
        with open('models.json', 'w') as f:
            json.dump(models, f)
        return titles, synopsises


def main():
    session = db.Session()
    titles, synopsises = load_models(session)
    print(titles.make_short_sentence(200, 30, tries=200))
    print(synopsises.make_short_sentence(1000, 100, tries=50))
    sentence = ''
    while len(sentence) < 150:
        beginning = random.choice(('However', 'But'))
        sentence = synopsises.make_sentence_with_start(beginning, tries=100)
    print(sentence)
