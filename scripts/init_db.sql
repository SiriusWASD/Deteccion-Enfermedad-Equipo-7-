-- 1. Insertar el catálogo de síntomas y sus pesos médicos
INSERT INTO sintomas_catalogo (nombre_sintoma, aplica_a, peso) VALUES
('Poliuria (Orinar frecuentemente)', 'ambos', 3),
('Polidipsia (Sed excesiva)', 'ambos', 3),
('Polifagia (Hambre extrema)', 'ambos', 3),
('Pérdida de peso inexplicable', 'ambos', 3),
('Fatiga constante', 'ambos', 2),
('Visión borrosa', 'ambos', 2),
('Cicatrización lenta de heridas', 'ambos', 2),
('Hormigueo en manos/pies', 'adulto', 2),
('Irritabilidad (Cambios de humor)', 'menor', 1),
('Infecciones frecuentes', 'ambos', 1),
('Enuresis (Mojar la cama)', 'menor', 2);

-- 2. Insertar un usuario de prueba para poder hacer login
INSERT INTO usuarios (nombre_completo, correo, password_hash) 
VALUES ('Administrador Equipo 7', 'admin@diabetes.com', 'admin123');