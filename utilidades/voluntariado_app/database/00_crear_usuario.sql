-- =====================================================================
-- 00 - Usuario de MySQL para la aplicación (ejecutar UNA vez, como root)
-- Cambie 'CAMBIAR_CLAVE' por su contraseña y use la misma en src/config.py
-- =====================================================================
CREATE USER IF NOT EXISTS 'app_voluntariado'@'localhost' IDENTIFIED BY 'CAMBIAR_CLAVE';
GRANT ALL PRIVILEGES ON voluntariado_db.* TO 'app_voluntariado'@'localhost';
FLUSH PRIVILEGES;
