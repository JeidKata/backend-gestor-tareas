from models import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

class Persona(Base):
    __tablename__ = "persona"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False) # In a real app, store hashed passwords!

    # Relationship to Tarea (One-to-Many: One Persona can have many Tareas assigned)
    tareas_asignadas = relationship("Tarea", back_populates="asignado_a")

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
