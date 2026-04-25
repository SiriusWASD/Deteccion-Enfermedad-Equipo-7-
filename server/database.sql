-- SCRIPT DE EXPORTACIÓN: BASE DE DATOS SISTEMA EXPERTO
-- Este archivo recrea la estructura y los datos iniciales

-- 1. Borrar tablas si existen (para evitar errores al importar)
DROP TABLE IF EXISTS registros_evaluacion;
DROP TABLE IF EXISTS sintomas;
DROP TABLE IF EXISTS enfermedades;

-- 2. Crear tabla de enfermedades (Investigación de las 5 causas en México)
CREATE TABLE enfermedades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- 3. Crear tabla de síntomas (Base de conocimiento para el sistema experto)
CREATE TABLE sintomas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- 4. Crear tabla de registros (Historial de consultas)
CREATE TABLE registros_evaluacion (
    id SERIAL PRIMARY KEY,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    enfermedad_detectada VARCHAR(100),
    sintomas_reportados TEXT,
    recomendacion TEXT
);

-- 5. Insertar datos de investigación (Diabetes Mellitus es la seleccionada)
INSERT INTO enfermedades (nombre, descripcion) VALUES 
('Enfermedades del Corazón', 'Primera causa de muerte en México.'),
('Diabetes Mellitus', 'Segunda causa de muerte en México. Seleccionada para este sistema.'),
('Tumores Malignos', 'Tercera causa de muerte en México.'),
('Enfermedades del Hígado', 'Cuarta causa de muerte en México.'),
('Enfermedades Cerebrovasculares', 'Quinta causa de muerte en México.');

-- 6. Insertar síntomas clave para la lógica del programa
INSERT INTO sintomas (nombre) VALUES 
('Sed excesiva'), 
('Mucha hambre'), 
('Orina frecuente'), 
('Visión borrosa'), 
('Cansancio persistente');