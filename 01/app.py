from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Usuario, Produtos  # Importa a instância db e os modelos

# Inicializa a aplicação Flask
app = Flask(__name__)

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecreto'

# Inicializa o SQLAlchemy
db.init_app(app)

# Configuração do Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Função para carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Cria as tabelas dentro do contexto da aplicação
with app.app_context():
    db.create_all()

# Rota de registro de usuário
@app.route('/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        # Gerar o hash da senha do usuário
        hash_senha = generate_password_hash(senha)

        # Adicionando usuário no banco
        novo_usuario = Usuario(nome=nome, email=email, senha=hash_senha)
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Registro bem-sucedido! Faça login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Rota de login
@app.route('/login', methods=['POST', 'GET'])
def login():
    print('ola')
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        # Consulta no banco e verificação de senha
        usuario = Usuario.query.filter_by(email=email).first()
        print(usuario)
        if usuario and check_password_hash(usuario.senha, senha):
            print('02')
            login_user(usuario)
            return redirect(url_for('home'))
        else:
            print('03')
            flash('Email ou senha incorretos!', 'error')

    return render_template("login.html")

# Rota protegida (somente para usuários logados)
@app.route('/home')
@login_required
def home():
    return render_template('home.html', usuario=current_user)

# Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da conta!', 'info')
    return redirect(url_for('login'))

# Executa a aplicação
if __name__ == '__main__':
    app.run(debug=True)