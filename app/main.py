# Archivo: app/main.py
import os
from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy.orm import Session
from sqlalchemy import or_

# Importar base de datos, modelos y motor
from app.db.database import engine, Base, SessionLocal
from app.db.models import Usuario, SintomaCatalogo, Paciente, HistorialDiagnostico
from app.expert_system.inference_engine import MotorInferenciaDiabetes

# 1. Inicializar Base de Datos (¡Esto creará las tablas en PostgreSQL!)
Base.metadata.create_all(bind=engine)

# 2. Inicializar Flask
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave_secreta_equipo_7")

# ==========================================
# RUTAS DE AUTENTICACIÓN Y REGISTRO
# ==========================================

@app.route("/", methods=["GET"])
def pagina_login():
    """Muestra la pantalla de inicio de sesión."""
    if "usuario_id" in session:
        return redirect(url_for("panel_principal"))
    mensaje = request.args.get("mensaje")
    return render_template("login.html", mensaje=mensaje)

@app.route("/login", methods=["POST"])
def procesar_login():
    """Valida credenciales y crea la sesión."""
    db = SessionLocal()
    correo = request.form.get("correo")
    password = request.form.get("password")
    
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    
    if not usuario or usuario.password_hash != password:
        db.close()
        return render_template("login.html", mensaje="Credenciales inválidas. Intente de nuevo.")
    
    session["usuario_id"] = usuario.id_usuario
    session["nombre"] = usuario.nombre_completo
    db.close()
    return redirect(url_for("panel_principal"))

@app.route("/registro", methods=["GET"])
def pantalla_registro():
    """Muestra el formulario para crear una nueva cuenta."""
    return render_template("registro.html", mensaje=None)

@app.route("/procesar_registro", methods=["POST"])
def procesar_registro():
    """Crea un nuevo usuario en la base de datos."""
    db = SessionLocal()
    nombre = request.form.get("nombre")
    correo = request.form.get("correo")
    password = request.form.get("password")
    
    existe = db.query(Usuario).filter(Usuario.correo == correo).first()
    if existe:
        db.close()
        return render_template("registro.html", mensaje="El correo ya está registrado.")
    
    nuevo_usuario = Usuario(nombre_completo=nombre, correo=correo, password_hash=password)
    db.add(nuevo_usuario)
    db.commit()
    db.close()
    return redirect(url_for("pagina_login", mensaje="Cuenta creada exitosamente"))

@app.route("/logout", methods=["GET"])
def cerrar_sesion():
    """Limpia la sesión y redirige al login."""
    session.clear()
    return redirect(url_for("pagina_login"))

# ==========================================
# RUTAS DEL PANEL Y CONSULTAS
# ==========================================

@app.route("/dashboard", methods=["GET"])
def panel_principal():
    """Pantalla de bienvenida y selección de perfil."""
    if "usuario_id" not in session:
        return redirect(url_for("pagina_login"))
    
    nombre = session.get("nombre")
    return render_template("dashboard.html", nombre=nombre)

@app.route("/historial", methods=["GET"])
def ver_historial():
    """Muestra todas las consultas previas del usuario logueado."""
    if "usuario_id" not in session:
        return redirect(url_for("pagina_login"))
    
    db = SessionLocal()
    usuario_id = session.get("usuario_id")
    
    consultas = db.query(HistorialDiagnostico).join(Paciente).filter(
        Paciente.id_usuario == usuario_id
    ).order_by(HistorialDiagnostico.fecha_consulta.desc()).all()
    
    # ✅ CORRECCIÓN APLICADA: Renderizamos el HTML antes de cerrar la base de datos
    html_renderizado = render_template("historial.html", consultas=consultas)
    db.close()
    
    return html_renderizado

@app.route("/consulta/<tipo_paciente>", methods=["GET"])
def pantalla_consulta(tipo_paciente):
    """Formulario de síntomas filtrado por tipo de paciente."""
    if "usuario_id" not in session:
        return redirect(url_for("pagina_login"))

    db = SessionLocal()
    sintomas = db.query(SintomaCatalogo).filter(
        or_(SintomaCatalogo.aplica_a == tipo_paciente, SintomaCatalogo.aplica_a == 'ambos')
    ).all()
    
    # ✅ CORRECCIÓN APLICADA: Renderizamos el HTML antes de cerrar la base de datos
    html_renderizado = render_template("consulta.html", tipo=tipo_paciente, sintomas=sintomas)
    db.close()
    
    return html_renderizado

@app.route("/procesar_diagnostico", methods=["POST"])
def procesar_diagnostico():
    """Ejecuta la inferencia, guarda en DB y muestra resultados."""
    if "usuario_id" not in session:
        return redirect(url_for("pagina_login"))

    db = SessionLocal()
    usuario_id = session.get("usuario_id")
    
    es_menor_str = request.form.get("es_menor")
    es_menor_bool = True if es_menor_str and es_menor_str.lower() == 'true' else False
    
    nombre_paciente = request.form.get("nombre_paciente")
    edad = int(request.form.get("edad", 0))
    peso = float(request.form.get("peso", 0))
    estatura = float(request.form.get("estatura", 0))
    
    # Obtener lista de IDs de síntomas desde los checkboxes
    sintomas_ids_str = request.form.getlist("sintomas_ids")
    sintomas_ids = [int(sid) for sid in sintomas_ids_str]

    # 1. Cálculos de salud
    imc = peso / (estatura ** 2) if estatura > 0 else 0

    # 2. Registrar Paciente
    nuevo_paciente = Paciente(
        id_usuario=usuario_id, nombre_paciente=nombre_paciente,
        edad=edad, es_menor=es_menor_bool, imc=round(imc, 2)
    )
    db.add(nuevo_paciente)
    db.commit()
    db.refresh(nuevo_paciente)

    # 3. Consultar Pesos de Síntomas
    sintomas_db = db.query(SintomaCatalogo).filter(SintomaCatalogo.id_sintoma.in_(sintomas_ids)).all()
    lista_sintomas_motor = [{"nombre": s.nombre_sintoma, "peso": s.peso} for s in sintomas_db]

    # 4. Inferencia
    motor = MotorInferenciaDiabetes()
    resultado = motor.evaluar_paciente(edad, es_menor_bool, lista_sintomas_motor)

    # 5. Guardar Diagnóstico
    nuevo_diagnostico = HistorialDiagnostico(
        id_paciente=nuevo_paciente.id_paciente,
        puntuacion_total=resultado["puntuacion_total"],
        nivel_riesgo=resultado["nivel_riesgo"],
        tipo_diabetes_inferido=resultado["tipo_diabetes_inferido"]
    )
    nuevo_diagnostico.sintomas.extend(sintomas_db)
    db.add(nuevo_diagnostico)
    db.commit()

    # 6. Respuesta Visual (Renderizamos ANTES de cerrar la base de datos)
    html_renderizado = render_template("resultado.html", 
                                       paciente=nuevo_paciente, 
                                       resultado=resultado, 
                                       sintomas=sintomas_db)
    
    db.close()  # ✅ AHORA SÍ CERRAMOS LA CONEXIÓN
    return html_renderizado

if __name__ == "__main__":
    app.run(debug=True, port=8000)