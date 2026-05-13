# ⚙️ Manual Técnico y Topología del Sistema

### Arquitectura (MVC Adaptado)
El proyecto sigue un patrón arquitectónico Modelo-Vista-Controlador (MVC) adaptado:
1.  **Modelos (`app/db/models.py`):** Definen el esquema de datos usando el ORM de SQLAlchemy.
2.  **Vistas (`app/templates/`):** Archivos HTML potenciados por Jinja2 y TailwindCSS para el estilizado.
3.  **Controladores (`app/main.py`):** Rutas de Flask que actúan como puente entre la vista, el modelo y el motor de inferencia.

### Flujo de Datos
1.  El cliente envía los datos del formulario vía HTTP POST a `/procesar_diagnostico`.
2.  El controlador captura los datos, calcula el IMC y registra al nuevo paciente en la tabla `pacientes`.
3.  El controlador extrae los objetos "Síntoma" de la tabla `sintomas_catalogo` utilizando los IDs recibidos.
4.  **Inferencia:** Se instancia la clase `MotorInferenciaDiabetes`, la cual procesa la lista de síntomas en memoria RAM sin realizar conexiones a disco.
5.  Se genera un diccionario de resultados que es empaquetado en un objeto `HistorialDiagnostico` y persistido en PostgreSQL.
6.  La respuesta se renderiza en la vista `resultado.html`.

### Directorio de Archivos Principal
*   `app/main.py`: Arranque de Flask y enrutamiento HTTP.
*   `app/expert_system/inference_engine.py`: Lógica matemática, heurística y reglas médicas aisladas.
*   `app/db/database.py`: Configuración del ORM, manejo de sesiones y conexión a PostgreSQL mediante `psycopg2`.
*   `.env`: Variables de entorno (puertos, secretos, credenciales).