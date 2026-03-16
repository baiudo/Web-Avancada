from flask import Blueprint

bp = Blueprint(
    'site',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/site/static'
)

def init_app(app):
    app.register_blueprint(bp)
    print("Blueprint 'site' registrado OK")

# ────────────────────────────────────────────────
# ESSA PARTE EH OBRIGATORIA para carregar as rotas!
# Tem que estar DEPOIS da criação do bp
# ────────────────────────────────────────────────
from delivery.site.routes import *          # opção 1 – importa tudo
# OU
# from . import routes         # opção 2 – importa o módulo (as rotas são executadas no import)

print("Rotas do módulo site importadas")   # ← deve aparecer no terminal