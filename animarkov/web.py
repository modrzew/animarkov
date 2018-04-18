from flask import Flask, render_template

from . import generate
from . import models

app = Flask(__name__)


CACHED = {
    'models': None,
}


@app.route('/')
def index():
    if not CACHED['models']:
        try:
            CACHED['models'] = generate.load_models()
        except generate.ModelsNotGeneratedError:
            return 'Models not generated'
    titles, synopsises = CACHED['models']
    title = models.get_title(titles)
    synopsis = models.get_synopsis(synopsises)
    return render_template(
        'index.html',
        title=title,
        synopsis=synopsis,
        count=len(titles.parsed_sentences),
    )
