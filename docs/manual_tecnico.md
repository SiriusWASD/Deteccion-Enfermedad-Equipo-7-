# Manual Técnico: Sistema Experto para Detección de Diabetes

## 1. Topología del Sistema (Entorno Local)

El sistema opera bajo una arquitectura monolítica local (Localhost) de tres capas integradas, garantizando una comunicación de muy baja latencia entre la interfaz y el motor de inferencia.

* **Capa de Presentación (Cliente):** Navegador web local (Chrome, Edge, Firefox) que renderiza las vistas HTML generadas por Jinja2 y estilizadas con TailwindCSS.
* **Capa de Aplicación (Servidor Lógico):** Servidor ASGI Uvicorn ejecutando la API construida en FastAPI (Python). Esta capa contiene las rutas de acceso, el control de sesiones y orquesta las llamadas al motor de inteligencia artificial.
* **Capa de Inteligencia (Sistema Experto):** Módulo aislado en Python orientado a objetos (`MotorInferenciaDiabetes`) que ejecuta la lógica de encadenamiento hacia adelante basado en pesos.
* **Capa de Persistencia (Base de Datos):** Servidor MySQL local (XAMPP/MAMP/Workbench) conectado a través del ORM SQLAlchemy. Asegura la integridad referencial de los usuarios, pacientes y el historial de diagnósticos.

---

## 2. Flujo de Datos

El recorrido de la información, desde la captura hasta la inferencia, sigue un modelo estrictamente unidireccional por transacción:

1. **Autenticación:** El usuario envía credenciales a `/login`. El servidor valida contra MySQL. Si es exitoso, se genera una *Cookie de Sesión* encriptada que se devuelve al navegador.
2. **Selección de Perfil:** En `/dashboard`, el usuario bifurca el flujo eligiendo entre Adulto o Menor.
3. **Extracción de Conocimiento:** Al cargar la vista `/consulta/{tipo}`, el servidor realiza un `SELECT` a la tabla `sintomas_catalogo` en MySQL, filtrando únicamente los síntomas que aplican al perfil demográfico seleccionado, y los inyecta en el formulario HTML.
4. **Procesamiento de Inferencia:** 
    * El usuario hace un `POST` a `/procesar_diagnostico` con sus datos físicos (peso, estatura) y un array de IDs de síntomas.
    * FastAPI calcula el IMC y traduce los IDs en objetos con "nombre" y "peso" lógico.
    * Se instancia el `MotorInferenciaDiabetes`, el cual procesa los síntomas y retorna un diccionario con el nivel de riesgo y el tipo de diabetes inferido.
5. **Persistencia y Retorno:** El servidor guarda el registro relacional en `historial_diagnosticos` y `detalle_diagnostico_sintomas`. Finalmente, inyecta los resultados en `resultado.html`, cambiando el color de la interfaz (Verde, Amarillo, Rojo) según la gravedad.

---

## 3. Análisis de Decisiones (Motor de Inferencia)

El núcleo del sistema experto utiliza un mecanismo de evaluación ponderada, estructurado bajo guías clínicas internacionales (ADA, ISPAD, OMS).

### 3.1. Sistema de Ponderación (Pesos)
Cada síntoma en el catálogo tiene un valor numérico:
* **Peso 3 (Cardinales / Urgentes):** Poliuria, Polidipsia, Pérdida de peso, Acantosis nigricans, Enuresis.
* **Peso 2 (Secundarios / Alerta):** Visión borrosa, Sobrepeso (IMC alto), Antecedentes familiares, Cicatrización lenta.
* **Peso 1 (Generales):** Fatiga, Sedentarismo.

### 3.2. Reglas de Inferencia Lógica
El motor toma decisiones basadas en la sumatoria total y la presencia de variables específicas:

* **Regla de Umbrales:**
    * Si Puntuación Total < 3 → Riesgo **Bajo**.
    * Si Puntuación Total ≥ 3 y < 5 → Riesgo **Moderado**.
    * Si Puntuación Total ≥ 5 → Riesgo **Alto**.

* **Regla de Seguridad Clínica (Override):** Si el motor detecta **2 o más síntomas cardinales** (Peso 3), el riesgo escala automáticamente a **Alto**, ignorando la sumatoria estándar.

* **Bifurcación Pediátrica:** Si el atributo `es_menor` es `True`, el motor ignora las reglas de adultos y busca específicamente marcadores de resistencia a la insulina (Acantosis nigricans) para inferir *Diabetes Infantil Tipo 2*, o pérdida rápida de peso y enuresis para inferir *Diabetes Infantil Tipo 1 (Aguda)*.

---

## 4. Limitaciones del Sistema Experto

Para mantener la validez académica y médica del proyecto, se reconocen las siguientes limitaciones de la primera versión iterativa:

1. **Falta de Memoria Longitudinal:** El motor actual evalúa la salud del paciente basándose en una "fotografía" del momento presente. Aunque la base de datos guarda el historial, el motor lógico aún no lee consultas previas para inferir la progresión de la enfermedad.
2. **Dependencia de la Percepción del Usuario:** Al ser un cuestionario auto-reportado, la precisión de la inferencia está ligada a la interpretación subjetiva del usuario sobre sus propios síntomas.
3. **Exclusión de Pruebas Bioquímicas:** El sistema no cuenta actualmente con un módulo para ingresar resultados de laboratorio (Glucosa en ayuno, HbA1c), los cuales son el estándar de oro para un diagnóstico definitivo.
4. **Límite Legal y Médico:** El algoritmo carece de validez diagnóstica oficial. Su propósito es funcionar como una herramienta de tamizaje (screening) temprano, no para recetar ni confirmar clínicamente la patología.

---

## 5. Capturas de Ejecución del Sistema

*(Instrucciones de llenado: Reemplaza las rutas entre paréntesis con las imágenes reales generadas al correr tu proyecto localmente).*

### 5.1. Pantalla de Autenticación
![Captura de Login - Mostrar formulario de acceso y validación de errores](docs/capturas/pantalla_login.png)

### 5.2. Panel Principal (Dashboard)
![Captura del Dashboard - Mostrar la bifurcación entre Adulto y Menor](docs/capturas/pantalla_dashboard.png)

### 5.3. Interfaz de Ingesta de Datos (Consulta)
![Captura de Formulario - Mostrar secciones de datos físicos y síntomas divididos por gravedad](docs/capturas/pantalla_consulta.png)

### 5.4. Resultado de Inferencia (Riesgo Alto - Semáforo Rojo)
![Captura de Resultado Alto - Mostrar alerta roja con 2+ síntomas cardinales](docs/capturas/resultado_alto.png)

### 5.5. Resultado de Inferencia (Riesgo Bajo - Semáforo Verde)
![Captura de Resultado Bajo - Mostrar resultado verde con síntomas generales](docs/capturas/resultado_bajo.png)