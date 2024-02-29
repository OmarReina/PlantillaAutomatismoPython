Desarrollo base o plantilla para los automatismos Claro usando Python

Por [Jhonatan Martínez](mailto:martinezjha@globalhitss.com)

Versión 0.0.3

💡 Prerequisitos:

- [Python 3.8.9](https://www.python.org/downloads/release/python-389/)
- [Librerías](requirements.txt)
- [Archivo .env](.env) con al menos los siguientes datos:
  - **APP_VERSION** (Versión que tendrá el aplicativo a desarrollar)
  - **APP_LOG_FILE** (Nombre del archivo plano que guardará el log)
  - **APP_REQUIREMENT_NAME** (Nombre del requerimiento para buscar en la tabla CT_PROPIEDADES)
  - **APP_SECRET_KEY** (Clave para encriptar o desencriptar)
- Variable de entorno ENVIROMENT con alguno de estos valores (DEV, QA, PROD)
- [Propiedades básicas](properties.sql) reemplazar los valores REQ0000_000 con el nombre del requerimiento

# 📚 Primer uso:
- Una vez con los archivos descargados crear un ambiente virtual
    
        virtualenv venv

- Con el ambiente creado y activado instalar las librerías requeridas

        pip install -r requirements.txt

El desarrollo utiliza el patrón MVC que aunque es muy usado para desarrollo web, 
nos sirve también para los automatismos.

# Paquete utils 
Podemos encontrar los archivos:
- **base y database:** Estos nos sirven para la conexión a base de datos
- **my_logger:** Con este podemos agregar tanto en la consola como en un archivo plano lo que va sucediendo en el aplicativo
- **security:** Con este podemos encriptar y desencriptar
- **sftp_connection:** Nos permite conectar a un servidor SFTP, cargar y descargar archivo
- **smtp_connection:** Nos permite conectar a un servidor SMTP para enviar correos electrónicos
- **validation:** Permite realizar validaciones a las configuraciones necesarias

# ¿Qué realiza la plantilla?
- Leer las configuraciones del archivo .env
- Leer las propiedades del requerimiento desde la tabla CT_PROPIEDADES
- En este punto el desarrollador puede agregar lo que el requerimiento pide
- Limpia el archivo .log

# ¿Cómo generar el archivo .exe?
- Modificar el archivo [version_info.txt](version_info.txt) según se requiera para agregar información al .exe, tales como la versión, nombre, descripción, etc. 
- Ejecutar el comando
      
    pyinstaller --onefile --icon=.\logo.ico --version-file version_info.txt main.py

# Notas
- REQ0000_000 cambiarlo por el nombre del requerimiento ejemplo REQ2022_456
- Si se encuentra algún bug, o se necesita realizar una mejora, actualizar esta plantilla, agregar una versión superior.

  Ejemplo esta plantilla está en la versión 0.0.3 el próximo commit hacerlo con el nombre versión 0.0.4 y también la versión al principio de este archivo
- No hacer commits a esta plantilla cuando trabaje en algún automatismo