def init_app(app):
    app.config["SECRET_KEY"] = "sua-chave-secreta-aqui" # mudar em producao!
    app.config["DEBUG"] = True

    # Editor de templates apenas em modo debug
    if app.debug:
        app.config["DEBUG_TB_TEMPLATE_EDITOR_ENABLED"] = True
        app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False