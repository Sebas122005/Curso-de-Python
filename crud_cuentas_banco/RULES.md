# REGLAS DEL PROYECTO - CRUD CUENTAS BANCARIAS

## 🎯 OBJETIVO
Sistema CRUD para gestión de cuentas bancarias usando Python, Tkinter y MySQL con patrón MVC.

## 📁 ESTRUCTURA OBLIGATORIA
```
crud_cuentas_banco/
├── config/
│   └── config.ini
├── models/           # Capa de Modelo
├── controllers/      # Capa de Controlador  
├── views/           # Capa de Vista
├── database/        # Gestión de BD
├── utils/           # Utilidades
├── tests/           # Pruebas
└── main.py          # Punto de entrada
```

## 🔧 REGLAS DE DESARROLLO

### 1. PATRÓN MVC ESTRICTO
- **Modelo**: Solo lógica de datos y validaciones
- **Vista**: Solo interfaz de usuario (Tkinter)
- **Controlador**: Solo lógica de negocio y coordinación
- **NO MIXTAR**: Cada capa tiene su responsabilidad específica

### 2. CONVENCIONES DE NOMBRES
- **Archivos**: `snake_case.py` (ej: `cliente_controller.py`)
- **Clases**: `PascalCase` (ej: `ClienteController`)
- **Métodos**: `snake_case()` (ej: `crear_cliente()`)
- **Variables**: `snake_case` (ej: `numero_documento`)

### 3. ESTRUCTURA DE MODELOS
```python
class ModeloBase:
    def __init__(self):
        self.id = None
        self.fecha_creacion = None
    
    def crear(self, datos): pass
    def leer(self, id): pass
    def actualizar(self, id, datos): pass
    def eliminar(self, id): pass
    def listar(self): pass
    def validar_datos(self, datos): pass
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

### 5. ESTRUCTURA DE VISTAS
```python
class VistaBase:
    def __init__(self, parent, controlador):
        self.parent = parent
        self.controlador = controlador
        self.crear_interfaz()
    
    def crear_interfaz(self): pass
    def limpiar_formulario(self): pass
    def mostrar_error(self, mensaje): pass
    def mostrar_exito(self, mensaje): pass
```

## 📊 ENTIDADES PRINCIPALES

### CLIENTES (Prioridad 1)
- **Campos**: id, nombre, apellidos, documento, email, teléfono, fecha_nacimiento
- **Validaciones**: Email válido, documento único, campos requeridos
- **Operaciones**: CRUD completo

### CUENTAS (Prioridad 2)  
- **Campos**: id, numero_cuenta, cci, cliente, producto, saldo, estado
- **Validaciones**: Número único, saldo >= 0, cliente válido
- **Operaciones**: CRUD, consulta saldo, historial

### TARJETAS (Prioridad 3)
- **Campos**: id, numero_tarjeta, fecha_vencimiento, cuenta, tipo, estado
- **Validaciones**: Número único, fecha futura, cuenta válida
- **Operaciones**: CRUD, activar/desactivar

## ⚠️ REGLAS OBLIGATORIAS

### VALIDACIONES
- **SIEMPRE** validar en Modelo, Controlador Y Vista
- **NO** confiar solo en validaciones de interfaz
- **SIEMPRE** mostrar errores claros al usuario

### MANEJO DE ERRORES
- **SIEMPRE** usar try-catch en operaciones de BD
- **SIEMPRE** hacer rollback en transacciones fallidas
- **NUNCA** mostrar errores técnicos al usuario final

### BASE DE DATOS
- **SIEMPRE** usar prepared statements (PyMySQL)
- **SIEMPRE** cerrar conexiones después de usar
- **NUNCA** concatenar strings en consultas SQL

### INTERFAZ
- **SIEMPRE** limpiar formularios después de operaciones
- **SIEMPRE** confirmar antes de eliminar
- **SIEMPRE** mostrar feedback de operaciones exitosas

## 🚫 PROHIBICIONES

### NO HACER
- ❌ Mezclar lógica de capas
- ❌ Acceso directo a BD desde Vista
- ❌ Validaciones solo en interfaz
- ❌ Código sin comentarios
- ❌ Variables con nombres genéricos (a, b, x)
- ❌ Métodos de más de 50 líneas
- ❌ Clases sin responsabilidad clara

### NO PERMITIDO
- ❌ Hardcodear credenciales de BD
- ❌ Exponer información sensible en logs
- ❌ Dejar conexiones de BD abiertas
- ❌ Operaciones sin validación
- ❌ Código duplicado sin justificación

## ✅ CHECKLIST DE DESARROLLO

### ANTES DE CODIFICAR
- [ ] ¿Entiendo la responsabilidad de esta capa?
- [ ] ¿Tengo claro el flujo de datos?
- [ ] ¿He definido las validaciones necesarias?

### DURANTE EL DESARROLLO
- [ ] ¿Sigo las convenciones de nombres?
- [ ] ¿Estoy validando en todas las capas?
- [ ] ¿Manejo todos los errores posibles?
- [ ] ¿Comento el código complejo?

### DESPUÉS DE CODIFICAR
- [ ] ¿Funciona sin errores?
- [ ] ¿Pasa todas las validaciones?
- [ ] ¿La interfaz es intuitiva?
- [ ] ¿El código es legible?

## 🎯 CRITERIOS DE ÉXITO

### FUNCIONALIDAD
- [ ] CRUD completo para Clientes
- [ ] CRUD completo para Cuentas  
- [ ] CRUD completo para Tarjetas
- [ ] Validaciones funcionan correctamente
- [ ] Datos se persisten en BD

### CÓDIGO
- [ ] Patrón MVC bien implementado
- [ ] Código limpio y comentado
- [ ] Sin errores de sintaxis
- [ ] Manejo correcto de errores
- [ ] Estructura de proyecto clara

### INTERFAZ
- [ ] Fácil de usar
- [ ] Feedback claro al usuario
- [ ] Formularios intuitivos
- [ ] Navegación lógica
- [ ] Sin errores visuales

## 📝 NOTAS IMPORTANTES

- **Empezar simple**: CRUD básico primero, funcionalidades avanzadas después
- **Probar cada paso**: Verificar funcionamiento antes de continuar
- **Documentar decisiones**: Comentar por qué se hace algo, no solo qué se hace
- **Mantener consistencia**: Mismo estilo en todo el proyecto
- **Pensar en el usuario**: Interfaz clara y operaciones intuitivas
