import logging
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)
    # Configuracao recomendada para desenvolvimento:
    # Mostra mensagens DEBUG e INFO no console
    if app.debug:
        app.logger.setLevel(logging.DEBUG)


    # ----------------------------------------------------------
    # Personalizacao do CLI no sistema
    # ----------------------------------------------------------
    from delivery.ext.cli import init_app as init_cli
    init_cli(app)

    # ----------------------------------------------------------
    # Configuracao da aplicacao (variaveis de ambiente)
    # ----------------------------------------------------------
    from delivery.ext.config import init_app as init_config
    init_config(app)
    
    if test_config:
        app.config.update(test_config)

    # ----------------------------------------------------------
    # Inicializacao do banco de dados
    # ----------------------------------------------------------
    from delivery.ext.db import init_app as init_db
    init_db(app)

    # Registro dos modelos no metadata do SQLAlchemy
    from delivery.ext.db import register_models
    register_models()

    # ----------------------------------------------------------
    # Outras extensoes
    # ----------------------------------------------------------
    if not app.config.get("TESTING"):
        from delivery.ext.wtf import init_app as init_wtf
        init_wtf(app)

    from delivery.ext.debugtoolbar import init_app as init_toolbar
    init_toolbar(app)

    # ----------------------------------------------------------
    # Blueprints (camada de apresentacao)
    # ----------------------------------------------------------
    from delivery.views import init_app as init_site
    init_site(app)
    
    return app