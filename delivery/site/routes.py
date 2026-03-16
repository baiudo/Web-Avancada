from flask import render_template
from delivery.site import bp   # ou from delivery.site import bp  (mas . é melhor)

@bp.route("/")
@bp.route("/home")
def index():
    print("Rota / (index) foi chamada!")   # deve aparecer ao acessar a URL
    return render_template("site/index.html", titulo="Home - Funcionou!")

@bp.route("/teste")
def teste():
    return "<h1>Teste OK – rota /teste funcionando</h1>"

@bp.route("/sobre")
def sobre():
    print("Rota /sobre foi chamada!")
    return render_template("site/sobre.html", titulo="Sobre Nós")

@bp.route("/contato")
def contato():
    print("Rota /contato foi chamada!")
    return render_template("site/contato.html", titulo="Fale Conosco")