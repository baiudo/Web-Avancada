from invoke import task
from datetime import datetime
import os
import zipfile

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


@task
def zip_windows(c, name=None):

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    zip_filename = name or f"delivery-projeto-{timestamp}.zip"
    zip_path = os.path.abspath(os.path.join("..", zip_filename))

    print(f"→ Criando ZIP: {zip_path}")

    excludes = [
        "venv",
        "__pycache__",
        ".git",
        ".vscode",
        "delivery.egg-info"
    ]

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("."):

            dirs[:] = [d for d in dirs if d not in excludes]

            for file in files:
                if file.endswith((".pyc", ".pyo", ".pyd", ".log", ".db", ".sqlite3")):
                    continue

                filepath = os.path.join(root, file)
                zipf.write(filepath)

    if os.path.exists(zip_path):
        size_mb = os.path.getsize(zip_path) / (1024 * 1024)
        print(f"→ ZIP criado com sucesso: {zip_path}")
        print(f"   Tamanho: {size_mb:.2f} MB")