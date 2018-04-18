try:
    from .animarkov.web import app
except ImportError:
    from animarkov.web import app
