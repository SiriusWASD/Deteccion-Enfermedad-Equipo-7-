from flask import Flask, render_template, request, jsonify, redirect, url_for
import psycopg2

app = Flask(__name__, 
            template_folder='../frontend/templates', 
            static_folder='../frontend/static')

# Configuración de conexión
DB_CONFIG = {
    "host": "localhost",
    "database": "sistema_experto",
    "user": "postgres",
    "password": "123456789" 
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diagnosticar', methods=['POST'])
def diagnosticar():
    datos = request.json
    sintomas_usuario = datos.get('sintomas', [])
    
    VALORES_GRAVEDAD = {
        "Visión borrosa": 3,
        "Cicatrización lenta": 3,
        "Hormigueo": 3,
        "Sed excesiva": 2,
        "Orina frecuente": 2,
        "Pérdida de peso": 2,
        "Mucha hambre": 1,
        "Cansancio persistente": 1
    }

    CONSEJOS_ESPECIFICOS = {
        "Visión borrosa": "La visión borrosa requiere una revisión urgente con un oftalmólogo para descartar retinopatía.",
        "Cicatrización lenta": "Presta especial atención al cuidado de tus pies; evita caminar descalzo para prevenir infecciones.",
        "Hormigueo": "El hormigueo puede indicar neuropatía; evita calzado apretado y monitorea tu circulación.",
        "Sed excesiva": "Evita bebidas azucaradas o jugos para calmar la sed; opta únicamente por agua natural.",
        "Pérdida de peso": "La pérdida de peso repentina sugiere que tu cuerpo está quemando grasa por falta de insulina; consulta médica prioritaria."
    }

    puntaje_total = sum(VALORES_GRAVEDAD.get(s, 0) for s in sintomas_usuario)
    tiene_sintoma_critico = any(VALORES_GRAVEDAD.get(s, 0) == 3 for s in sintomas_usuario)
    tips_adicionales = [CONSEJOS_ESPECIFICOS[s] for s in sintomas_usuario if s in CONSEJOS_ESPECIFICOS]

    if puntaje_total >= 7 or (puntaje_total >= 3 and tiene_sintoma_critico):
        resultado = "Alta probabilidad de Diabetes Mellitus."
        base_rec = "Urgente: Vaya con un médico urgentemente y realizece una prueba de Hemoglobina Glicosilada (HbA1c) y perfil de glucosa."
        clase = "riesgo-alto"
    elif puntaje_total >= 3:
        resultado = "Riesgo moderado / Pre-diabetes posible."
        base_rec = "Se recomienda realizar un perfil de glucosa en ayunas esta semana y vigilar la evolución."
        clase = "riesgo-medio"
    else:
        resultado = "Riesgo muy bajo"
        base_rec = "Tus síntomas no son concluyentes en este momento. Mantén hábitos saludables."
        clase = "riesgo-bajo"

    lista_recomendaciones = [base_rec] + tips_adicionales
    recomendacion_db = " ".join(lista_recomendaciones)

    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO registros_evaluacion (enfermedad_detectada, sintomas_reportados, recomendacion) VALUES (%s, %s, %s)",
            (resultado, ", ".join(sintomas_usuario), recomendacion_db)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error en DB: {e}")

    return jsonify({
        'resultado': resultado,
        'riesgo_msg': base_rec,
        'puntos_tips': tips_adicionales,
        'clase': clase
    })

@app.route('/historial')
def ver_historial():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT fecha, enfermedad_detectada, sintomas_reportados, recomendacion FROM registros_evaluacion ORDER BY fecha DESC")
        datos = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('historial.html', registros=datos)
    except Exception as e:
        return f"Error al consultar la base de datos: {e}"

# --- NUEVA RUTA PARA BORRAR HISTORIAL ---
@app.route('/borrar_historial', methods=['POST'])
def borrar_historial():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("DELETE FROM registros_evaluacion") # Elimina todos los registros
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('ver_historial')) # Recarga la página de historial
    except Exception as e:
        return f"Error al borrar el historial: {e}"
    
if __name__ == '__main__':
    app.run(debug=True)