#Manual de Instalación
##Sistema de Gestión de Riesgos de Seguridad Informática
##1. Requisitos Previos
-Python 3.10 o superior
-Git
-Virtualenv
-Base de datos SQL
-Cuenta y API Key de Shodan
##2. Clonar el Repositorio
Abre una terminal y ejecuta:
git clone https://github.com/JohannCalva/InventarioRiesgosWebApp
cd InventarioRiesgosWebApp
###3. Crear y Activar el Entorno Virtual
python -m venv venv
venv/Scripts/activate
###4. Instalar dependencias
pip install django
pip install python-dotenv
pip install shodan
pip install pyodbc
pip install django-mssql-backend
###5. Configuración Inicial
5.1 Variables de Entorno
Cree un archivo .env en la raíz del proyecto (si aplica) o edite settings.py y configure:
SHODAN_API_KEY = 'TU_API_KEY_DE_SHODAN'
Si no se configura, la aplicación funcionará sin la importación OSINT desde Shodan.
5.2. Conexion a base de datos SQL
En el archivo settings.py, en el apartado DATABASES, ingresar la información de su base de datos local:
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'RiesgoCiberneticoDB', #Recuerde ejecutar en SQL CREATE DATABASE RiesgoCiberneticoDB antes
        'USER': 'nombreusuario',
        'PASSWORD': 'contrasenia',
        'HOST': 'nombredehost',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}
###6. Aplicar Migraciones
python manage.py makemigrations
python manage.py migrate
###7. Ejecutar el servidor de Desarrollo
python manage.py runserver
Abra su navegador y acceda a:
http://127.0.0.1:8000/
