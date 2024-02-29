# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 08:30:00 2024

@author: Jhonatan Martínez
@email: martinezjha@globalhitss.com
"""

import re
from utils.validation import Validation
from utils.my_logger import get_logger


class ModelRequirement:
    def __init__(self) -> None:
        """constructor"""

        self.__configurations: dict = {}
        self.__environment: str = ""
        self.__log_file: str = ""
        self.__logger = get_logger()
        self.__name: str = ""
        self.__secret_key: str = ""
        self.__validation: Validation = Validation()
        self.__version: str = ""
        self.__properties: dict = {}

    def initialize(self, configurations: dict, environment: str, log_file: str, name: str, secret_key: str, version: str) -> None:
        """

        Args:
            configurations (dict): configuraciones del archivo .env
            environment (str): ambiente donde se encuentra el aplicativo
            log_file (str): nombre del archivo .log
            name (str): Nombre del requerimiento
            secret_key (str): Clave secreta
            version (str): Versión del aplicativo

        Returns:

        """

        valid, message = self.__validation.check_attribute(configurations)
        if not valid:
            self.__handle_warning(f"La configuración es inválida: {configurations}")

        valid, message = self.__validation.check_attribute(environment)
        if not valid:
            self.__handle_warning(f"El ambiente es inválido: {message}")

        valid, message = self.__validation.check_attribute(log_file)
        if not valid:
            self.__handle_warning(f"El archivo log es inválido: {message}")

        valid, message = self.__validation.check_attribute(name)
        if not valid:
            self.__handle_warning(f"El nombre es inválido: {message}")

        valid, message = self.__validation.check_attribute(secret_key)
        if not valid:
            self.__handle_warning(f"La llave es inválida: {message}")

        valid, message = self.__validation.check_attribute(version)
        if not valid:
            self.__handle_warning(f"La versión es inválida: {message}")

        self.__configurations = configurations
        self.__environment = environment
        self.__log_file = log_file
        self.__name = self.__validate_name(name)
        self.__secret_key = secret_key
        self.__version = version

    def __str__(self) -> str:
        return (f"ModelRequirement(name={self.__name}, configurations={self.__configurations}, "
                f"environment={self.__environment}, log_file={self.__log_file}, properties={self.__properties})")

    def __handle_error(self, message: str) -> None:
        """

        Args:
            message (str): Mensaje del error.

        Returns:

        """
        self.__logger.error(message, exc_info=True)
        raise Exception(message)

    def __handle_warning(self, message: str) -> None:
        """

        Args:
            message (str): Mensaje del warning.

        Returns:

        """
        self.__logger.warning(message)
        raise Exception(message)

    def __validate_name(self, name: str) -> str:
        """Validar el nombre del requerimiento.

        Args:
            name (str): Nombre del requerimiento

        Returns:
            str: El nombre del requerimiento
        """
        patron = r'^[Rr][Ee][Qq]\d{4}_\d+$'
        if re.match(patron, name):
            name = name.upper()
        else:
            raise Exception(f"El nombre del requerimiento '{name}' no es válido.")

        return name

    def get_configurations(self) -> dict:
        """Obtener las configuraciones del requerimiento.

        Returns:
            Dict:
        """

        return self.__configurations

    def get_environment(self) -> str:
        """Obtener el entorno del requerimiento.

        Returns:
            str:
        """
        return self.__environment

    def get_log_file(self) -> str:
        """Obtener el archivo de registro del requerimiento.

        Returns:
            str:
        """
        return self.__log_file

    def get_name(self) -> str:
        """Obtener el nombre del requerimiento.

        Returns:
             str:
        """
        return self.__name

    def get_properties(self) -> dict:
        """Obtener las propiedades del requerimiento.

        Returns:
            Dict:
        """
        return self.__properties

    def get_secret_key(self) -> str:
        """Obtener la clave secreta del requerimiento.

        Returns:
            str:
        """
        return self.__secret_key

    def get_version(self) -> str:
        """Obtener la versión del requerimiento.

        Returns:
            str:
        """
        return self.__version

    def set_properties(self, properties: dict) -> None:
        """Establecer las propiedades del requerimiento.

        Args:
            properties (dic): Guarda en memoria las propiedades del requerimiento.
        """

        self.__properties = properties
