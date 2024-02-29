# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 12:30:00 2024

@author: Jhonatan Martínez
@email: martinezjha@globalhitss.com
"""
import cryptocode
from utils.validation import Validation


class Security:
    def __init__(self) -> None:
        self.__validation = Validation()
        self.__key: str = ""

    def initialize(self, key: str) -> None:
        self.__validate(key)
        self.__key = key

    def __validate(self, str_value: str) -> None:
        valid, message = self.__validation.check_attribute(str_value)
        if not valid:
            raise ValueError(message)

    def decrypt(self, value: str) -> str:
        """Desencriptar un valor

        Args:
            value (str): Valor a desencriptar.

        Returns:
            str: valor desencriptado
        """
        self.__validate(value)

        try:
            value: str = cryptocode.decrypt(value, self.__key)
        except Exception as e:
            raise Exception(f"Error al desencriptar el valor: {e}")

        return value

    def encrypt(self, value: str) -> str:
        """Encriptar un valor

        Args:
            value (str): Valor a encriptar.

        Returns:
            str: valor encriptado
        """
        self.__validate(value)

        try:
            value: str = cryptocode.encrypt(value, self.__key)
        except Exception as e:
            raise Exception(f"Error al encriptar el valor: {e}")

        return value
