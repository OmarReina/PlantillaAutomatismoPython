# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 08:30:00 2024

@author: Jhonatan Martínez
@email: martinezjha@globalhitss.com
"""

from database.base import Base
from sqlalchemy import Column, String, Integer, Text


class ModelProperty(Base):
    """Clase que almacena las propiedades de un requerimiento."""
    __tablename__ = 'CT_PROPIEDADES'
    id_propiedad = Column(Integer, primary_key=True)
    nombre_propiedad = Column(String(150))
    valor_propiedad = Column(Text)
    rq = Column(String(20))
    descripcion = Column(String(500))

    def __str__(self):
        return (f"ModelProperty(id_propiedad={self.id_propiedad}, nombre_propiedad={self.nombre_propiedad}, "
                f"valor_propiedad={self.valor_propiedad}, rq={self.rq}")
