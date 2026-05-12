# 🩺 Sistema Experto para Detección de Diabetes - Equipo 7

Este es un sistema experto basado en reglas y ponderación clínica para el tamizaje temprano de diabetes en pacientes adultos y menores. Utiliza **FastAPI** para el backend y **MySQL** para la persistencia de datos.

---

## 🛠️ Requisitos Previos (Antes de empezar)

VS Code por sí solo no puede ejecutar el código. Tus compañeros deben asegurarse de instalar:

1. **Python 3.10 o superior:** [Descargar aquí](https://www.python.org/downloads/). 
   * *IMPORTANTE:* Durante la instalación, marcar la casilla **"Add Python to PATH"**

---

## 🚀 Guía de Instalación Paso a Paso

Sigue estos pasos en orden para correr el programa en tu computadora:

### 1. Clonar el Repositorio
Abre una terminal en VS Code y escribe:
```bash
git clone [https://github.com/TU_REPOSITORIO/Deteccion-Enfermedad-Equipo-7-.git](https://github.com/TU_REPOSITORIO/Deteccion-Enfermedad-Equipo-7-.git)
cd Deteccion-Enfermedad-Equipo-7-
2. Configurar la Base de Datos
Abre el Panel de Control de MySQL y haz clic en Start en el módulo de MySQL

Importa el archivo localizado en scripts/init_db.sql o copia su contenido y ejecútalo en la pestaña SQL.

3. Instalar Librerías
En la terminal de VS Code, ejecuta el siguiente comando para instalar todo lo necesario:

Bash
python -m pip install -r requirements.txt
4. Configurar Variables de Entorno
Cambia un archivo llamado exactamente .env en la raíz del proyecto con lo siguiente:

Fragmento de código
DB_USER=root
DB_PASSWORD="tu pasword"
DB_HOST=localhost
DB_PORT=3306
DB_NAME=diabetes_expert_system
SECRET_KEY=clave_secreta_equipo_7

🖥️ Cómo Ejecutar el Programa
Una vez configurado todo, lanza el servidor con este comando:

Bash
python -m uvicorn app.main:app --reload
Cuando veas el mensaje Uvicorn running on http://127.0.0.1:8000, abre tu navegador y entra a:
👉 http://localhost:8000

🧪 Datos de Prueba Rápidos
Para probar el sistema de inmediato sin registrarte manualmente en la base de datos:

Ve a la opción "Regístrate aquí" en la pantalla de inicio.

Crea una cuenta con cualquier correo y contraseña.

Inicia sesión y comienza tu primera consulta.

📂 Estructura del Proyecto
/app: Contiene la lógica del servidor, modelos de datos y el motor experto.

/app/templates: Archivos HTML con el diseño de la interfaz.

/docs: Manual técnico y documentación detallada.

requirements.txt: Lista de dependencias del sistema.


---

### Un consejo final
Si alguno de tus compañeros recibe el error de **"Access Denied"** en la base de datos, recuérdales revisar el archivo `.env`. En instalaciones estándar de MySQL, el usuario es `root` y la contraseña se deja vacía.
