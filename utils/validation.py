"""
Created on Wed Feb 14 08:30:00 2024

@author: Jhonatan Martínez
@email: martinezjha@globalhitss.com
"""
from typing import Tuple


class Validation:

    @staticmethod
    def check_missing_keys(attributes: set, dictionary: dict) -> Tuple[bool, str]:
        """
        Verifica que existan los atributos o keys en un diccionario.

        Returns:
            bool: True si los atributos existen, False en caso contrario
            str: Mensaje del proceso
        """
        response: bool = True

        valid, message = Validation.check_attribute(attributes)
        if valid:
            valid, message = Validation.check_attribute(dictionary)
            if valid:
                message = "Los atributos existen."
                try:
                    missing: list = [key for key in attributes if str(key).lower() not in map(str.lower, dictionary.keys())]
                    if missing:
                        message = f"Faltan los siguientes atributos: {missing}"
                        response = False
                except Exception as e:
                    response = False
                    message = f"Error validando atributos: {str(e)}"
            else:
                response = valid
        else:
            response = valid

        return response, message

    @staticmethod
    def check_attribute(value: any) -> Tuple[bool, str]:
        """
        Verifica que el valor sea una cadena de texto y que no esté vació.

        Args:
            value (any): valor a verificar

        Returns:
            bool: True si es una cadena de texto, False en caso contrario
            str: Mensaje del proceso
        """
        response: bool = False
        message: str = f"El valor de la variable es valido."
        try:
            if value:
                if isinstance(value, str):
                    if value.strip() != "":
                        response = True
                elif isinstance(value, (dict, set)):
                    if len(value) > 0:
                        response = True
                else:
                    response = True
            else:
                message = f"El valor de la variable no puede ser None o Null "
        except Exception as e:
            message = f"Error validando el valor de la variable: {str(e)}"

        return response, message
