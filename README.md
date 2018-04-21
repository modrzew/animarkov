# Animarkov

Tired of waiting for the announcement of new anime series? Worry not, for now you can generate them by yourself!

`animarkov` parses titles and synopsises of large amount of anime series taken from MyAnimeList, and generates Markov chains based on them. From those chains, legit-sounding new titles and synopsises are generated—some of them even sound plausible!(or at least as plausible as your average anime synopsis)

## Demo

https://anime.modriv.net/

## Installation

`animarkov` requires Python 3.6+. Python virtualenv or other isolation solution (like `pyenv`) is strongly suggested.

To install dependencies, run:

```
pip install -r requirements.txt
```

## Running

### 1. Download

To download data from MAL, run:

```
python cli.py fetch
```

It will open the database (or create it if it doesn't exist), and start filling it with downloaded values.

If you just want to try out the code for fun, then feel free to use the existing database, located in the repository.

### 2. Generate models

To generate models, run:

```
python cli.py generate
```

It will generate models from data found in the database and dump them into `models.json`, so that they can be reused.

In order to regenerate models (e.g. after downloading new portion of data), simply remove `models.json` file and rerun this command.

### 3. Run interface

To run the web interface, run:

```
FLASK_APP=web.py flask run
```

Since this is a quite simple Flask app, all Flask parameters are supported.

### Database

Both `fetch` and `generate` commands operate on a SQLite database, located in `db.sqlite` file. It's meant to be reused between runs.

## License

See [LICENSE.md](LICENSE.md).
