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
VALUES ('Administrador Equipo 7', 'admin@diabetes.com', 'admin123');UPDATE sintomas_catalogo SET descripcion = 'Necesidad de orinar con más frecuencia de lo normal, especialmente por la noche.' WHERE nombre_sintoma LIKE 'Poliuria%';
UPDATE sintomas_catalogo SET descripcion = 'Sensación de sed anormalmente intensa que no se calma al beber líquidos.' WHERE nombre_sintoma LIKE 'Polidipsia%';
UPDATE sintomas_catalogo SET descripcion = 'Aumento desmedido del apetito, incluso después de haber comido.' WHERE nombre_sintoma LIKE 'Polifagia%';
UPDATE sintomas_catalogo SET descripcion = 'Disminución del peso corporal sin haber realizado dieta o aumento de ejercicio.' WHERE nombre_sintoma LIKE 'Pérdida de peso%';
UPDATE sintomas_catalogo SET descripcion = 'Sensación de cansancio extremo, falta de energía o debilidad continua.' WHERE nombre_sintoma LIKE 'Fatiga%';
UPDATE sintomas_catalogo SET descripcion = 'Dificultad para enfocar o ver detalles finos, visión nublada temporal.' WHERE nombre_sintoma LIKE 'Visión%';
UPDATE sintomas_catalogo SET descripcion = 'Cortes, rasguños o llagas que tardan semanas en sanar o se infectan fácilmente.' WHERE nombre_sintoma LIKE 'Cicatrización%';
UPDATE sintomas_catalogo SET descripcion = 'Sensación de entumecimiento, pinchazos o ardor en las extremidades.' WHERE nombre_sintoma LIKE 'Hormigueo%';
UPDATE sintomas_catalogo SET descripcion = 'Alteraciones repentinas en el estado de ánimo, llanto inusual o irritación constante.' WHERE nombre_sintoma LIKE 'Irritabilidad%';
UPDATE sintomas_catalogo SET descripcion = 'Aparición recurrente de infecciones en la piel, encías o tracto urinario.' WHERE nombre_sintoma LIKE 'Infecciones%';
UPDATE sintomas_catalogo SET descripcion = 'Pérdida involuntaria de orina durante el sueño en niños que ya controlaban esfínteres.' WHERE nombre_sintoma LIKE 'Enuresis%';