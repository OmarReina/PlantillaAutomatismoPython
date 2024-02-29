# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 08:30:00 2024

@author: Jhonatan Martínez
@email: martinezjha@globalhitss.com
"""

import os
from dotenv import load_dotenv
from loguru import logger

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

logger.add(os.getenv('APP_LOG_FILE'),
           rotation="500 MB",
           level="DEBUG" if os.environ.get("ENVIRONMENT") != "PROD" else "INFO",
           backtrace=True,
           diagnose=True)


def get_logger() -> logger:
    """Devuelve el logger

    Returns:
        logger: El logger
    """
    return logger
