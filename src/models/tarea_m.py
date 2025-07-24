from . import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Tarea(Base):
    __tablename__ = "tarea"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_inicio = Column(DateTime, nullable=False)
    fecha_fin = Column(DateTime, nullable=True) # Can be null if not yet finished
    estado = Column(String, default="pendiente", nullable=False) # e.g., 'pendiente', 'en progreso', 'completada'

    # Foreign Keys
    fase_id = Column(Integer, ForeignKey("fase.id"), nullable=False)
    persona_id = Column(Integer, ForeignKey("persona.id"), nullable=True) # Can be null if not yet assigned
    tablero_id = Column(Integer, ForeignKey("tablero.id"), nullable=False)

    # Relationships
    fase_asociada = relationship("Fase", back_populates="tareas")
    asignado_a = relationship("Persona", back_populates="tareas_asignadas")
    tablero_asociado = relationship("Tablero", back_populates="tareas")

    def __init__(self, nombre, descripcion, fecha_inicio, estado="pendiente"):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.estado = estado

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "fecha_inicio": self.fecha_inicio.isoformat(),
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
            "estado": self.estado,
            "fase_id": self.fase_id,
            "tablero_id": self.tablero_id
        }
    
    def __repr__(self):
        return (f"<Tarea(id={self.id}, nombre='{self.nombre}', "
                f"tablero_id={self.tablero_id}, fase_id={self.fase_id}, "
                f"persona_id={self.persona_id})>")
