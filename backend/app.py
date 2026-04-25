from flask import Flask, render_template, request, jsonify
import psycopg2

app = Flask(__name__, template_folder='../templates')

# Configuración de conexión (Ajusta con tu contraseña de Postgres)
DB_CONFIG = {
    "host": "localhost",
    "database": "sistema_experto",
    "user": "postgres",
    "password": "123456789" 
}

# Base de Conocimiento (Diccionario)
SINTOMAS_DIABETES = ["Sed excesiva", "Mucha hambre", "Orina frecuente", "Visión borrosa", "Cansancio persistente"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diagnosticar', methods=['POST'])
def diagnosticar():
    datos = request.json
    sintomas_usuario = datos.get('sintomas', [])
    
    # Motor de Inferencia (Reglas If-Then)
    puntos = sum(1 for s in sintomas_usuario if s in SINTOMAS_DIABETES)
    
    if puntos >= 3:
        resultado = "Alta probabilidad de Diabetes Mellitus."
        recomendacion = "Urgente: Agende una prueba de glucosa en ayunas."
    elif puntos >= 1:
        resultado = "Riesgo moderado / Síntomas leves."
        recomendacion = "Monitoree su dieta y consulte a su médico preventivamente."
    else:
        resultado = "Sin indicios claros."
        recomendacion = "Mantenga un estilo de vida saludable."

    # Guardar en PostgreSQL
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO registros_evaluacion (enfermedad_detectada, sintomas_reportados, recomendacion) VALUES (%s, %s, %s)",
            (resultado, ", ".join(sintomas_usuario), recomendacion)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error en DB: {e}")

    return jsonify({"diagnostico": resultado, "recomendacion": recomendacion})

@app.route('/historial')
def ver_historial():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        # Nota: Cambié 'enfermedad_detected' por 'enfermedad_detectada'
        cur.execute("SELECT fecha, enfermedad_detectada, sintomas_reportados, recomendacion FROM registros_evaluacion ORDER BY fecha DESC")
        datos = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('historial.html', registros=datos)
    except Exception as e:
        return f"Error al consultar la base de datos: {e}"
    
if __name__ == '__main__':
    app.run(debug=True)