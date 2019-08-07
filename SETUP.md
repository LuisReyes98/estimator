# Requerimientos

Python 3

## Base de datos

Nombre: `estimator`

## Comandos de setup en ubuntu

Crear entorno virtual:

```shell
python3 -m venv venv
```

Activar entorno virtual en ubuntu

```shell
source venv/bin/activate
```

Ver librerias instaladas:

```shell
pip freeze
```

Instalar requirements.txt

```shell
pip install -r requirements.txt
```

## Configurando Postgresql

Primero instalar [postgresql](https://www.postgresql.org/download/) en el sistema

Para accerder a la base de datos que crea por defecto al instalarse en consola hacer

```shell
psql postgres
```

o

```shell
psql
```

esto abrira la consola de postgresql
la cual puedes cerrar con

```shell
\q
```

Listar usuarios existentes

```shell
\du+
```

Listar bases de datos

```shell
\l
```

Crear usuario nuevo

```shell
CREATE USER nombre_de_usuario WITH PASSWORD 'contraseña';
```

Crear base de datos

```shell
CREATE DATABASE nombre_de_base_de_datos WITH OWNER nombre_de_usuario;
```

Crear Base de datos del proyecto

```shell
CREATE DATABASE estimator WITH OWNER luis;
```

Borrar base de datos

```shell
DROP DATABASE IF EXISTS estimator;
```

Conectar a base de datos

```shell
\c database_name
```

Ver tablas una vez conectado

```shell
\dt
```

Ver la tabla

```shell
\d nombre_tabla
```

### Referencias para POSTGRESQL

- [PostgreSQL en Django](https://medium.com/agatha-codes/painless-postgresql-django-d4f03364989)
- [PostgreSQL en consola](https://www.godaddy.com/garage/how-to-install-postgresql-on-ubuntu-14-04/)

## Migraciones en django

ver migraciones

```shell
python manage.py makemigrations
```

aplicar migraciones

```shell
python manage.py migrate
```

## Recomendaciones

- crear un super user con `python manage.py createsuperuser`
mi superusuario de desarrollo
correo: `admin@email.com`
contraseña: `admin`
