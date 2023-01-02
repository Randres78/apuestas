from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///database/usuarios.db', connect_args={'check_same_thread': False})

Session = sessionmaker(bind=engine)
session = Session()

# Vinculacion
Base = declarative_base()