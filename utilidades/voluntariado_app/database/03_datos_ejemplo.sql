-- =====================================================================
-- 03 - DATOS DE EJEMPLO (FICTICIOS). Cada integrante puede usar los suyos.
-- Ejecutar después de 01 y 02, sobre una base nueva (usa ids 1, 2, 3...).
-- =====================================================================
USE voluntariado_db;

INSERT INTO usuario (id_rol, usuario, contrasena, activo) VALUES
(2, 'ana.rojas',    'ana123',   1),   -- id_usuario 2
(2, 'luis.mamani',  'luis123',  1),   -- id_usuario 3
(2, 'carla.flores', 'carla123', 1);   -- id_usuario 4

INSERT INTO voluntario (id_usuario, id_estado_vol, id_admin_aprueba, nombres, apellidos, cedula, correo, telefono, fecha_registro) VALUES
(2, 2, 1,    'Ana',   'Rojas',  '1000001', 'ana@example.com',   '70000001', '2026-10-01'),
(3, 2, 1,    'Luis',  'Mamani', '1000002', 'luis@example.com',  '70000002', '2026-10-02'),
(4, 1, NULL, 'Carla', 'Flores', '1000003', 'carla@example.com', '70000003', '2026-10-05');

INSERT INTO actividad (id_estado_act, nombre, descripcion, fecha, hora_inicio, hora_fin, lugar, cupo) VALUES
(1, 'Taller de lectura',        'Actividad de apoyo a la lectura (ejemplo)', '2026-11-20', '09:00', '12:00', 'Aula comunitaria', 10),
(1, 'Jornada de reforzamiento', 'Reforzamiento escolar (ejemplo)',           '2026-11-27', '14:00', '17:00', 'Unidad educativa', 15);

INSERT INTO postulacion (id_voluntario, id_actividad, id_estado_pos, id_admin_resuelve, fecha_postulacion) VALUES
(1, 1, 2, 1,    '2026-11-05'),
(2, 1, 2, 1,    '2026-11-05'),
(1, 2, 1, NULL, '2026-11-08');

INSERT INTO asistencia (id_postulacion, asistio, horas) VALUES
(1, 1, 3.0),
(2, 1, 2.5);

INSERT INTO donante (nombres, correo, telefono) VALUES
('Marta Quispe', 'marta@example.com', '71000001'),
('Pedro Vega',   'pedro@example.com', '71000002');

INSERT INTO donacion (id_donante, id_actividad, id_metodo_pago, tipo, monto, fecha, observacion) VALUES
(1, 1,    1,    'DINERO',   100.00, '2026-11-10', 'Donación ficticia para el taller de lectura'),
(2, 2,    NULL, 'MATERIAL', NULL,   '2026-11-12', 'Útiles escolares (20 cuadernos)'),
(1, NULL, 3,    'DINERO',   50.00,  '2026-11-14', 'Donación general ficticia');
