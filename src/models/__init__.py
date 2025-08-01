from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

DATABASE_URL = "sqlite:///my_project.db"
engine = create_engine(DATABASE_URL)
conexion = engine.connect()

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = scoped_session(SessionLocal)