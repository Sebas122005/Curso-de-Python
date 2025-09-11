# Sistema CRUD - Cuentas Bancarias

Sistema de gestión de cuentas bancarias desarrollado con Python, Tkinter y MySQL siguiendo el patrón de arquitectura MVC.

## 🚀 Características

- **Gestión de Clientes**: CRUD completo para clientes del banco
- **Gestión de Cuentas**: CRUD completo para cuentas bancarias
- **Gestión de Usuarios**: Sistema de autenticación y usuarios
- **Interfaz Gráfica**: Interfaz intuitiva desarrollada con Tkinter
- **Base de Datos**: Integración con MySQL
- **Patrón MVC**: Arquitectura bien estructurada y mantenible
- **Validaciones**: Validaciones robustas en todas las capas
- **Reportes**: Estadísticas y reportes del sistema

## 📋 Requisitos

### Software Necesario
- Python 3.7 o superior
- MySQL 5.7 o superior
- Git (opcional)

### Dependencias de Python
```
pymysql==1.1.0
```

## 🛠️ Instalación

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd crud_cuentas_banco
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar Base de Datos

#### 3.1. Crear Base de Datos
```sql
CREATE DATABASE banco_peru_db;
```

#### 3.2. Ejecutar Script SQL
```bash
mysql -u root -p banco_peru_db < script.sql
```

#### 3.3. Configurar Conexión
Editar el archivo `config/config.ini`:
```ini
[mysql_config]
host = localhost
port = 3306
user = tu_usuario
password = tu_contraseña
db = banco_peru_db
```

### 4. Ejecutar la Aplicación
```bash
python main.py
```

## 📁 Estructura del Proyecto

```
crud_cuentas_banco/
├── config/
│   └── config.ini                 # Configuración de BD
├── models/                        # Capa de Modelo
│   ├── base_model.py             # Modelo base
│   ├── cliente.py                # Modelo Cliente
│   ├── usuario.py                # Modelo Usuario
│   ├── cuenta.py                 # Modelo Cuenta
│   └── catalogo.py               # Modelos de catálogos
├── controllers/                   # Capa de Controlador
│   ├── base_controller.py        # Controlador base
│   ├── cliente_controller.py     # Controlador Cliente
│   ├── cuenta_controller.py      # Controlador Cuenta
│   └── usuario_controller.py     # Controlador Usuario
├── views/                        # Capa de Vista
│   ├── base_view.py              # Vista base
│   ├── main_window.py            # Ventana principal
│   ├── cliente_view.py           # Vista Cliente
│   └── cuenta_view.py            # Vista Cuenta
├── database/                     # Gestión de BD
│   └── connection.py             # Conexión a BD
├── utils/                        # Utilidades
│   ├── validators.py             # Validaciones
│   └── helpers.py                # Funciones auxiliares
├── tests/                        # Pruebas
├── script.sql                    # Script de BD
├── main.py                       # Punto de entrada
├── master.py                     # Compatibilidad
├── requirements.txt              # Dependencias
├── RULES.md                      # Reglas del proyecto
├── PASO_A_PASO.md               # Guía paso a paso
└── README.md                     # Este archivo
```

## 🎯 Uso del Sistema

### Pantalla Principal
Al iniciar la aplicación, verás la pantalla principal con:
- Menú de navegación
- Botones de acceso rápido
- Información del sistema

### Gestión de Clientes
1. Selecciona "Clientes" → "Gestionar Clientes"
2. Completa el formulario con los datos del cliente
3. Usa los botones para:
   - **Nuevo**: Limpiar formulario para nuevo cliente
   - **Guardar**: Guardar cliente (crear o actualizar)
   - **Editar**: Cargar datos del cliente seleccionado
   - **Eliminar**: Eliminar cliente seleccionado
   - **Limpiar**: Limpiar formulario

### Gestión de Cuentas
1. Selecciona "Cuentas" → "Gestionar Cuentas"
2. Completa el formulario con los datos de la cuenta
3. Usa "Generar Número" para crear automáticamente el número de cuenta
4. Los botones funcionan igual que en clientes

### Reportes
- Selecciona "Reportes" → "Estadísticas Generales"
- Ve estadísticas de clientes y cuentas

## 🔧 Configuración Avanzada

### Personalizar Validaciones
Edita `utils/validators.py` para agregar nuevas validaciones.

### Personalizar Interfaz
Modifica `views/base_view.py` para cambiar el estilo general.

### Agregar Nuevas Entidades
1. Crea el modelo en `models/`
2. Crea el controlador en `controllers/`
3. Crea la vista en `views/`
4. Agrega la funcionalidad en `main_window.py`

## 🐛 Solución de Problemas

### Error de Conexión a BD
1. Verifica que MySQL esté ejecutándose
2. Confirma que la base de datos existe
3. Revisa las credenciales en `config/config.ini`
4. Verifica permisos del usuario

### Error de Importación
1. Asegúrate de estar en el directorio correcto
2. Verifica que todas las dependencias estén instaladas
3. Revisa que los archivos `__init__.py` existan

### Error de Validación
1. Revisa que todos los campos requeridos estén completos
2. Verifica el formato de los datos (email, fechas, etc.)
3. Consulta los logs en `sistema_bancario.log`

## 📝 Logs

El sistema genera logs en `sistema_bancario.log` con información detallada sobre:
- Conexiones a la base de datos
- Operaciones CRUD
- Errores y excepciones
- Actividad general del sistema

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Desarrolladores

- Desarrollado como parte del Mega Curso de Python
- Patrón MVC implementado
- Sistema CRUD completo

## 📞 Soporte

Para soporte técnico o preguntas:
1. Revisa la documentación en `RULES.md` y `PASO_A_PASO.md`
2. Consulta los logs del sistema
3. Verifica la configuración de la base de datos

---

**¡Disfruta usando el Sistema CRUD de Cuentas Bancarias!** 🏦
