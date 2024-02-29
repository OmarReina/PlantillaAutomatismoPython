# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 08:30:00 2024

@author: Jhonatan Martínez
@email: martinezjha@globalhitss.com
"""
from typing import Dict
import cx_Oracle
from sqlalchemy import create_engine, Engine, orm
from utils.security import Security
from utils.validation import Validation
from utils.my_logger import get_logger


class Database:

    def __init__(self) -> None:
        """Constructor.

        Returns:
            None.
        """
        self.__attributes: set = {'host', 'port', 'sdi', 'user', 'password', 'driver', "client"}
        self.__key: str = ''
        self.__logger = get_logger()
        self.__security: Security = Security()
        self.__session: orm.Session = None
        self.__setup: dict = {}
        self.__validation: Validation = Validation()

    def initialize(self, key: str, setup: Dict[str, str]) -> None:
        """Ejecuta el proceso después de instanciar.

        Args:
            key (str): La llave de encriptación.
            setup (Dict[str, str]):
                El diccionario necesita de las siguientes keys:
                    - host: Server host.
                    - port: Server port.
                    - sdi: Database SDI.
                    - user: Database user.
                    - password: Database password.
                    - driver: Database driver.
                    - client: Database instant client.


        Returns:
            None.
            """
        valid, message = self.__validation.check_attribute(key)
        if not valid:
            self.__handle_warning(f"La llave es inválida: {message}")

        valid, message = self.__validation.check_attribute(setup)
        if not valid:
            self.__handle_warning(f"La configuración es inválida: {message}")

        valid, message = self.__validation.check_missing_keys(self.__attributes, setup)
        if not valid:
            self.__handle_warning(message)

        self.__key = key
        self.__setup = setup
        self.__security.initialize(self.__key)
        self.__create_session()

    def __create_session(self) -> None:
        """Crea el motor y la sesión de la base de datos.

        Returns:

        """
        if self.__session is not None:
            return

        try:
            if 'oracle' in self.__setup['driver'].lower():
                cx_Oracle.init_oracle_client(lib_dir=self.__setup['client'])
            url: str = (
                f"{self.__setup['driver']}://"
                f"{self.__security.decrypt(self.__setup['user'])}:"
                f"{self.__security.decrypt(self.__setup['password'])}@"
                f"{self.__setup['host']}:"
                f"{self.__setup['port']}/"
                f"{self.__setup['sdi']}"
            )
            self.__logger.debug(url)
            engine: Engine = create_engine(url)
            self.__session = orm.Session(engine)

        except (cx_Oracle.DatabaseError,Exception) as e:
            self.__handle_error(
                f"Error creando la sesión de la base de datos: {str(e)}")

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

    def get_attributes(self) -> set:
        """
        Obtiene los atributos de la base de datos.

        Returns:
            set: Los atributos de la base de datos.
        """
        return self.__attributes.copy()

    def get_session(self) -> orm.Session:
        """
        Obtiene la sesión de la base de datos.

        Returns:
            Session: La sesión de la base de datos.
        """
        return self.__session
