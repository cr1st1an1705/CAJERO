CREATE DATABASE IF NOT EXISTS cajero_atm;
USE cajero_atm;

CREATE TABLE IF NOT EXISTS cuentas (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    numero_cuenta VARCHAR(20) NOT NULL UNIQUE,
    titular_nombre VARCHAR(150) NOT NULL,
    pin_hash VARCHAR(255) NOT NULL,
    saldo DECIMAL(18,2) NOT NULL DEFAULT 0,
    intentos_fallidos INT NOT NULL DEFAULT 0,
    bloqueada_hasta DATETIME NULL,
    activa BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS sesiones (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    cuenta_id BIGINT NOT NULL,
    token VARCHAR(500) NOT NULL UNIQUE,
    ultimo_movimiento DATETIME NOT NULL,
    activa BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_sesiones_cuenta FOREIGN KEY (cuenta_id) REFERENCES cuentas(id)
);

CREATE TABLE IF NOT EXISTS transacciones (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    cuenta_id BIGINT NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    monto DECIMAL(18,2) NOT NULL DEFAULT 0,
    saldo_anterior DECIMAL(18,2) NOT NULL DEFAULT 0,
    saldo_nuevo DECIMAL(18,2) NOT NULL DEFAULT 0,
    descripcion TEXT NULL,
    atm_origen VARCHAR(50) NOT NULL DEFAULT 'ATM-LOCAL',
    fecha DATETIME NOT NULL,
    CONSTRAINT fk_transacciones_cuenta FOREIGN KEY (cuenta_id) REFERENCES cuentas(id)
);

CREATE TABLE IF NOT EXISTS auditorias (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    cuenta_id BIGINT NULL,
    nivel VARCHAR(20) NOT NULL DEFAULT 'INFO',
    categoria VARCHAR(20) NOT NULL,
    accion VARCHAR(100) NOT NULL,
    detalle TEXT NULL,
    nodo_bd VARCHAR(30) NULL,
    ip_origen VARCHAR(50) NULL,
    fecha DATETIME NOT NULL,
    CONSTRAINT fk_auditorias_cuenta FOREIGN KEY (cuenta_id) REFERENCES cuentas(id)
);
