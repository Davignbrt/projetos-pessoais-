from database import Base, engine
from models import Usuario, Produtos  # Importar os modelos

# Criar as tabelas
if __name__ == "__main__":
    print("Criando as tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)  # Cria todas as tabelas definidas
    print("Tabelas criadas com sucesso!")
