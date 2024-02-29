# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 08:30:00 2024

@author: Jhonatan Martínez
@email: martinezjha@globalhitss.com
"""
import json

from sqlalchemy.exc import SQLAlchemyError

from models.model_property import ModelProperty
from database.database import Database
from utils.my_logger import get_logger
from utils.validation import Validation


class ControllerProperty:
    def __init__(self):
        self.__database: Database = Database()
        self.__logger = get_logger()
        self.__validation = Validation()

    def initialize(self, database: Database) -> None:
        valid, message = self.__validation.check_attribute(database)
        if not valid:
            self.__handle_warning(f"La conexión a la base de datos es inválida: {message}")

        self.__database = database

    def __handle_warning(self, message: str) -> None:
        """

        Args:
            message (str): Mensaje del warning.

        Returns:

        """
        self.__logger.warning(message)
        raise Exception(message)

    def get_properties(self, requirement_name: str) -> dict:
        """
        Obtiene las propiedades del requerimiento desde la base de datos

        Args:
            requirement_name (str): Nombre del requerimiento

        Returns:
            dict: Lista de propiedades

        """
        response: dict = {}
        self.__logger.info('Consultando las propiedades en la base de datos')
        requirement_name = requirement_name.strip()

        if not requirement_name:
            self.__logger.warning('El nombre del requerimiento no puede estar vacío')
            return response

        try:
            with self.__database.get_session() as session:
                query = session.query(ModelProperty).filter(ModelProperty.rq == requirement_name).all()
                for row in query:
                    name: str = row.nombre_propiedad
                    value: str = row.valor_propiedad.strip()
                    response[name] = json.loads(value) if value.startswith('{') else value
        except (SQLAlchemyError, Exception) as e:
            self.__logger.error(f"Error consultando las propiedades: {str(e)}", exc_info=True)

        return response
