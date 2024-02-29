# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 08:00:00 2024

@author: Jhonatan Martínez
@email: martinezjha@globalhitss.com
"""

from typing import Dict
import pysftp
from utils.validation import Validation
from utils.my_logger import get_logger


class SFTPConnection:
    """Permite realizar una conexión a SFTP.
    """

    def __init__(self) -> None:
        """Constructor"""
        self.__attributes: set = {'host', 'port', 'user', 'password'}
        self.__connection = None
        self.__logger = get_logger()
        self.__setup: Dict = {}
        self.__validation: Validation = Validation()

    def initialize(self, setup: Dict[str, str]) -> None:
        """Ejecuta el proceso.

        Args:
            setup (Dic[str, str]):
                El diccionario necesita de las siguientes keys:
                - host: Server host.
                - port: Server port.
                - user: SFTP user.
                - password: SFTP password.

        Returns:

        """

        valid, message = self.__validation.check_attribute(setup)
        if not valid:
            self.__handle_warning(f"La configuración es inválida: {message}")

        valid, message = self.__validation.check_missing_keys(self.__attributes, setup)
        if not valid:
            self.__handle_warning(message)

        self.__setup = setup

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

    def close_connection(self) -> None:
        """Cierra la conexión al servidor.
        """
        try:
            if self.__connection:
                self.__connection.close()
                self.__logger.info("La conexión al SFTP fue cerrada.")
        except (pysftp.ConnectionException, Exception) as e:
            self.__handle_error(f"Error al cerrar la conexión al SFTP: {str(e)}")

    def open_connection(self) -> bool:
        """Establece la conexión al servidor SFTP.\n

        Returns:
            bool: El valor de retorno es True si se realiza con éxito, False en caso contrario.
        """
        response: bool = False
        self.__connection = None

        try:
            # This is for no use the host keys
            opciones = pysftp.CnOpts()
            opciones.hostkeys = None
            self.__connection = pysftp.Connection(host=self.__setup["host"],
                                                  port=int(self.__setup["port"]),
                                                  username=self.__setup["user"],
                                                  password=self.__setup["password"],
                                                  cnopts=opciones)
            self.__logger.info(f'Conexión establecida al servidor SFTP:{self.__setup["host"]}')
            response = True
        except (pysftp.ConnectionException, Exception) as e:
            self.__handle_error(f"Error al abrir conexión al SFTP ({self.__setup['host']}): {str(e)}")

        return response

    def change_path(self, path: str) -> bool:
        """Cambia el directorio en el que se va a trabajar en el servidor SFTP.

        Args:
            path (str): Directorio del SFTP en el que se va a trabajar.

        Returns:
            bool: El valor de retorno es True si se realiza con éxito, False en caso contrario.
        """
        response: bool = False

        if self.__connection:
            try:
                self.__connection.cwd(path)
                self.__logger.info(f"Cambiando directorio de trabajo a: {path}")
                response = True
            except (pysftp.ConnectionException, Exception) as e:
                self.__handle_error(f"Error al cambiar de directorio: {str(e)}")
        else:
            self.__handle_warning(f"No hay conexión con el servidor SFTP {self.__setup['host']}.")

        return response

    def upload_file(self, original_file: str, end_file: str) -> bool:
        """Subir archivos al servidor SFTP.

        Args:
            original_file (str): Recibe la ruta absoluta y el archivo a subir. \n
            end_file (str): Nombre con el que se va a guardar el archivo. \n

        Returns:
             bool: El valor de retorno es True si se realiza con éxito, False en caso contrario.
        """
        response: bool = False

        if self.__connection:
            try:
                self.__connection.put(original_file, end_file)
                self.__logger.info(f"El archivo {end_file} fue cargado correctamente.")
                response = True
            except (pysftp.ConnectionException, Exception) as e:
                self.__handle_error(f"Error al subir el archivo: {str(e)}")
        else:
            self.__handle_warning(f"No hay conexión con el servidor SFTP {self.__setup['host']}.")

        return response

    def download_file(self, directory: str, filename: str, final_filename: str) -> bool:
        """Descargar un archivo de un servidor SFTP.

        Args:
            directory (str): Ruta dónde se van a guardar el archivo a descargar. \n
            filename (str): Nombre del archivo a descargar. \n
            final_filename (str): Nombre con el que se va a guardar el archivo.

        Returns:
            bool: El valor de retorno es True si se realiza con éxito, False en caso contrario.
        """
        response: bool = False

        if self.__connection:
            try:
                if self.__connection.isfile(filename):
                    self.__connection.get(filename, directory + "/" + final_filename)
                    self.__logger.info(f"El archivo {final_filename} fue descargado correctamente.")
                    response = True
            except (pysftp.ConnectionException, Exception) as e:
                self.__handle_error(f"Error al descargar el archivo: {str(e)}")
        else:
            self.__handle_warning(f"No hay conexión con el servidor SFTP {self.__setup['host']}.")

        return response

    def download_files(self, directory: str) -> None:
        """Descargar archivos de un servidor SFTP.

        Args:
            directory (str): Ruta dónde se van a guardar los archivos. \n
        """
        try:
            self.__logger.info(f"Descargando archivos desde el directorio {directory}.")
            for file in self.__connection.listdir():
                self.download_file(directory, file, file)
        except Exception as e:
            self.__handle_error(f"Error descargando desde directorio {directory}: {str(e)}")
