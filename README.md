﻿# Sistema de Gestión - Cafetería Pamplonesa
# More Coffee - Sistema de Gestión de Cafetería

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

## Desarrolladores
- Diego Trujillo
- Pablo Quintana

## Características Principales
### Gestión de Roles

- Administrador
- Cajero
- Cocinero
- Mesero
- Cliente

### Gestión de inventario

- Articulos
- Precios
- Proveedores

### Atención automatizada del cliente

- El cliente ordena su orden el mismo
- La facturación es automática.
- Puede cancelar orden si desea.

### Login por ajustado para cada rol

- El administrador tiene vista de todo lo que sucede en el aplicativo
- Cada uno de los empleados tiene una vista diferente dependiendo de su rol
- Fácil de utilizar e intuitivo


## Requisitos Previos
- Python 3.10+
- PostgreSQL 14+
- pip (gestor de paquetes de Python)

## Instalación y Configuración

1. Clonar repositorio:

git clone https://github.com/Raxelthuwu/More-coffe.git
cd more-coffee

2. Crear entorno virtual

python -m venv venv
# Windows
.\venv\Scripts\Activate
# macOS/Linux
source venv/bin/activate

3. Instalar dependencias

pip install -r requirements.txt

4. Configurar base de datos

DJANGO_SECRET_KEY='tu-clave-secreta-aqui'
DEBUG=True
DB_ENGINE=django.db.backends.postgresql
DB_HOST=localhost
DB_PORT=5432
DB_NAME=morecoffee_db
DB_USER=morecoffee_user
DB_PASSWORD=tu_contraseña_segura

5. Ejecuta las migraciones

python manage.py migrate

6. Ejecuta el servidor

python manage.py runserver


## Contribución

- Haz fork del proyecto
- Crea una rama (git checkout -b feature/nueva-funcionalidad)
- Haz commit de tus cambios (git commit -m 'Añade nueva funcionalidad')
- Haz push a la rama (git push origin feature/nueva-funcionalidad)
- Abre un Pull Request




