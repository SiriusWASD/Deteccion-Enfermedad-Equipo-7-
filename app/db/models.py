# Archivo: app/db/models.py
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_completo = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    fecha_registro = Column(DateTime, default=datetime.datetime.utcnow)

    # Relación: Un usuario tiene muchos pacientes (perfiles)
    pacientes = relationship("Paciente", back_populates="usuario")

class Paciente(Base):
    __tablename__ = "pacientes"

    id_paciente = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), nullable=False)
    nombre_paciente = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    es_menor = Column(Boolean, nullable=False)
    imc = Column(Float, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)

    # Relaciones
    usuario = relationship("Usuario", back_populates="pacientes")
    historial = relationship("HistorialDiagnostico", back_populates="paciente")

class SintomaCatalogo(Base):
    __tablename__ = "sintomas_catalogo"

    id_sintoma = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_sintoma = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    peso = Column(Integer, nullable=False)
    aplica_a = Column(Enum('adulto', 'menor', 'ambos', name='aplica_a_enum'), nullable=False)

    # Relación muchos a muchos
    diagnosticos = relationship("HistorialDiagnostico", secondary="detalle_diagnostico_sintomas", back_populates="sintomas")

class HistorialDiagnostico(Base):
    __tablename__ = "historial_diagnosticos"

    id_diagnostico = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id_paciente", ondelete="CASCADE"), nullable=False)
    fecha_consulta = Column(DateTime, default=datetime.datetime.utcnow)
    puntuacion_total = Column(Integer, nullable=False)
    nivel_riesgo = Column(Enum('Bajo', 'Moderado', 'Alto', name='nivel_riesgo_enum'), nullable=False)
    tipo_diabetes_inferido = Column(String(100))

    # Relaciones
    paciente = relationship("Paciente", back_populates="historial")
    sintomas = relationship("SintomaCatalogo", secondary="detalle_diagnostico_sintomas", back_populates="diagnosticos")

class DetalleDiagnosticoSintomas(Base):
    __tablename__ = "detalle_diagnostico_sintomas"
    
    id_diagnostico = Column(Integer, ForeignKey("historial_diagnosticos.id_diagnostico", ondelete="CASCADE"), primary_key=True)
    id_sintoma = Column(Integer, ForeignKey("sintomas_catalogo.id_sintoma", ondelete="CASCADE"), primary_key=True)