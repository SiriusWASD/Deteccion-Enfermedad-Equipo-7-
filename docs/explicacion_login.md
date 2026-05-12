¿Cómo funciona la Autenticación por Cookies/Sesiones?
Imagina que este sistema es como la recepción de un gran gimnasio o centro deportivo.

El Inicio de Sesión (Presentar la identificación): El usuario llega a tu página principal y envía su correo y contraseña. El servidor (FastAPI) revisa en la base de datos de MySQL si esos datos son correctos.

La Sesión (La pulsera de acceso): Si todo coincide, el servidor crea un espacio seguro en su memoria llamado "Sesión". Luego, le envía al navegador del usuario una "Cookie", que es básicamente una pulsera de acceso con un código único (encriptado).

La Navegación (Moverse por las instalaciones): Cada vez que el usuario hace clic para ir a la página de "Elegir paciente" o "Seleccionar síntomas", su navegador le muestra automáticamente esa "pulsera" (Cookie) al servidor.

La Validación Automática: El servidor ve la Cookie, reconoce el código, y le da acceso a las pantallas sin pedirle el correo y la contraseña en cada clic. Si el usuario cierra sesión, el servidor "corta la pulsera" y el acceso se bloquea.