from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)

def register_models():
    """
    Importa todos os modulos que definem modelos para que sejam registrados
    no metadata do SQLAlchemy antes de operacoes como create_all().
    """
    import delivery.models.role
    import delivery.models.user
    import delivery.models.level
    import delivery.models.business
    import delivery.models.business_owners
    import delivery.models.business_type
    import delivery.models.role_user
    import delivery.models.location
    #import delivery.models.order