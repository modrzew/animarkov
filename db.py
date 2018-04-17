from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models


engine = create_engine('sqlite:///db.sqlite')
Session = sessionmaker(bind=engine)


def create_schema():
    models.Base.metadata.create_all(engine)
