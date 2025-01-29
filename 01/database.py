from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados
DATABASE_URI = 'sqlite:///meubanco.db'  # SQLite (arquivo local)
engine = create_engine(DATABASE_URI, echo=True)  # echo=True exibe as queries no console

# Base para os modelos
Base = declarative_base()

# Configura a sessão
Session = sessionmaker(bind=engine)
session = Session()