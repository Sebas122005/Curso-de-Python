# REGLAS DEL PROYECTO - CRUD CUENTAS BANCARIAS

## 📋 INFORMACIÓN GENERAL
- **Proyecto**: Sistema CRUD de Cuentas Bancarias
- **Base de Datos**: MySQL (banco_peru_db)
- **Patrón de Arquitectura**: Modelo-Vista-Controlador (MVC)
- **Lenguaje**: Python 3.x
- **Interfaz**: Tkinter
- **ORM**: PyMySQL

## 🏗️ ESTRUCTURA DEL PROYECTO

```
crud_cuentas_banco/
├── config/
│   └── config.ini                 # Configuración de base de datos
├── models/                        # Capa de Modelo
│   ├── __init__.py
│   ├── base_model.py             # Clase base para todos los modelos
│   ├── cliente.py                # Modelo Cliente
│   ├── usuario.py                # Modelo Usuario
│   ├── cuenta.py                 # Modelo Cuenta
│   ├── tarjeta.py                # Modelo Tarjeta
│   ├── transaccion.py            # Modelo Transacción
│   ├── agencia.py                # Modelo Agencia
│   └── catalogo.py               # Modelos de catálogos
├── controllers/                   # Capa de Controlador
│   ├── __init__.py
│   ├── base_controller.py        # Controlador base
│   ├── cliente_controller.py     # Controlador Cliente
│   ├── cuenta_controller.py      # Controlador Cuenta
│   ├── tarjeta_controller.py     # Controlador Tarjeta
│   └── transaccion_controller.py # Controlador Transacción
├── views/                        # Capa de Vista
│   ├── __init__.py
│   ├── base_view.py              # Vista base
│   ├── main_window.py            # Ventana principal
│   ├── cliente_view.py           # Vista Cliente
│   ├── cuenta_view.py            # Vista Cuenta
│   └── tarjeta_view.py           # Vista Tarjeta
├── database/                     # Gestión de Base de Datos
│   ├── __init__.py
│   ├── connection.py             # Conexión a BD
│   └── migrations.py             # Migraciones
├── utils/                        # Utilidades
│   ├── __init__.py
│   ├── validators.py             # Validaciones
│   └── helpers.py                # Funciones auxiliares
├── tests/                        # Pruebas
│   ├── __init__.py
│   └── test_models.py
├── script.sql                    # Script de base de datos
├── requirements.txt              # Dependencias
├── main.py                       # Punto de entrada
└── README.md                     # Documentación
```

## 🎯 REGLAS DE DESARROLLO

### 1. PATRÓN MVC
- **Modelo**: Representa los datos y la lógica de negocio
- **Vista**: Interfaz de usuario (Tkinter)
- **Controlador**: Maneja la lógica de aplicación y comunicación entre Modelo y Vista

### 2. CONVENCIONES DE NOMBRES
- **Archivos**: snake_case (ej: cliente_controller.py)
- **Clases**: PascalCase (ej: ClienteController)
- **Métodos y variables**: snake_case (ej: crear_cliente)
- **Constantes**: UPPER_SNAKE_CASE (ej: MAX_SALDO)

### 3. ESTRUCTURA DE MODELOS
```python
class ModeloBase:
    def __init__(self):
        self.id = None
        self.fecha_creacion = None
        self.fecha_modificacion = None
    
    def crear(self): pass
    def leer(self, id): pass
    def actualizar(self, id, datos): pass
    def eliminar(self, id): pass
    def listar(self): pass
```

### 4. ESTRUCTURA DE CONTROLADORES
```python
class ControladorBase:
    def __init__(self, modelo):
        self.modelo = modelo
    
    def crear(self, datos): pass
    def leer(self, id): pass
    def actualizar(self, id, datos): pass
    def eliminar(self, id): pass
    def listar(self): pass
```

### 5. VALIDACIONES OBLIGATORIAS
- **Campos requeridos**: No pueden estar vacíos
- **Formato de email**: Validación de formato
- **Números de documento**: Formato según tipo
- **Montos**: Solo números positivos
- **Fechas**: Formato válido y lógico

### 6. MANEJO DE ERRORES
- Usar try-catch en todas las operaciones de BD
- Mostrar mensajes de error amigables al usuario
- Log de errores para debugging
- Rollback automático en transacciones fallidas

### 7. SEGURIDAD
- Validación de entrada en todas las capas
- Uso de prepared statements (PyMySQL)
- No exponer información sensible en logs
- Validación de permisos por rol de usuario

## 📊 ENTIDADES PRINCIPALES

### 1. CLIENTES
- **Campos**: id, nombre, apellidos, documento, email, teléfono, fecha_nacimiento
- **Relaciones**: tipo_documento, categoria, agencia_apertura, direcciones
- **Operaciones**: CRUD completo

### 2. CUENTAS
- **Campos**: id, numero_cuenta, cci, cliente, producto, saldo, fecha_apertura, estado
- **Relaciones**: cliente, producto_cuenta
- **Operaciones**: CRUD, consulta de saldo, historial

### 3. TARJETAS
- **Campos**: id, numero_tarjeta, fecha_vencimiento, cuenta, linea_credito, tipo, estado
- **Relaciones**: cuenta, linea_credito, tipo_tarjeta
- **Operaciones**: CRUD, activar/desactivar

### 4. TRANSACCIONES
- **Campos**: id, cuenta_origen, cuenta_destino, monto, fecha, descripcion, tipo
- **Relaciones**: cuentas
- **Operaciones**: Crear, consultar historial

## 🔧 CONFIGURACIÓN

### Base de Datos
- **Host**: localhost
- **Puerto**: 3306
- **Usuario**: admin
- **Contraseña**: admin
- **Base de datos**: banco_peru_db

### Dependencias
```
pymysql==1.1.0
tkinter (incluido en Python)
configparser (incluido en Python)
```

## 🚀 FLUJO DE TRABAJO

1. **Inicialización**: Cargar configuración y conectar a BD
2. **Autenticación**: Login de usuario (opcional para demo)
3. **Menú Principal**: Selección de módulo (Clientes, Cuentas, Tarjetas)
4. **Operaciones CRUD**: Crear, Leer, Actualizar, Eliminar
5. **Validaciones**: En cada operación
6. **Persistencia**: Guardar en base de datos
7. **Feedback**: Mostrar resultado al usuario

## 📝 NOTAS IMPORTANTES

- Mantener separación clara entre capas
- Un controlador por entidad principal
- Una vista por entidad principal
- Reutilizar código común en clases base
- Documentar todos los métodos públicos
- Implementar logging para debugging
- Usar transacciones para operaciones complejas
