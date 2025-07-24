from . import Base, session
from sqlalchemy import Column, Integer, String, Text

class Fase(Base):
    __tablename__ = "fase"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True) # e.g., "Planning", "Development", "Testing"

    def __init__(self, nombre):
        self.nombre = nombre

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }

    def __repr__(self):
        return f"<Fase(id={self.id}, nombre='{self.nombre}')>"

    @classmethod
    def crear_fase(cls, nombre): # Recibe 'cls' para referirse a la clase Fase
        nueva_fase = cls(nombre=nombre)  # Usar cls() para crear instancias
        session.add(nueva_fase) 
        session.commit() # Commit de la sesión actual
        return nueva_fase
    
    @classmethod
    def obtener_fase_por_id(cls, id):
        fase = session.query(cls).filter(cls.id == id).first()
        if fase:
            return fase.to_dict()
        else:
            return None

    