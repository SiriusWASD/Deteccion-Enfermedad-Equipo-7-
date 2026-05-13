# 🩺 Sistema Experto para Detección de Riesgo de Diabetes - Equipo 7

Este es un sistema experto basado en reglas y ponderación clínica para el tamizaje temprano de diabetes en pacientes. Utiliza **Flask** para el backend, **Jinja2** para la renderización de interfaces y **PostgreSQL** para la persistencia de datos.

---

## 🛠️ Requisitos Previos

Asegúrate de tener instalados los siguientes programas:
1. **Python 3.10 o superior:** (Asegúrate de marcar "Add Python to PATH" al instalar).
2. **PostgreSQL (versión 16 o 17):** Descarga el instalador oficial y asegúrate de recordar la contraseña del superusuario `postgres`. La herramienta **pgAdmin 4** se instalará automáticamente con él.

---

## 🚀 Guía de Instalación Paso a Paso

### 1. Clonar el Repositorio
Abre una terminal en VS Code y descarga el código:
```bash
git clone [https://github.com/TU_REPOSITORIO/Deteccion-Enfermedad-Equipo-7-.git](https://github.com/TU_REPOSITORIO/Deteccion-Enfermedad-Equipo-7-.git)
cd Deteccion-Enfermedad-Equipo-7-


2. Instalar Librerías
En la terminal de VS Code, ejecuta:

Bash
python -m pip install -r requirements.txt


3. Configurar la Base de Datos (pgAdmin 4)
Abre pgAdmin 4 e ingresa tu contraseña maestra.

Ve a Servers > PostgreSQL > Databases.

Haz clic derecho en Databases > Create > Database...

Nombra la base de datos como: "diabetes_expert_system" y guarda.

4. Archivo de Configuración (.env)
Crea/Modifica un archivo llamado exactamente .env en la raíz del proyecto con este contenido:

Fragmento de código
DB_USER=postgres
DB_PASSWORD=tu_contraseña_de_postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=diabetes_expert_system
SECRET_KEY=clave_secreta_equipo_7


5. Iniciar el Servidor y Crear Tablas
Ejecuta el siguiente comando. Al hacerlo, SQLAlchemy se conectará a PostgreSQL y creará las tablas automáticamente:

Bash
python -m app.main
6. Cargar los Datos Base
Con el servidor corriendo, regresa a pgAdmin 4:

Haz clic derecho sobre la base de datos diabetes_expert_system > Query Tool.

Ejecuta el script SQL (O copia y pega el contenido) ubicado en la carpeta del proyecto para cargar el catálogo de síntomas y el usuario administrador. (scripts/init_db.sql)