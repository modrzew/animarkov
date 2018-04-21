import random

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Anime(Base):
    __tablename__ = 'anime'

    mal_id = Column(Integer, primary_key=True)
    title = Column(String)
    synopsis = Column(Text)


def get_title(model):
    return model.make_short_sentence(200, 30, tries=200)


SECOND_PARAGRAPH_START = (
    'However',
    'However,',
    'But',
    'Meanwhile,',
    'Meanwhile',
    'Unfortunately',
    'Unfortunately,',
    'Although',
    'Though',
    'Suddenly,',
    'Suddenly',
    'Yet',
    'Yet,',
    'Nevertheless,',
    'Moreover,',
    'Fortunately,',
    'Furthermore,',
    'Thus',
    'Thus,',
    'Unable',
    'Later',
    'Later,',
)


def get_synopsis(model):
    while True:
        first = model.make_short_sentence(1000, 100, tries=100)
        for word in SECOND_PARAGRAPH_START:
            if first.startswith(word):
                continue
        break
    second = ''
    while len(second) < 200:
        beginning = random.choice(SECOND_PARAGRAPH_START)
        second = model.make_sentence_with_start(beginning, tries=100)
    return [first, second]
