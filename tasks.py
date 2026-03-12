from invoke import task


@task
def install(c, dev=True):
    """
    Instala o projeto.
    """
    if dev:
        c.run('pip install -e ".[dev,test]"', echo=True)
    else:
        c.run("pip install .", echo=True)


@task
def uninstall(c):
    """
    Remove o pacote instalado.
    """
    c.run("pip uninstall -y delivery", echo=True)


@task
def run(c):
    """
    Executa a aplicacao Flask.
    """
    c.run("flask run", pty=True)


@task
def test(c):
    """
    Executa os testes automatizados.
    """
    c.run("pytest tests -v", pty=True)


@task
def lint(c):
    """
    Verifica qualidade de codigo.
    """
    c.run("flake8", pty=True)


@task
def format(c):
    """
    Formata o codigo automaticamente.
    """
    c.run("black .", pty=True)