from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from models import Usuario, Produtos
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#iniciar o sqlalchemy
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        hash_senha = generate_password_hash(senha)
        
        novo_usuario = Usuario(nome=nome, email=email, senha=hash_senha)
        db.session.add(novo_usuario)
        db.session.commit()

    return render_template('register.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        usuario = usuario.query.filter_by(email=email).fist()
        if usuario and check_password_hash(usuario.senha, senha):
            return redirect(url_for('home_page'))
        else:
            flash('email ou senha incorretos!!', 'error')

        return render_template("login.html")
    