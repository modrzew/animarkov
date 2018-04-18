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


def get_synopsis(model):
    first = model.make_short_sentence(1000, 100, tries=100)
    second = ''
    while len(second) < 150:
        beginning = random.choice((
            'However',
            'However,',
            'But',
            'Meanwhile,',
            'Unfortunately',
            'Unfortunately,',
            'Although',
            'Though',
            'Suddenly,',
            'Suddenly',
            'Yet',
            'Nevertheless,',
            'Moreover,',
            'Fortunately,',
            'Furthermore,',
            'Thus',
            'Thus,',
            'Unable',
        ))
        second = model.make_sentence_with_start(beginning, tries=100)
    return [first, second]
