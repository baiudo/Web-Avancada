from flask_debugtoolbar import DebugToolbarExtension

toolbar = DebugToolbarExtension()

def init_app(app):
    """Inicializa a Flask-DebugToolbar"""
    toolbar.init_app(app)