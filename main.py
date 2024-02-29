# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 09:00:00 2024

@author: Jhonatan Martínez
@email: martinezjha@globalhitss.com
"""
from datetime import datetime, timedelta
from controllers.controller_requirement import ControllerRequirement
from models.model_requirement import ModelRequirement
from utils.smtp_connection import SMTPConnection
from utils.my_logger import get_logger


class Main:
    def __init__(self):
        self.__logger = get_logger()
        self.__requirement: ModelRequirement = ModelRequirement()
        self.__start_task()

    def __start_task(self) -> None:
        """
        Ejecuta la tarea

        Returns:

        """
        self.__logger.info('-' * 30 + ' Iniciando la ejecución del programa ' + '-' * 30)
        controller_requirement: ControllerRequirement = ControllerRequirement()
        controller_requirement.initialize()
        self.__requirement = controller_requirement.get_requirement()

        if self.__requirement.get_properties():
            self.__logger.info("Realizando tarea")
            try:
                self.__to_do_task()
            except Exception as e:
                self.__logger.error(f"Error realizando la tarea: {e}", exc_info=True)
        else:
            self.__logger.warning('Programa sin propiedades')
        self.__end_task()

    def __to_do_task(self) -> None:
        ########## Reemplace con el código de la tarea ##########
        email: SMTPConnection = SMTPConnection()
        email.initialize(self.__requirement.get_properties()['email'])
        email.send_email(body="Mensaje de prueba")
        ##################################################

    def __end_task(self) -> None:
        """
        Finaliza la tarea

        Returns:

        """
        self.__delete_log()
        self.__logger.info('-' * 30 + ' Finalizando la ejecución del programa ' + '-' * 30)

    def __delete_log(self) -> None:
        """Eliminar historial de logs
        """

        self.__logger.info("Preparando para eliminar historial del log")
        try:
            final_date = (
                    datetime.now() - timedelta(days=int(self.__requirement.get_properties().get('log_days', 1)))
            ).date()
            with open(self.__requirement.get_log_file(), 'r') as log:
                lines = log.readlines()
            filtered_lines = []
            deleted_line: bool = False
            for line in lines:
                try:
                    line_date = datetime.strptime(line[:10], '%Y-%m-%d').date()
                    if line_date >= final_date:
                        deleted_line = False
                        filtered_lines.append(line)
                    else:
                        deleted_line = True
                except ValueError:
                    if not deleted_line:
                        filtered_lines.append(line)
            with open(self.__requirement.get_log_file(), 'w') as log:
                log.writelines(filtered_lines)
        except Exception as e:
            self.__logger.error(f"Error al borrar el historial de log: {str(e)}", exc_info=True)


if __name__ == '__main__':
    main = Main()
