from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Cria uma instância do SQLAlchemy
db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    
    # Relacionamento com Produtos
    produtos = db.relationship('Produtos', back_populates='usuario')

class Produtos(db.Model):
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    # Relacionamento com Usuario
    usuario = db.relationship('Usuario', back_populates='produtos')