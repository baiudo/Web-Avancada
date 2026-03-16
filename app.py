from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configurações básicas (obrigatórias para debugtoolbar e segurança)
    app.config['SECRET_KEY'] = 'minha-chave-secreta-muito-longa-123456'
    app.config['DEBUG'] = True

    # Inicialização das extensões
    from delivery.ext.config import init_app as init_config
    init_config(app)

    # Debug toolbar (se você já configurou)
    # from delivery.ext.debugtoolbar import init_app as init_toolbar
    # init_toolbar(app)

    # <<<< Registro do blueprint site >>>>
    from delivery.site import init_app as init_site
    init_site(app)

    # Debug: confirme que as rotas foram registradas
    print("Rotas registradas:")
    print(app.url_map)

    return app