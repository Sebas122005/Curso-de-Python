-- Crear la base de datos 'banco_peru_db'
CREATE DATABASE IF NOT EXISTS banco_peru_db;
USE banco_peru_db;

-- Tablas de Normalización y Catálogos
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS tipo_documento_legal (
    id_tipo_documento INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS departamentos (
    id_departamento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS provincias (
    id_provincia INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    id_departamento INT,
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento)
);

CREATE TABLE IF NOT EXISTS distritos (
    id_distrito INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    id_provincia INT,
    FOREIGN KEY (id_provincia) REFERENCES provincias(id_provincia)
);

CREATE TABLE IF NOT EXISTS categoria_cliente (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_categoria VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS bancos (
    id_banco INT AUTO_INCREMENT PRIMARY KEY,
    nombre_banco VARCHAR(100) UNIQUE NOT NULL,
    codigo_banco VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS agencias (
    id_agencia INT AUTO_INCREMENT PRIMARY KEY,
    nombre_agencia VARCHAR(100) NOT NULL,
    id_distrito INT,
    direccion VARCHAR(255),
    FOREIGN KEY (id_distrito) REFERENCES distritos(id_distrito)
);

CREATE TABLE IF NOT EXISTS roles (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre_rol VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS productos_cuenta (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre_producto VARCHAR(100) UNIQUE NOT NULL,
    tipo_producto VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS tipo_tarjeta (
    id_tipo_tarjeta INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tipo VARCHAR(50) UNIQUE NOT NULL
);

-- Tablas Principales
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    id_tipo_documento INT,
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    fecha_nacimiento DATE,
    id_categoria INT,
    id_agencia_apertura INT,
    FOREIGN KEY (id_tipo_documento) REFERENCES tipo_documento_legal(id_tipo_documento),
    FOREIGN KEY (id_categoria) REFERENCES categoria_cliente(id_categoria),
    FOREIGN KEY (id_agencia_apertura) REFERENCES agencias(id_agencia)
);

CREATE TABLE IF NOT EXISTS direcciones (
    id_direccion INT AUTO_INCREMENT PRIMARY KEY,
    calle VARCHAR(100) NOT NULL,
    numero VARCHAR(10),
    id_distrito INT,
    id_cliente INT,
    FOREIGN KEY (id_distrito) REFERENCES distritos(id_distrito),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    id_cliente INT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

CREATE TABLE IF NOT EXISTS usuario_rol (
    id_usuario INT,
    id_rol INT,
    PRIMARY KEY (id_usuario, id_rol),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

CREATE TABLE IF NOT EXISTS lineas_credito (
    id_linea INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    limite_credito DECIMAL(18, 2) NOT NULL,
    saldo_pendiente DECIMAL(18, 2) NOT NULL,
    tasa_interes DECIMAL(5, 2) NOT NULL,
    fecha_apertura DATE NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- Tablas Transaccionales
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS cuentas (
    id_cuenta INT AUTO_INCREMENT PRIMARY KEY,
    numero_cuenta VARCHAR(50) UNIQUE NOT NULL,
    cci VARCHAR(25) UNIQUE NOT NULL,
    id_cliente INT,
    id_producto INT,
    saldo DECIMAL(18, 2) NOT NULL,
    fecha_apertura DATE NOT NULL,
    estado VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_producto) REFERENCES productos_cuenta(id_producto)
);

CREATE TABLE IF NOT EXISTS tarjetas (
    id_tarjeta INT AUTO_INCREMENT PRIMARY KEY,
    numero_tarjeta VARCHAR(16) UNIQUE NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    id_cuenta INT,
    id_linea INT,
    id_tipo_tarjeta INT,
    estado VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_cuenta) REFERENCES cuentas(id_cuenta),
    FOREIGN KEY (id_linea) REFERENCES lineas_credito(id_linea),
    FOREIGN KEY (id_tipo_tarjeta) REFERENCES tipo_tarjeta(id_tipo_tarjeta)
);

CREATE TABLE IF NOT EXISTS transacciones_cuenta (
    id_transaccion INT AUTO_INCREMENT PRIMARY KEY,
    id_cuenta_origen INT,
    id_cuenta_destino INT,
    monto DECIMAL(18, 2) NOT NULL,
    fecha_transaccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT,
    tipo_movimiento VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_cuenta_origen) REFERENCES cuentas(id_cuenta),
    FOREIGN KEY (id_cuenta_destino) REFERENCES cuentas(id_cuenta)
);

CREATE TABLE IF NOT EXISTS transacciones_tarjeta (
    id_transaccion INT AUTO_INCREMENT PRIMARY KEY,
    id_tarjeta INT,
    monto DECIMAL(18, 2) NOT NULL,
    fecha_transaccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT,
    tipo_movimiento VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_tarjeta) REFERENCES tarjetas(id_tarjeta)
);

CREATE TABLE IF NOT EXISTS historial_saldos (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_cuenta INT,
    saldo_anterior DECIMAL(18, 2),
    saldo_nuevo DECIMAL(18, 2),
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_cuenta) REFERENCES cuentas(id_cuenta)
);
-- Datos de Ubicación (Perú)
INSERT INTO departamentos (nombre) VALUES 
('Lima'), 
('Arequipa'), 
('Cusco');

INSERT INTO provincias (nombre, id_departamento) VALUES 
('Lima', 1), 
('Callao', 1), 
('Arequipa', 2),
('Cusco', 3);

INSERT INTO distritos (nombre, id_provincia) VALUES 
('Miraflores', 1), 
('San Isidro', 1), 
('Cercado de Lima', 1), 
('Arequipa', 3),
('Cercado del Cusco', 4),
('Chorrillos', 1);

-- Catálogos
INSERT INTO tipo_documento_legal (nombre_tipo) VALUES 
('DNI'), 
('Carné de Extranjería'), 
('Pasaporte');

INSERT INTO categoria_cliente (nombre_categoria) VALUES 
('Estándar'), 
('Premium'),
('Empresarial');

INSERT INTO bancos (nombre_banco, codigo_banco) VALUES 
('BCP', '002'), 
('Interbank', '003'), 
('BBVA', '011');

INSERT INTO agencias (nombre_agencia, id_distrito, direccion) VALUES 
('Agencia Miraflores', 1, 'Av. Larco 101'), 
('Agencia San Isidro', 2, 'Av. Canaval y Moreyra 202'),
('Agencia Cercado de Lima', 3, 'Jirón de la Unión 500');

INSERT INTO productos_cuenta (nombre_producto, tipo_producto) VALUES 
('Cuenta de Ahorros Clásica', 'Ahorros'), 
('Cuenta Sueldo', 'Ahorros'), 
('Cuenta Corriente Empresarial', 'Corriente'),
('Ahorro Programado', 'Ahorros');

INSERT INTO tipo_tarjeta (nombre_tipo) VALUES 
('Débito'), 
('Crédito');

INSERT INTO roles (nombre_rol) VALUES 
('Cliente'), 
('Administrador'), 
('Cajero');
-- Clientes
INSERT INTO clientes (nombre, apellido_paterno, apellido_materno, id_tipo_documento, numero_documento, email, telefono, fecha_nacimiento, id_categoria, id_agencia_apertura) VALUES
('Pedro', 'Alvarez', 'Mendoza', 1, '47896541', 'pedro.alvarez@email.com', '987654321', '1990-03-15', 1, 1),
('Laura', 'Vargas', 'Quispe', 1, '87654321', 'laura.vargas@email.com', '998877665', '1985-08-22', 2, 2),
('Carlos', 'Suárez', 'Gómez', 1, '76543210', 'carlos.suarez@email.com', '965432109', '1975-10-01', 3, 2),
('Ana', 'Díaz', 'Rojas', 2, 'A12345678', 'ana.diaz@email.com', '945678901', '1995-04-18', 1, 3);

-- Direcciones
INSERT INTO direcciones (calle, numero, id_distrito, id_cliente) VALUES
('Calle Cantuarias', '125', 1, 1),
('Av. Pardo', '330', 2, 2),
('Av. Larco', '500', 3, 3),
('Calle El Bosque', '855', 4, 4);

-- Usuarios
INSERT INTO usuarios (username, password_hash, id_cliente) VALUES
('palvarez', 'e5e7914f6b0f9f1b0a7018c1b504221a7199c9c8', 1),
('lvargas', 'a2884a44f9f7d499298539207e4d9c79e6027a05', 2),
('csuarez', '970d4432243d4f8286f773663b65126867083163', 3),
('adiaz', '7a1a23e5907406606a09074f4b9f2d1e2b5e2a22', 4),
('admin', 'b3260c67e7100b777a49681b953a3e6a64b9f7a7', NULL);

-- Roles de usuario
INSERT INTO usuario_rol (id_usuario, id_rol) VALUES
(1, 1), -- Pedro es un Cliente
(2, 1), -- Laura es un Cliente
(3, 1), -- Carlos es un Cliente
(4, 1), -- Ana es una Cliente
(5, 2); -- El usuario 'admin' es un Administrador
-- Cuentas
INSERT INTO cuentas (numero_cuenta, cci, id_cliente, id_producto, saldo, fecha_apertura, estado) VALUES
('003-100-001001-44', '003-100-001001-44', 1, 1, 500.50, '2023-01-20', 'Activa'),
('003-100-001002-55', '003-100-001002-55', 2, 2, 12000.75, '2023-03-10', 'Activa'),
('003-100-001003-66', '003-100-001003-66', 3, 3, 50000.00, '2023-04-01', 'Activa'),
('003-100-001004-77', '003-100-001004-77', 4, 1, 850.20, '2023-05-18', 'Activa');

-- Líneas de Crédito
INSERT INTO lineas_credito (id_cliente, limite_credito, saldo_pendiente, tasa_interes, fecha_apertura) VALUES
(1, 10000.00, 250.00, 4.5, '2023-05-15');

-- Tarjetas
INSERT INTO tarjetas (numero_tarjeta, fecha_vencimiento, id_cuenta, id_linea, id_tipo_tarjeta, estado) VALUES
('4567-8901-2345-6789', '2027-12-31', 1, NULL, 1, 'Activa'), -- Tarjeta de débito para Pedro
('1234-5678-9012-3456', '2028-09-30', NULL, 1, 2, 'Activa'), -- Tarjeta de crédito para Pedro
('9876-5432-1098-7654', '2027-08-31', 2, NULL, 1, 'Activa'), -- Tarjeta de débito para Laura
('7777-7777-7777-7777', '2030-01-31', 3, NULL, 1, 'Inactiva'); -- Tarjeta de débito para Carlos
-- Transacciones de Cuenta
INSERT INTO transacciones_cuenta (id_cuenta_origen, id_cuenta_destino, monto, fecha_transaccion, descripcion, tipo_movimiento) VALUES
(1, 2, 250.00, NOW(), 'Transferencia a Laura por deuda', 'Cargo'),
(2, 1, 250.00, NOW(), 'Abono de Pedro por transferencia', 'Abono'),
(4, NULL, 150.00, NOW(), 'Depósito de efectivo', 'Abono');

-- Transacciones de Tarjeta
INSERT INTO transacciones_tarjeta (id_tarjeta, monto, fecha_transaccion, descripcion, tipo_movimiento) VALUES
(1, 50.00, NOW(), 'Compra en supermercado', 'Compra'), -- Compra con débito
(2, 100.00, NOW(), 'Compra en linea de ropa', 'Compra'), -- Compra con crédito
(2, 150.00, NOW(), 'Retiro en cajero', 'Retiro'), -- Retiro con crédito
(3, 200.00, NOW(), 'Compra en restaurante', 'Compra'); -- Compra con débito

-- Historial de Saldos
INSERT INTO historial_saldos (id_cuenta, saldo_anterior, saldo_nuevo, fecha_cambio) VALUES
(1, 500.50, 250.50, NOW()),
(2, 12000.75, 12250.75, NOW()),
(4, 850.20, 1000.20, NOW());

