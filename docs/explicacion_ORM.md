Imagina que tu base de datos MySQL y tu código en Python hablan dos idiomas completamente distintos.

MySQL habla en Tablas y Consultas SQL (SELECT, INSERT, WHERE).

Python habla en Objetos y Clases.

Un ORM es un "traductor simultáneo" que se coloca en medio de los dos. En lugar de escribir texto plano con sentencias SQL dentro de tu código Python (lo cual es propenso a errores y ataques de seguridad), tú escribes código Python normal y el ORM se encarga de convertirlo a SQL por detrás.

Ejemplo visual de cómo funciona:

Si quisiéramos registrar a un nuevo paciente, sin ORM tendrías que escribir algo así:

Python
# Así se haría SIN ORM (Código crudo)
cursor.execute("INSERT INTO pacientes (id_usuario, nombre_paciente, edad) VALUES (1, 'Carlos', 45)")
Con nuestro ORM (SQLAlchemy), lo haremos de forma orientada a objetos:

Python
# Así lo haremos CON ORM (Elegante y seguro)
nuevo_paciente = Paciente(id_usuario=1, nombre_paciente="Carlos", edad=45)
db.add(nuevo_paciente)
db.commit()
¿Por qué elegí esto para tu proyecto? (Justificación para tu rúbrica)
Validación de Datos (Requisito de tu rúbrica): Al combinar SQLAlchemy con otra herramienta llamada Pydantic (que viene incluida en FastAPI), si alguien intenta enviar una letra en el campo "edad", la API lo bloqueará automáticamente antes de que llegue a la base de datos y devolverá un error estructurado.

Seguridad: Nos protege automáticamente contra la Inyección SQL, una de las vulnerabilidades más comunes.

Mantenibilidad: Si el día de mañana decides cambiar MySQL por PostgreSQL, no tienes que reescribir ni una sola línea de código SQL; el ORM hace la traducción al nuevo motor automáticamente.