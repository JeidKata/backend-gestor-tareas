from . import Base, session
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

class Persona(Base):
    __tablename__ = "persona"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False) # In a real app, store hashed passwords!

    # Relationships
    tareas_asignadas = relationship("Tarea", back_populates="asignado_a", cascade="all, delete-orphan")

    def __init__(self, nombre, correo, password):
        self.nombre = nombre
        self.correo = correo
        self.password = password

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
        }

    def __repr__(self):
        return f"<Persona(id={self.id}, nombre='{self.nombre}', correo='{self.correo}')>"

    @classmethod
    def crear_persona(cls, nombre, correo, password):
        nueva_persona = cls(nombre=nombre, correo=correo, password=password)
        session.add(nueva_persona)
        session.commit()
        return nueva_persona.to_dict()
    
    @classmethod
    def obtener_persona_por_id(cls, persona_id):
        persona = session.query(cls).filter(cls.id == persona_id).first()
        if persona:
            return persona.to_dict()
        else:
            return None
        
    @classmethod
    def obtener_personas(cls):
        personas = session.query(cls).all()
        return [persona.to_dict() for persona in personas]
    
    @classmethod
    def actualizar_persona(cls, persona_id, nombre=None, correo=None, password=None):
        persona = session.query(cls).filter(cls.id == persona_id).first()
        if persona:
            if nombre:
                persona.nombre = nombre
            if correo:
                persona.correo = correo
            if password:
                persona.password = password
            session.commit()
            return persona.to_dict()
        else:
            return None
        
    @classmethod
    def eliminar_persona(cls, persona_id):
        persona = session.query(cls).filter(cls.id == persona_id).first()
        if persona:
            session.delete(persona)
            session.commit()
            return True
        else:
            return False
    