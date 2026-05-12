# Archivo: app/main.py
import os
from typing import List, Optional

from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from sqlalchemy.orm import Session
from sqlalchemy import or_

# Importar base de datos, modelos y motor
from app.db.database import engine, Base, get_db
from app.db.models import Usuario, SintomaCatalogo, Paciente, HistorialDiagnostico
from app.expert_system.inference_engine import MotorInferenciaDiabetes

# 1. Inicializar Base de Datos
Base.metadata.create_all(bind=engine)

# 2. Inicializar FastAPI
app = FastAPI(title="Sistema Experto Diabetes v1.1")

# 3. Configuración de Sesiones
SECRET_KEY = os.getenv("SECRET_KEY", "clave_secreta_para_desarrollo_local")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# 4. Configurar Plantillas
templates = Jinja2Templates(directory="app/templates")

# ==========================================
# RUTAS DE AUTENTICACIÓN Y REGISTRO
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def pagina_login(request: Request, mensaje: Optional[str] = None):
    """Muestra la pantalla de inicio de sesión."""
    if request.session.get("usuario_id"):
        return RedirectResponse(url="/dashboard")
    return templates.TemplateResponse(request, "login.html", {"mensaje": mensaje})

@app.post("/login")
async def procesar_login(
    request: Request, 
    correo: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    """Valida credenciales y crea la sesión."""
    usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    
    if not usuario or usuario.password_hash != password:
        return templates.TemplateResponse(request, "login.html", {
            "mensaje": "Credenciales inválidas. Intente de nuevo."
        })
    
    request.session["usuario_id"] = usuario.id_usuario
    request.session["nombre"] = usuario.nombre_completo
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/registro", response_class=HTMLResponse)
async def pantalla_registro(request: Request):
    """Muestra el formulario para crear una nueva cuenta."""
    return templates.TemplateResponse(request, "registro.html", {"mensaje": None})

@app.post("/procesar_registro")
async def procesar_registro(
    request: Request,
    nombre: str = Form(...),
    correo: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Crea un nuevo usuario en la base de datos."""
    existe = db.query(Usuario).filter(Usuario.correo == correo).first()
    if existe:
        return templates.TemplateResponse(request, "registro.html", {
            "mensaje": "El correo ya está registrado."
        })
    
    nuevo_usuario = Usuario(nombre_completo=nombre, correo=correo, password_hash=password)
    db.add(nuevo_usuario)
    db.commit()
    return RedirectResponse(url="/?mensaje=Cuenta+creada+exitosamente", status_code=303)

@app.get("/logout")
async def cerrar_sesion(request: Request):
    """Limpia la sesión y redirige al login."""
    request.session.clear()
    return RedirectResponse(url="/")

# ==========================================
# RUTAS DEL PANEL Y CONSULTAS
# ==========================================

@app.get("/dashboard", response_class=HTMLResponse)
async def panel_principal(request: Request):
    """Pantalla de bienvenida y selección de perfil."""
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return RedirectResponse(url="/")
    
    nombre = request.session.get("nombre")
    return templates.TemplateResponse(request, "dashboard.html", {"nombre": nombre})

@app.get("/historial", response_class=HTMLResponse)
async def ver_historial(request: Request, db: Session = Depends(get_db)):
    """Muestra todas las consultas previas del usuario logueado."""
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return RedirectResponse(url="/")
    
    consultas = db.query(HistorialDiagnostico).join(Paciente).filter(
        Paciente.id_usuario == usuario_id
    ).order_by(HistorialDiagnostico.fecha_consulta.desc()).all()
    
    return templates.TemplateResponse(request, "historial.html", {"consultas": consultas})

@app.get("/consulta/{tipo_paciente}", response_class=HTMLResponse)
async def pantalla_consulta(request: Request, tipo_paciente: str, db: Session = Depends(get_db)):
    """Formulario de síntomas filtrado por tipo de paciente."""
    if not request.session.get("usuario_id"):
        return RedirectResponse(url="/")

    sintomas = db.query(SintomaCatalogo).filter(
        or_(SintomaCatalogo.aplica_a == tipo_paciente, SintomaCatalogo.aplica_a == 'ambos')
    ).all()

    return templates.TemplateResponse(request, "consulta.html", {
        "tipo": tipo_paciente,
        "sintomas": sintomas
    })

@app.post("/procesar_diagnostico", response_class=HTMLResponse)
async def procesar_diagnostico(
    request: Request,
    es_menor: str = Form(...),
    nombre_paciente: str = Form(...),
    edad: int = Form(...),
    peso: float = Form(...),
    estatura: float = Form(...),
    sintomas_ids: Optional[List[int]] = Form(default=[]),
    db: Session = Depends(get_db)
):
    """Ejecuta la inferencia, guarda en DB y muestra resultados por colores."""
    usuario_id = request.session.get("usuario_id")
    if not usuario_id:
        return RedirectResponse(url="/")

    # 1. Cálculos de salud
    imc = peso / (estatura ** 2) if estatura > 0 else 0
    es_menor_bool = es_menor.lower() == 'true'

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

    # 6. Respuesta Visual
    return templates.TemplateResponse(request, "resultado.html", {
        "paciente": nuevo_paciente,
        "resultado": resultado,
        "sintomas": sintomas_db
    })