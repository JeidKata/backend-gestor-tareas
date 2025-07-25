from . import Base, session
from sqlalchemy import Column, Integer, String, Text

class Fase(Base):
    __tablename__ = "fase"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)

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
        
    @classmethod
    def obtener_fases(cls):
        fases = session.query(cls).all()
        return [fase.to_dict() for fase in fases]
    
    @classmethod
    def actualizar_fase(cls, id, nombre):
        fase = session.query(cls).filter(cls.id == id).first()
        if fase:
            fase.nombre = nombre
            session.commit()
            return fase.to_dict()
        else:
            return None
        
    @classmethod
    def eliminar_fase(cls, id):
        fase = session.query(cls).filter(cls.id == id).first()
        if fase:
            session.delete(fase)
            session.commit()
            return True
        else:
            return False

    