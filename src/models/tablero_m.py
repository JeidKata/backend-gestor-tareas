from . import Base, session
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


    # def __init__(self, nombre, descripcion=None, fecha_entrega=None, estado="activo"):
    #     self.nombre = nombre
    #     self.descripcion = descripcion
    #     self.fecha_entrega = fecha_entrega
    #     self.estado = estado

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
    
    @classmethod
    def crear_tablero(cls, nombre, descripcion, fecha_entrega, estado):
        tablero_nuevo = cls(nombre=nombre, descripcion=descripcion,
                            fecha_entrega=fecha_entrega, estado=estado)
        session.add(tablero_nuevo)
        session.commit()
        return tablero_nuevo.to_dict()
    
    @classmethod
    def obtener_tableros(cls):
        tableros = session.query(cls).all()
        return [tablero.to_dict() for tablero in tableros]
    
    @classmethod
    def obtener_tablero_por_id(cls, id):
        tablero = session.query(cls).filter_by(id=id).first()
        if tablero:
            return tablero.to_dict()
        return None
    
    @classmethod
    def actualizar_tablero(cls, id, nombre=None, descripcion=None, fecha_entrega=None, estado=None):
        tablero = session.query(cls).filter_by(id=id).first()
        if not tablero:
            return None
        
        if nombre:
            tablero.nombre = nombre
        if descripcion:
            tablero.descripcion = descripcion
        if fecha_entrega:
            tablero.fecha_entrega = fecha_entrega
        if estado:
            tablero.estado = estado
        
        session.commit()
        return tablero.to_dict()
    
    @classmethod
    def eliminar_tablero(cls, id):
        tablero = session.query(cls).filter_by(id=id).first()
        session.delete(tablero)
        session.commit()
        return True
    
    @classmethod
    def eliminar_tablero(cls, id):
        tablero = session.query(cls).filter_by(id=id).first()
        if not tablero:
            return False
        session.delete(tablero)
        session.commit()
        return True
