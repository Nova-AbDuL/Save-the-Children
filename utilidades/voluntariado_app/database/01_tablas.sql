-- =====================================================================
-- 01 - TABLAS del sistema de voluntariado y donaciones (diseño común)
-- Save the Children Bolivia - escenario de diseño. Datos ficticios.
-- Si necesita reconstruir todo desde cero, ejecute antes:
--     DROP DATABASE voluntariado_db;
-- Los campos pueden editarse y complementarse; avise al grupo y actualice este archivo.
-- =====================================================================
CREATE DATABASE IF NOT EXISTS voluntariado_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE voluntariado_db;

-- ---------------------------------------------------------------------
-- Catálogos
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS rol (
  id_rol INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(30) NOT NULL,
  PRIMARY KEY (id_rol),
  UNIQUE KEY uq_rol_nombre (nombre)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS estado_voluntario (
  id_estado_vol INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(30) NOT NULL,
  PRIMARY KEY (id_estado_vol),
  UNIQUE KEY uq_estado_vol_nombre (nombre)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS estado_actividad (
  id_estado_act INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(30) NOT NULL,
  PRIMARY KEY (id_estado_act),
  UNIQUE KEY uq_estado_act_nombre (nombre)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS estado_postulacion (
  id_estado_pos INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(30) NOT NULL,
  PRIMARY KEY (id_estado_pos),
  UNIQUE KEY uq_estado_pos_nombre (nombre)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS metodo_pago (
  id_metodo_pago INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(30) NOT NULL,
  PRIMARY KEY (id_metodo_pago),
  UNIQUE KEY uq_metodo_pago_nombre (nombre)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Usuarios y voluntarios
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuario (
  id_usuario INT NOT NULL AUTO_INCREMENT,
  id_rol INT NOT NULL,
  usuario VARCHAR(40) NOT NULL,
  contrasena VARCHAR(100) NOT NULL,          -- texto simple solo para el prototipo
  activo TINYINT(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (id_usuario),
  UNIQUE KEY uq_usuario_usuario (usuario),
  CONSTRAINT fk_usuario_rol FOREIGN KEY (id_rol) REFERENCES rol (id_rol)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS voluntario (
  id_voluntario INT NOT NULL AUTO_INCREMENT,
  id_usuario INT NOT NULL,
  id_estado_vol INT NOT NULL,
  id_admin_aprueba INT NULL,                 -- se llena cuando el administrador decide
  nombres VARCHAR(60) NOT NULL,
  apellidos VARCHAR(60) NOT NULL,
  cedula VARCHAR(20) NOT NULL,               -- cédula FICTICIA
  correo VARCHAR(80) NULL,
  telefono VARCHAR(15) NULL,
  fecha_registro DATE NOT NULL,
  PRIMARY KEY (id_voluntario),
  UNIQUE KEY uq_voluntario_usuario (id_usuario),
  UNIQUE KEY uq_voluntario_cedula (cedula),
  CONSTRAINT fk_voluntario_usuario FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_voluntario_estado FOREIGN KEY (id_estado_vol) REFERENCES estado_voluntario (id_estado_vol)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_voluntario_admin FOREIGN KEY (id_admin_aprueba) REFERENCES usuario (id_usuario)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Actividades, postulaciones y asistencia
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS actividad (
  id_actividad INT NOT NULL AUTO_INCREMENT,
  id_estado_act INT NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  descripcion VARCHAR(255) NULL,
  fecha DATE NOT NULL,
  hora_inicio TIME NULL,
  hora_fin TIME NULL,
  lugar VARCHAR(100) NOT NULL,
  cupo INT NOT NULL DEFAULT 10,
  PRIMARY KEY (id_actividad),
  CONSTRAINT fk_actividad_estado FOREIGN KEY (id_estado_act) REFERENCES estado_actividad (id_estado_act)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS postulacion (
  id_postulacion INT NOT NULL AUTO_INCREMENT,
  id_voluntario INT NOT NULL,
  id_actividad INT NOT NULL,
  id_estado_pos INT NOT NULL,
  id_admin_resuelve INT NULL,                -- se llena cuando el administrador decide
  fecha_postulacion DATE NOT NULL,
  PRIMARY KEY (id_postulacion),
  UNIQUE KEY uq_postulacion_vol_act (id_voluntario, id_actividad),
  CONSTRAINT fk_postulacion_voluntario FOREIGN KEY (id_voluntario) REFERENCES voluntario (id_voluntario)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_postulacion_actividad FOREIGN KEY (id_actividad) REFERENCES actividad (id_actividad)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_postulacion_estado FOREIGN KEY (id_estado_pos) REFERENCES estado_postulacion (id_estado_pos)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_postulacion_admin FOREIGN KEY (id_admin_resuelve) REFERENCES usuario (id_usuario)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS asistencia (
  id_asistencia INT NOT NULL AUTO_INCREMENT,
  id_postulacion INT NOT NULL,
  asistio TINYINT(1) NOT NULL DEFAULT 0,
  horas DECIMAL(4,1) NOT NULL DEFAULT 0,
  PRIMARY KEY (id_asistencia),
  UNIQUE KEY uq_asistencia_postulacion (id_postulacion),
  CONSTRAINT fk_asistencia_postulacion FOREIGN KEY (id_postulacion) REFERENCES postulacion (id_postulacion)
    ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Donaciones (datos ficticios, sin pagos reales), ligadas a una actividad
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS donante (
  id_donante INT NOT NULL AUTO_INCREMENT,
  nombres VARCHAR(60) NOT NULL,
  correo VARCHAR(80) NULL,
  telefono VARCHAR(15) NULL,
  PRIMARY KEY (id_donante)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS donacion (
  id_donacion INT NOT NULL AUTO_INCREMENT,
  id_donante INT NOT NULL,
  id_actividad INT NULL,                     -- actividad a la que se destina; vacío si es una donación general
  id_metodo_pago INT NULL,                   -- vacío si la donación es de material
  tipo ENUM('DINERO','MATERIAL') NOT NULL,
  monto DECIMAL(10,2) NULL,                  -- vacío si la donación es de material
  fecha DATE NOT NULL,
  observacion VARCHAR(150) NULL,             -- aquí se describe el material
  PRIMARY KEY (id_donacion),
  CONSTRAINT fk_donacion_donante FOREIGN KEY (id_donante) REFERENCES donante (id_donante)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_donacion_actividad FOREIGN KEY (id_actividad) REFERENCES actividad (id_actividad)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_donacion_metodo FOREIGN KEY (id_metodo_pago) REFERENCES metodo_pago (id_metodo_pago)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;
