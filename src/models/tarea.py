from models import Base, sessionmaker
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
    proyecto_id = Column(Integer, ForeignKey("proyecto.id"), nullable=False)

    # Relationships
    fase_asociada = relationship("Fase", back_populates="tareas")
    asignado_a = relationship("Persona", back_populates="tareas_asignadas")
    proyecto_asociado = relationship("Proyecto", back_populates="tareas")

    def __repr__(self):
        return (f"<Tarea(id={self.id}, nombre='{self.nombre}', "
                f"proyecto_id={self.proyecto_id}, fase_id={self.fase_id}, "
                f"persona_id={self.persona_id})>")
