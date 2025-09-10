-- Crear la base de datos 'banco_db'
CREATE DATABASE IF NOT EXISTS banco_db;

-- Seleccionar la base de datos para usarla
USE banco_db;

-- Crear la tabla de clientes (información personal)
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    telefono VARCHAR(20)
);

-- Crear la tabla de usuarios (credenciales de acceso)
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    id_cliente INT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Crear la tabla de cuentas
CREATE TABLE IF NOT EXISTS cuentas (
    numero_cuenta VARCHAR(50) PRIMARY KEY,
    id_cliente INT,
    tipo_cuenta VARCHAR(50) NOT NULL,
    saldo DECIMAL(10, 2) NOT NULL,
    fecha_apertura DATE NOT NULL,
    estado VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Crear la tabla de transacciones
CREATE TABLE IF NOT EXISTS transacciones (
    id_transaccion INT AUTO_INCREMENT PRIMARY KEY,
    numero_cuenta VARCHAR(50),
    tipo_transaccion VARCHAR(50) NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    fecha_transaccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    descripcion TEXT,
    FOREIGN KEY (numero_cuenta) REFERENCES cuentas(numero_cuenta)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

---

-- Insertar datos de ejemplo
-- El orden es crucial: clientes, luego usuarios, luego cuentas, y finalmente transacciones.

-- Insertar clientes
INSERT INTO clientes (nombre, apellido_paterno, apellido_materno, email, telefono) VALUES
('Juan', 'García', 'López', 'juan.garcia@email.com', '555-1234'),
('Ana', 'Martínez', 'Ruiz', 'ana.martinez@email.com', '555-5678'),
('Carlos', 'Sánchez', 'Pérez', 'carlos.sanchez@email.com', '555-9012');

-- Insertar usuarios
-- Las contraseñas aquí son 'pass123', 'pass456' y 'pass789', hasheadas con un algoritmo simple.
-- En un proyecto real, generarías estos hashes en Python.
INSERT INTO usuarios (username, password_hash, id_cliente) VALUES
('jgarcia', 'e5e7914f6b0f9f1b0a7018c1b504221a7199c9c8', 1),
('amartinez', 'a2884a44f9f7d499298539207e4d9c79e6027a05', 2),
('csanchez', '970d4432243d4f8286f773663b65126867083163', 3);

-- Insertar cuentas
INSERT INTO cuentas (numero_cuenta, id_cliente, tipo_cuenta, saldo, fecha_apertura, estado) VALUES
('CTA-1001', 1, 'Ahorros', 1500.50, '2024-01-15', 'Activa'),
('CTA-1002', 1, 'Corriente', 3200.00, '2024-02-20', 'Activa'),
('CTA-2001', 2, 'Ahorros', 850.75, '2024-03-10', 'Activa'),
('CTA-3001', 3, 'Corriente', 5000.00, '2024-04-05', 'Activa');

-- Insertar transacciones
INSERT INTO transacciones (numero_cuenta, tipo_transaccion, monto, descripcion) VALUES
('CTA-1001', 'Depósito', 500.00, 'Depósito inicial'),
('CTA-1001', 'Retiro', 200.00, 'Retiro en cajero'),
('CTA-1002', 'Depósito', 3200.00, 'Transferencia bancaria'),
('CTA-2001', 'Depósito', 850.75, 'Pago de nómina'),
('CTA-3001', 'Depósito', 5000.00, 'Transferencia de otra cuenta');