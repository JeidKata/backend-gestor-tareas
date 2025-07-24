from . import Base
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

class Tablero(Base):
    __tablename__ = "tablero"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_entrega = Column(DateTime, nullable=True)
    estado = Column(String, default="activo", nullable=False) # e.g., 'activo', 'completado', 'en espera'

    # Relationship to Tarea (One-to-Many: One Tablero can have many Tareas)
    tareas = relationship("Tarea", back_populates="tablero_asociado")

    def __init__(self, nombre, descripcion=None, fecha_entrega=None, estado="activo"):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_entrega = fecha_entrega
        self.estado = estado

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fecha_creacion": self.fecha_creacion,
            "fecha_entrega": self.fecha_entrega,
            "estado": self.estado,
        }

    def __repr__(self):
        return f"<Proyecto(id={self.id}, nombre='{self.nombre}')>"
    