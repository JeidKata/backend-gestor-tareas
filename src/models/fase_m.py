from . import Base
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

class Fase(Base):
    __tablename__ = "fase"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True) # e.g., "Planning", "Development", "Testing"


    # Relationship to Tarea (One-to-Many: One Fase can have many Tareas)
    tareas = relationship("Tarea", back_populates="fase_asociada")

    def __init__(self, nombre):
        self.nombre = nombre

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
        }

    def __repr__(self):
        return f"<Fase(id={self.id}, nombre='{self.nombre}')>"
    