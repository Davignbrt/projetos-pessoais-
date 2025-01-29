from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario, Base  # Certifique-se de que o modelo está correto
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecreto'
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],echo=True)  # echo=True exibe as queries no console

# Configura a sessão
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

# Configuração do Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Definir função para carregar usuário
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Iniciar o SQLAlchemy
db = SQLAlchemy(app)

Base.metadata.create_all(engine)

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
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        # Consulta no banco e verificação de senha
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('home'))
        else:
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

if __name__ == '__main__':
    app.run(debug=True)
