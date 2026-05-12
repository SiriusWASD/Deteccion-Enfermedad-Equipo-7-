-- Creación de la base de datos
CREATE DATABASE IF NOT EXISTS diabetes_expert_system;
USE diabetes_expert_system;

-- 1. Tabla de Usuarios (Para el sistema de Login)
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de Pacientes (Perfiles asociados a un usuario para manejar la bifurcación)
CREATE TABLE pacientes (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    nombre_paciente VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    es_menor BOOLEAN NOT NULL,
    imc DECIMAL(5,2), -- Índice de Masa Corporal, útil para inferencias de Tipo 2
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
);

-- 3. Tabla del Catálogo de Síntomas (Base de Conocimiento)
CREATE TABLE sintomas_catalogo (
    id_sintoma INT AUTO_INCREMENT PRIMARY KEY,
    nombre_sintoma VARCHAR(100) NOT NULL,
    descripcion TEXT,
    peso INT NOT NULL, -- Puntuación para el motor de inferencia (1 a 3)
    aplica_a ENUM('adulto', 'menor', 'ambos') NOT NULL
);

-- 4. Tabla de Historial de Diagnósticos (Resultados de las inferencias)
CREATE TABLE historial_diagnosticos (
    id_diagnostico INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    fecha_consulta DATETIME DEFAULT CURRENT_TIMESTAMP,
    puntuacion_total INT NOT NULL,
    nivel_riesgo ENUM('Bajo', 'Moderado', 'Alto') NOT NULL,
    tipo_diabetes_inferido VARCHAR(100), -- Ej. "Riesgo Tipo 2", "Posible Tipo 1 Infantil"
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) ON DELETE CASCADE
);

-- 5. Tabla Relacional: Detalle de Síntomas por Diagnóstico (Relación Muchos a Muchos)
CREATE TABLE detalle_diagnostico_sintomas (
    id_diagnostico INT NOT NULL,
    id_sintoma INT NOT NULL,
    PRIMARY KEY (id_diagnostico, id_sintoma),
    FOREIGN KEY (id_diagnostico) REFERENCES historial_diagnosticos(id_diagnostico) ON DELETE CASCADE,
    FOREIGN KEY (id_sintoma) REFERENCES sintomas_catalogo(id_sintoma) ON DELETE CASCADE
);

-- =========================================================
-- INSERCIÓN DE DATOS BASE (Catálogo inicial de síntomas)
-- =========================================================

INSERT INTO sintomas_catalogo (nombre_sintoma, descripcion, peso, aplica_a) VALUES
-- Síntomas Cardinales (Peso 3)
('Poliuria', 'Necesidad frecuente de orinar', 3, 'ambos'),
('Polidipsia', 'Sed excesiva e inusual', 3, 'ambos'),
('Pérdida de peso', 'Pérdida de peso rápida e inexplicable', 3, 'ambos'),
('Acantosis nigricans', 'Manchas oscuras en cuello o axilas', 3, 'menor'),
('Enuresis', 'Pérdida del control de esfínteres nocturno repentino', 3, 'menor'),

-- Síntomas Secundarios (Peso 2)
('Sobrepeso/Obesidad', 'IMC superior a los rangos saludables', 2, 'ambos'),
('Visión borrosa', 'Dificultad para enfocar o visión nublada', 2, 'adulto'),
('Antecedentes familiares', 'Padres o hermanos con diabetes', 2, 'ambos'),
('Cicatrización lenta', 'Heridas o rasguños que tardan en sanar', 2, 'adulto'),

-- Síntomas Leves/Generales (Peso 1)
('Fatiga', 'Cansancio extremo o falta de energía', 1, 'ambos'),
('Sedentarismo', 'Estilo de vida sin actividad física regular', 1, 'adulto');