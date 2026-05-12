DETECCION-ENFERMEDAD-EQUIPO-7/
│
├── app/                        # Contiene toda la lógica principal de la aplicación
│   ├── api/                    # Endpoints de la API (rutas para login, síntomas, diagnóstico)
│   ├── core/                   # Configuraciones globales y seguridad (manejo de sesiones/tokens)
│   ├── db/                     # Conexión a MySQL, modelos relacionales y operaciones CRUD
│   ├── expert_system/          # Motor de inferencia y base de conocimiento (las reglas lógicas)
│   ├── static/                 # Archivos estáticos (CSS, Bootstrap, imágenes, JS)
│   ├── templates/              # Vistas HTML (Login, formularios, resultados)
│   └── main.py                 # Archivo de arranque de FastAPI
│
├── docs/                       # Documentación del proyecto (manual técnico, capturas, topología)
│
├── scripts/                    # Scripts SQL para inicializar la base de datos y poblar datos base
│
├── .env                        # Variables de entorno (credenciales de MySQL, claves secretas)
├── .gitignore                  # Archivos y carpetas que Git debe ignorar (ej. entornos virtuales, .env)
├── requirements.txt            # Dependencias de Python (fastapi, uvicorn, mysql-connector-python, jinja2)
└── README.md                   # Descripción general del repositorio y pasos de instalación