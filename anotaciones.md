## Crear Maquina Virtual
> python -m venv nombre_maquina_virtual

# Errores al intentar activar maquina virtual:

> No se puede cargar el archivo... porque la ejecución de scripts está deshabilitada en este sistema

# Solución
> Cambiar la plítica de ejecución de Scripts de Power Shell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> Set-ExecutionPolicy: Comando para cambiar reglas de seguridad de PowerShell sobre ejecición de Scripts
> -ExecutionPolicy RemoteSigned: Elige la regla de Seguridad. RemoteSigned significa que permite ejecutar scripts que yo creo, pero exige una firma de confianza para Scripts descargados de Internet.
> -Scope CurrentUser: Establece el alcance de la regla. CurrentUser significa que el cambio de seguridad solo se aplica a tu usuario de la computadora, no a los demás.

## Instalar Jupyter Lab

> pip install jupyterlab
# Inicializar interfaz de Jupyter
> jupyter lab
# Guardar librerias instaladas de mi entorno virtual en requirements.txt
> pip freeze > requirements.txt

# Ver liibrerias instaladas en el entorno virtual
> pip freeze --local

# Instalar librerias de requirements.txt
> pip install -r requirements.txt

# Instalar libreria django
> pip install django

# Crear configuración de Proyecto django
> django-admin startproject nombre_proyecto

# Levantar Server con django con la configuración...
> python manage.py runserver

# Levantar app después de haber creado la congiguración...
> python manage.py startapp app_cliente