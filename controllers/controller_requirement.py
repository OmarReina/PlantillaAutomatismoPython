# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 08:30:00 2024

@author: Jhonatan Martínez
@email: martinezjha@globalhitss.com
"""
import os
from dotenv import dotenv_values
from controllers.controller_property import ControllerProperty
from models.model_requirement import ModelRequirement
from database.database import Database
from utils.validation import Validation
from utils.my_logger import get_logger


class ControllerRequirement:
    def __init__(self):
        """
        Carga las configuraciones del archivo .env y las propiedades de la base de datos
        """
        self.__attributes: set = {'app_version', 'app_log_file', 'app_requirement_name', 'app_secret_key'}
        self.__database: Database = Database()
        self.__logger = get_logger()
        self.__requirement: ModelRequirement = ModelRequirement()
        self.__validation: Validation = Validation()

    def initialize(self) -> None:
        """
        Ejecuta el proceso

        Returns:

        """
        try:
            if self.__read_configurations():
                self.__read_properties()
            else:
                self.__logger.warning('Programa sin configuraciones')
        except Exception as e:
            self.__logger.error(f"Error leyendo el requerimiento: {str(e)}", exc_info=True)

    def __read_configurations(self) -> bool:
        """
        Lee las configuraciones del archivo .env

        Returns:
            bool: True si se cargaron las configuraciones, False en caso contrario
        """
        response: bool = False
        self.__logger.info('Leyendo las configuraciones del programa')

        try:
            dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
            configurations_dict = dict(dotenv_values(dotenv_path))
            configurations_dict = {key.lower(): value for key, value in configurations_dict.items()}

            if self.__validation.check_missing_keys(self.__attributes, configurations_dict):
                self.__logger.info(f'Se leyeron {len(configurations_dict)} configuraciones')
                self.__logger.debug(configurations_dict)
                self.__requirement = ModelRequirement()
                self.__requirement.initialize(configurations=configurations_dict,
                                              environment=os.environ.get("ENVIRONMENT"),
                                              log_file=configurations_dict['app_log_file'],
                                              name=configurations_dict['app_requirement_name'],
                                              secret_key=configurations_dict['app_secret_key'],
                                              version=configurations_dict['app_version'])
                response = True
        except Exception as e:
            self.__logger.error(f"Error leyendo las configuraciones: {str(e)}", exc_info=True)

        return response

    def __read_properties(self) -> bool:
        """
        Lee las propiedades de la base de datos

        Returns:
            bool: True si se cargaron las propiedades, False en caso contrario
        """
        response: bool = False
        self.__logger.info('Leyendo las propiedades del programa')

        try:
            db_setup: dict = self.__get_db_setup()
            self.__database = Database()
            self.__database.initialize(self.__requirement.get_secret_key(), db_setup)
            controller_property: ControllerProperty = ControllerProperty()
            controller_property.initialize(self.__database)
            self.__requirement.set_properties(controller_property.get_properties(self.__requirement.get_name()))
            self.__logger.info(f'Se leyeron {len(self.__requirement.get_properties())} propiedades')
            self.__logger.debug(self.__requirement.get_properties())
            response = True
        except Exception as e:
            self.__logger.error(f"Error leyendo las propiedades: {str(e)}", exc_info=True)

        return response

    def __get_db_setup(self) -> dict:
        """
        Obtiene la configuración de la base de datos

        Returns:
            dict: Configuración de la base de datos
        """
        db_setup: dict = {}
        try:
            keys = self.__database.get_attributes()
            attributes: set = {f'{self.__requirement.get_environment().lower()}_db_{key}' for key in keys}
            db_config: dict = self.__requirement.get_configurations()
            if self.__validation.check_missing_keys(attributes, db_config):
                db_setup = {key.split('_')[-1]: db_config[key] for key in attributes}
        except Exception as e:
            self.__logger.error(f"Error leyendo la configuración de la base de datos: {str(e)}", exc_info=True)

        return db_setup

    def get_requirement(self) -> ModelRequirement:
        """
        Obtiene el requerimiento

        Returns:
            ModelRequirement: Requerimiento

        """
        return self.__requirement
