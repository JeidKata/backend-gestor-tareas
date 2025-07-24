from models import Base
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

class Proyecto(Base):
    __tablename__ = "proyecto"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_entrega = Column(DateTime, nullable=True)
    estado = Column(String, default="activo", nullable=False) # e.g., 'activo', 'completado', 'en espera'

    # Relationship to Tarea (One-to-Many: One Proyecto can have many Tareas)
    tareas = relationship("Tarea", back_populates="proyecto_asociado")

    def __repr__(self):
        return f"<Proyecto(id={self.id}, nombre='{self.nombre}')>"
    