from flask import Flask, render_template

import generate
import models

app = Flask('animarkov')


@app.route('/')
def index():
    try:
        titles, synopsises = generate.load_models()
    except generate.ModelsNotGeneratedError:
        return 'Models not generated'
    title = models.get_title(titles)
    synopsis = models.get_synopsis(synopsises)
    return render_template('index.html', title=title, synopsis=synopsis)
