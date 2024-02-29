# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 16:00:00 2024

@author: Jhonatan Martínez
@email: martinezjha@globalhitss.com
"""
import json
import socket
from email.message import EmailMessage
import smtplib
from typing import Dict, Tuple
from utils.validation import Validation
from utils.my_logger import get_logger


class SMTPConnection:
    """Permite realizar una conexión a un SMTP."""

    def __init__(self) -> None:
        """Constructor."""

        self.__attributes: set = {'host', 'port', 'user', 'password', 'subject', 'recipients'}
        self.__connection = None
        self.__email = EmailMessage()
        self.__logger = get_logger()
        self.__setup: dict = {}
        self.__validation: Validation = Validation()

    def initialize(self, setup: Dict[str, str]) -> None:
        """Ejecuta el proceso.

        Args:
        setup (Dict[str, str]):
            El diccionario necesita de las siguientes keys:
                - host: Server host.
                - port: Server port.
                - user: SMTP user.
                - password: SMTP password.
                - subject: Asunto que va a tener el email.
                - recipients: Correo(s) a los que se va a enviar el email separados por ','.\n

        Returns:
        """
        valid, message = self.__validation.check_attribute(setup)
        if not valid:
            self.__handle_warning(f"La configuración es inválida: {message}")

        valid, message = self.__validation.check_missing_keys(self.__attributes, setup)
        if not valid:
            self.__handle_warning(message)

        self.__setup = setup
        self.__email["From"] = self.__setup['user']

    def __handle_error(self, message: str) -> None:
        """

        Args:
            message (str): Mensaje del error.

        Returns:

        """
        self.__logger.error(message, exc_info=True)

    def __handle_warning(self, message: str) -> None:
        """

        Args:
            message (str): Mensaje del warning.

        Returns:

        """
        self.__logger.warning(message)

    def __close_connection(self) -> None:
        """Cerrar la conexión a la base de datos."""
        try:
            if self.__connection:
                self.__connection.quit()
                self.__logger.info("La conexión al SMTP fue cerrada.")
        except (smtplib.SMTPException, Exception) as e:
            self.__handle_error(f"Error al cerrar la conexión al SMTP: {str(e)}")

    def __open_connection(self) -> None:
        """Crear y obtener la conexión a una base de datos

        Returns:

        """
        self.__connection = None
        try:
            self.__connection = smtplib.SMTP(self.__setup["host"], int(self.__setup["port"]))
            if self.__setup["password"] != "":
                self.__connection.ehlo()
                # Secure the SMTP connection.
                self.__connection.starttls()
                # Identify this cliente to the SMTP server.
                self.__connection.ehlo()
                self.__connection.login(self.__email["From"], self.__setup["password"])
            self.__logger.info(f'Conexión establecida al servidor SMTP: {self.__setup["host"]}')
        except (smtplib.SMTPException, Exception) as e:
            self.__handle_error(f"Error al abrir conexión al SMTP ({self.__setup['host']}): {str(e)}")

    def send_email(self, body: str, html: bool = False, attachment_path: str = None) -> Tuple[bool, str]:
        """Configura el body y permite enviar un correo electrónico.

        Args:
            body (str): Contiene la descripción o cuerpo del email.\n
            html (bool, optional): Email con cuerpo HTML en True. False por defecto
            attachment_path (str, optional): Ruta y nombre del archivo a adjuntar.
        """
        valid: bool = False
        message: str = 'Mensaje enviado correctamente'
        try:
            recipients = str(self.__setup['recipients']).split(sep=",")
            self.__email["To"] = ", ".join(recipients)
            self.__email["Subject"] = str(self.__setup['subject']).strip()
            self.__open_connection()
            if self.__connection:
                # Add content to the email and with type html.
                if html:
                    self.__email.set_content(body, 'html')
                else:
                    self.__email.set_content(body)
                # Adjuntar el archivo al mensaje
                if attachment_path is not None:
                    with open(attachment_path, 'rb') as file:
                        attachment_data = file.read()
                        self.__email.add_attachment(attachment_data,
                                                    maintype='application',
                                                    subtype='octet-stream',
                                                    filename=attachment_path.split(sep="\\")[-1])
                # Enviar el email
                self.__connection.send_message(self.__email)
                valid = True
            else:
                self.__handle_warning(f"No hay conexión con el servidor SMTP {self.__setup['host']}, se tratará de enviar por tunel")
                self.__get_email_data(body, html)
                valid, message = self.__send_email_to_intermediary()

        except (smtplib.SMTPException, Exception) as e:
            self.__handle_error(f"Error al enviar el correo: {str(e)}")

        finally:
            self.__close_connection()

        return valid, message

    def __get_email_data(self, body: str, html: bool = False) -> None:
        """Construye los datos del correo electrónico.

        Args:
            body (str): Contiene la descripción o cuerpo del email
            html (bool, optional): Email con cuerpo HTML en True. False por defecto
        """
        self.__email_data = {
            "host": self.__setup['host'],
            "port": self.__setup['port'],
            "user": self.__setup['user'],
            "password": self.__setup['password'],
            "subject": self.__setup['subject'],
            "recipients": self.__setup['recipients'],
            "body": body,
            "html": html,
            "attachment_path": ""
        }

    def __send_email_to_intermediary(self) -> Tuple[bool, str]:
        """Envía los datos del correo electrónico al servidor intermediario.

        Returns:
            Tuple[bool, str]:
        """
        valid: bool = False
        message: str = 'Correo enviado correctamente'
        try:
            intermediary_address: Tuple[str, int] = ('10.67.106.100', 2552)
            with socket.create_connection(intermediary_address) as client_socket:
                client_socket.sendall(json.dumps(self.__email_data).encode())
                message = client_socket.recv(1024).decode()
                valid = True
        except (smtplib.SMTPException, Exception) as e:
            self.__handle_error(f"Error al enviar el correo: {str(e)}")

        return valid, message
