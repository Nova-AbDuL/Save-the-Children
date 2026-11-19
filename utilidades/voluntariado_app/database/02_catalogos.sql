-- =====================================================================
-- 02 - CATÁLOGOS y usuario administrador inicial (iguales para todo el grupo)
-- Ejecutar después de 01_tablas.sql
-- Los ids quedan así (base nueva): rol 1=ADMINISTRADOR, 2=VOLUNTARIO;
-- estado_voluntario 1=PENDIENTE, 2=APROBADO, 3=RECHAZADO;
-- estado_actividad 1=ACTIVA, 2=INACTIVA;
-- estado_postulacion 1=PENDIENTE, 2=APROBADA, 3=RECHAZADA;
-- metodo_pago 1=EFECTIVO, 2=TRANSFERENCIA, 3=QR.
-- =====================================================================
USE voluntariado_db;

INSERT IGNORE INTO rol (nombre) VALUES ('ADMINISTRADOR'), ('VOLUNTARIO');
INSERT IGNORE INTO estado_voluntario (nombre) VALUES ('PENDIENTE'), ('APROBADO'), ('RECHAZADO');
INSERT IGNORE INTO estado_actividad (nombre) VALUES ('ACTIVA'), ('INACTIVA');
INSERT IGNORE INTO estado_postulacion (nombre) VALUES ('PENDIENTE'), ('APROBADA'), ('RECHAZADA');
INSERT IGNORE INTO metodo_pago (nombre) VALUES ('EFECTIVO'), ('TRANSFERENCIA'), ('QR');

-- Administrador inicial (ficticio) para poder entrar al sistema por primera vez.
-- Contraseña en texto simple solo porque es un prototipo.
INSERT IGNORE INTO usuario (id_rol, usuario, contrasena, activo)
SELECT id_rol, 'admin', 'admin123', 1 FROM rol WHERE nombre = 'ADMINISTRADOR';
