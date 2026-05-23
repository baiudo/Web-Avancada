import click
from flask import current_app
from delivery.ext.db import db
from delivery.models import *


# ==========================================================
# INIT
# ========================================================== 
def init_app(app):

    # ======================================================
    # CREATE DB
    # ======================================================
    @app.cli.command("create-db")
    def create_db():
        """Cria todas as tabelas do banco de dados."""
        # Garantimos que os modelos foram carregados via __init__
        import delivery.models 
        db.create_all()
        click.echo("Banco de dados materializado com sucesso!")


    # ======================================================
    # DROP DB
    # ======================================================
    @app.cli.command("drop-db")
    @click.confirmation_option(prompt="Tem certeza que deseja apagar TUDO?")
    def drop_db():
        """
        Remove todas as tabelas do banco (Cuidado!).
        """
        db.drop_all()
        click.echo("Banco de dados removido.")


    # ======================================================
    # CREATE ROOT
    # ======================================================
    @app.cli.command("create-root")
    def create_root():
        """
        Cria o usuario Root e as permissoes basicas de sistema (Seguro para Producao).
        """
        try:
            click.echo("Configurando acesso Root do sistema...")

            # 1. Garante a existencia do Nível 'God'
            level_god = Level.query.filter_by(name="God").first()
            if not level_god:
                level_god = Level(name="God", description="Acesso total ao sistema: recomendado apenas para root.")
                db.session.add(level_god)
                click.echo("- Nivel 'God' criado.")

            # 2. Garante a existencia do Papel 'Root'
            role_root = Role.query.filter_by(name="Root").first()
            if not role_root:
                role_root = Role(name="Root")
                db.session.add(role_root)
                click.echo("- Papel 'Root' criado.")

            db.session.flush() # Sincroniza IDs antes de criar o usuario e o vinculo

            # 3. Cria ou recupera o usuario Wanderson Santana
            user = User.query.filter_by(email="wanderson@dev.com").first()
            if not user:
                user = User(
                    name="Wanderson Santana",
                    email="wanderson@dev.com",
                    cpf="109.876.543-21",
                    is_active=True
                )
                db.session.add(user)
                click.echo(f"- Usuario {user.name} criado.")
            else:
                click.echo(f"- Usuario {user.name} ja existe.")

            db.session.flush()

            # 4. Cria o vinculo de acesso Global (sem Business)
            access = RoleUser.query.filter_by(
                user_id=user.id, 
                role_id=role_root.id, 
                business_id=None
            ).first()

            if not access:
                access = RoleUser(
                    user=user,
                    role=role_root,
                    level=level_god,
                    business=None
                )
                db.session.add(access)
                click.echo("- Permissoes de Root vinculadas com sucesso.")
            else:
                click.echo("- O usuario ja possui permissoes de Root.")

            db.session.commit()
            click.echo("Operacao finalizada com sucesso.")

        except Exception as e:
            db.session.rollback()
            click.echo(f"Erro ao criar root: {e}")
            raise click.ClickException(str(e))


    # ======================================================
    # SEMEANDO DADOS EM AMBIENTE DE DESENVOLVIMENTO
    # ======================================================
    @app.cli.command("seed-dev")
    def seed_dev():
        """
        Popula o banco com cenario completo (Apenas em Development).
        """
       
        click.echo("Isso ira popular o banco com dados de teste. Deseja continuar? [y/N]: ", nl=False)

        confirm = input().strip().lower()

        if confirm not in ("y", "yes", "s", "sim"):
            click.echo("Operacao cancelada.")
            return

        try:
            click.echo("Iniciando Seed de Desenvolvimento...")

            # 1. Niveis
            levels_data = [
                ("God", "Acesso total ao sistema: recomendado apenas para root."),
                ("Premium", "Nivel de acesso e oferta superior."),
                ("Basic", "Nivel intermediário de acesso e operacional."),
                ("Standard", "Nivel padrão de acesso.")
            ]
            levels = {}
            for name, desc in levels_data:
                lv = Level.query.filter_by(name=name).first()
                if not lv:
                    lv = Level(name=name, description=desc)
                    db.session.add(lv)
                levels[name] = lv

            # 2. Papeis
            role_names = ["Root", "Sustainer", "Administrador", "Gerente", "Operador", "Cliente"]
            roles = {}
            for name in role_names:
                r = Role.query.filter_by(name=name).first()
                if not r:
                    r = Role(name=name)
                    db.session.add(r)
                roles[name] = r

            # 3. Tipos de Negocio
            bt_data = [
                ("Pizzaria", "Estabelecimentos especializados em pizzas e calzones."),
                ("Hamburgueria", "Especialistas em hambúrgueres artesanais e lanches rápidos."),
                ("Restaurante", "Alimentação variada com serviço de pratos executivos ou à la carte."), 
                ("Farmácia", "Comércio de medicamentos, produtos de higiene e cuidados pessoais.")
            ]
            b_types = {}
            for name, desc in bt_data:
                bt = BusinessType.query.filter_by(name=name).first()
                if not bt:
                    bt = BusinessType(name=name, description=desc)
                    db.session.add(bt)
                b_types[name] = bt

            # 4. Localizacao (Cidade)
            city = City.query.filter_by(name="Vila Velha", state="ES").first()
            if not city:
                city = City(name="Vila Velha", state="ES", country="Brasil", region="Sudeste")
                db.session.add(city)

            db.session.flush() # Sincroniza IDs para os relacionamentos a seguir

            # 5. Usuarios (Root e Proprietario)
            root_user = User.query.filter_by(email="wanderson@dev.com").first()
            if not root_user:
                root_user = User(
                    name="Wanderson Santana",
                    email="wanderson@dev.com",
                    cpf="109.876.543-21",
                    is_active=True
                )
                db.session.add(root_user)

            joao = User.query.filter_by(email="joao@email.com").first()
            if not joao:
                joao = User(
                    name="João Paulo",
                    email="joao@email.com",
                    cpf="111.111.111-11",
                    is_active=True
                )
                db.session.add(joao)

            db.session.flush()

            # 6. Empresa e seu Endereço
            biz = Business.query.filter_by(cnpj="12.345.678/0001-99").first()
            if not biz:
                biz = Business(
                    owners=[joao],
                    trade_name="Bonna Pizza Express",
                    corporate_name="Joao Alimentos LTDA",
                    cnpj="12.345.678/0001-99",
                    business_type=b_types["Pizzaria"]
                )
                db.session.add(biz)
                db.session.flush()

                # Endereço da Empresa
                addr = Address(
                    road="Avenida Beira Mar",
                    number=500,
                    district="Itapuã",
                    zipcode="29101-000",
                    city=city,
                    business=biz # Vinculado a empresa
                )
                db.session.add(addr)

            # 7. Associacoes de Acesso (RoleUser)
            # Root como Root Global (sem empresa)
            if not RoleUser.query.filter_by(user=root_user, role=roles["Root"]).first():
                db.session.add(RoleUser(
                    user=root_user,
                    role=roles["Root"],
                    level=levels["God"],
                    business=None
                ))

            # Joao como Administrador da sua propria Pizzaria
            if not RoleUser.query.filter_by(user=joao, business=biz).first():
                db.session.add(RoleUser(
                    user=joao,
                    role=roles["Administrador"],
                    level=levels["Premium"],
                    business=biz
                ))

            db.session.commit()


            # Criando Maria de forma Pythonica (tudo de uma vez, sem flush)
            # Simulando comportamento esperado em um formulario no frontend
            # Criando a estrutura aninhada de Maria Mara
            vitoria = City.query.filter_by(name="Vitória", state="ES").first() or \
                          City(name="Vitória", state="ES", country="Brasil", region="Sudeste")
            
            maria = User(
                name="Maria Mara",
                email="maria@email.com",
                cpf="222.222.222-22",
                is_active=True
            )
            
            # Criando o endereco pessoal de Maria (opcional, se quiser separar do da empresa)
            maria.addresses.append(
                    Address(road="Rua das Palmeiras", number=100, district="Praia do Canto", city=vitoria)
            )
            
            # Criando a empresa e o vinculo de acesso simultaneamente
            hamburgueria = Business(
                owners=[maria],
                trade_name="Maria Burger Haus",
                corporate_name="Maria Mara Lanches LTDA",
                cnpj="33.333.333/0001-33",
                business_type=b_types["Hamburgueria"],
                address=Address(
                    road="Avenida Dante Michelini", 
                    number=1500, 
                    district="Jardim da Penha", 
                    city=vitoria
                )
            )

            # Vinculamos Maria à empresa através do papel de Administradora
            maria.role_associations.append(
                RoleUser(
                    role=roles["Administrador"],
                    level=levels["Standard"],
                    business=hamburgueria
                )
            )

            # Ao adicionar Maria, o SQL Alchemy "puxa" a Hamburgueria (pelo owner e pela associação)
            # e os Endereços (pelas listas), salvando tudo na ordem correta.
            db.session.add(maria)
            db.session.commit()


            # 1. Preparando dependencias de localizacao
            cariacica = City.query.filter_by(name="Cariacica", state="ES").first() or \
                        City(name="Cariacica", state="ES", country="Brasil", region="Sudeste")

            # 2. Criar Pedro José e suas múltiplas relações
            pedro = User(
                name="Pedro José",
                email="pedro@email.com",
                cpf="444.444.444-44",
                is_active=True
            )

            # Endereço Pessoal em Cariacica
            pedro.addresses.append(
                Address(
                    road="Avenida Expedicionário Vicente Caetano", 
                    number=250, 
                    district="Campo Grande", 
                    zipcode="29146-010", 
                    city=cariacica
                )
            )

            # --- Vinculos de Acesso (RoleUser) ---
            # A. Cliente Comum (Acesso Global/Standard)
            pedro.role_associations.append(
                RoleUser(
                    role=roles["Cliente"],
                    level=levels["Standard"],
                    business=None  # Sem vinculo com empresa especifica
                )
            )

            # B. Gerente na Hamburgueria da Maria (Level Premium)
            # Usamos a variavel 'hamburgueria' que foi instanciada no bloco da Maria
            pedro.role_associations.append(
                RoleUser(
                    role=roles["Gerente"],
                    level=levels["Premium"],
                    business=hamburgueria
                )
            )

            # C. Operador na Pizzaria do Joao (Level Basic)
            # Usamos a variável 'biz' que representa a pizzaria do Joao no seu seed
            pedro.role_associations.append(
                RoleUser(
                    role=roles["Operador"],
                    level=levels["Basic"],
                    business=biz 
                )
            )

            # 3. Persistencia
            db.session.add(pedro)
            db.session.commit()

            # Relacionamento Muitos-para-Muitos entre usuarios e empresas
            # 1. Preparar dependências de localização e catálogo
            vila_velha = City.query.filter_by(name="Vila Velha", state="ES").first()
            guarapari = City.query.filter_by(name="Guarapari", state="ES").first() or \
                        City(name="Guarapari", state="ES", country="Brasil", region="Sudeste")

            restaurante_type = b_types["Restaurante"]

            # 2. Criar os Usuários
            joaquim = User(
                name="Joaquim Lourenço",
                email="joaquim@email.com",
                cpf="555.555.555-55",
                is_active=True
            )
            joaquim.addresses.append(
                Address(road="Rua Rio Branco", number=10, district="Praia da Costa", city=vila_velha)
            )

            fatima = User(
                name="Fátima Almeida",
                email="fatima@email.com",
                cpf="666.666.666-66",
                is_active=True
            )
            fatima.addresses.append(
                Address(road="Rua Joaquim da Silva Lima", number=500, district="Centro", city=guarapari)
            )

            # 3. Criar o Restaurante (Joaquim como owner principal no banco)
            moquecaria = Business(
                # Vejam a magica: uma lista de objetos User
                owners=[joaquim, fatima],
                trade_name="Moquecaria Capixaba",
                corporate_name="Joaquim & Fatima Restaurante LTDA",
                cnpj="44.444.444/0001-44",
                business_type=restaurante_type,
                description="Especializado na autêntica moqueca capixaba e frutos do mar.",
                address=Address(
                    road="Avenida Beira Mar", 
                    number=2000, 
                    district="Praia do Morro", 
                    city=guarapari
                )
            )

            # --- Vínculos de Acesso (RoleUser) ---

            # Joaquim: Administrador Standard
            joaquim.role_associations.append(
                RoleUser(
                    role=roles["Administrador"],
                    level=levels["Standard"],
                    business=moquecaria
                )
            )

            # Fátima: Administradora Premium
            fatima.role_associations.append(
                RoleUser(
                    role=roles["Administrador"],
                    level=levels["Premium"],
                    business=moquecaria
                )
            )

            # Fátima: Cliente da Plataforma (Nível Basic - Global)
            fatima.role_associations.append(
                RoleUser(
                    role=roles["Cliente"],
                    level=levels["Basic"],
                    business=None
                )
            )

            # 4. Persistência
            db.session.add_all([joaquim, fatima]) # O SQLAlchemy salvará a 'moquecaria' por cascata
            db.session.commit()

            click.echo("Seed concluido com sucesso! Sistema pronto para continuar desenvolvimento.")

        except Exception as e:
            db.session.rollback()
            click.echo(f"Erro catastrófico no seed: {e}")