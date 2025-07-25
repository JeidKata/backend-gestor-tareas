from . import Base, session
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

    # Foreign Keys
    fase_id = Column(Integer, ForeignKey("fase.id"), nullable=False)
    persona_id = Column(Integer, ForeignKey("persona.id"), nullable=True) # Can be null if not yet assigned
    tablero_id = Column(Integer, ForeignKey("tablero.id"), nullable=False)

    # Relationships
    fase_asociada = relationship("Fase", back_populates="tareas_asociadas")
    asignado_a = relationship("Persona", back_populates="tareas_asignadas")
    tablero_asociado = relationship("Tablero", back_populates="tareas")

    def __init__(self, nombre, descripcion, fecha_inicio, fecha_fin=fecha_fin):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "fecha_creacion": self.fecha_creacion.isoformat(),
            "fecha_inicio": self.fecha_inicio.isoformat(),
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
            "fase_id": self.fase_id,
            "persona_id": self.persona_id,
            "tablero_id": self.tablero_id
        }
    
    def __repr__(self):
        return (f"<Tarea(id={self.id}, nombre='{self.nombre}', "
                f"tablero_id={self.tablero_id}, fase_id={self.fase_id}, "
                f"persona_id={self.persona_id})>")
    
    @classmethod
    def crear_tarea(cls, nombre, descripcion, fecha_inicio, fase_id, persona_id, tablero_id):
        nueva_tarea = cls(nombre=nombre, descripcion=descripcion,
                          fecha_inicio=fecha_inicio, fase_id=fase_id,
                          persona_id=persona_id, tablero_id=tablero_id)
        session.add(nueva_tarea)
        session.commit()
        return nueva_tarea.to_dict()
    
    @classmethod
    def obtener_tarea_por_id(cls, id):
        tarea = session.query(cls).filter(cls.id == id).first()
        if tarea:
            return tarea.to_dict()
        else:
            return None
        
    @classmethod
    def listar_tareas(cls):
        tareas = session.query(cls).all()
        return [tarea.to_dict() for tarea in tareas]
    
    @classmethod
    def actualizar_tarea(cls, id, nombre=None, descripcion=None, fecha_inicio=None,
                         fecha_fin=None):
        tarea = session.query(cls).filter(cls.id == id).first()
        if tarea:
            if nombre:
                tarea.nombre = nombre
            if descripcion:
                tarea.descripcion = descripcion
            if fecha_inicio:
                tarea.fecha_inicio = fecha_inicio
            if fecha_fin:
                tarea.fecha_fin = fecha_fin
            session.commit()
            return tarea.to_dict()
        else:
            return None
        
    @classmethod
    def eliminar_tarea(cls, id):
        tarea = session.query(cls).filter(cls.id == id).first()
        if tarea:
            session.delete(tarea)
            session.commit()
            return True
        else:
            return False
