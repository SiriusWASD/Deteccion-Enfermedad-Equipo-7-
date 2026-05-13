# 🧠 Análisis de Ingeniería y Guía de Defensa Académica
## Proyecto: Sistema Experto para Detección de Riesgo de Diabetes (Equipo 7)

Este documento proporciona una base conceptual profunda sobre las decisiones de diseño, la lógica algorítmica y la justificación técnica del sistema, preparada para responder a cuestionamientos de nivel avanzado.

---

## 1. Arquitectura de Razonamiento: Forward Chaining ⛓️

El núcleo del sistema utiliza un motor de **Encadenamiento hacia Adelante** (*Forward Chaining*). 

### Justificación Técnica
A diferencia del encadenamiento hacia atrás (*Backward Chaining*), que parte de una hipótesis para buscar evidencias, nuestro sistema es **impulsado por datos** (*Data-Driven*). 
*   **Contexto Clínico:** En un entorno de triaje o tamizaje inicial, el sistema no sabe qué enfermedad tiene el paciente. Recolecta hechos (síntomas y datos biofísicos) y los procesa para inferir una conclusión.
*   **Eficiencia:** El encadenamiento hacia adelante es computacionalmente eficiente para este caso de uso, ya que el espacio de búsqueda de síntomas es acotado y las reglas son deterministas.

---

## 2. Formalismo Matemático y Heurística de Ponderación ⚖️

El sistema no realiza una suma lineal simple; aplica una **función de evaluación ponderada** que imita el criterio médico de prioridad.

### Definición del Modelo
Sea $S$ el conjunto de síntomas reportados y $w_i$ el peso asociado a cada síntoma $i$. La puntuación total $P$ se define como:

$$P = \sum_{i \in S} w_i + f(IMC)$$

Donde $f(IMC)$ es una función penalizadora según el rango de masa corporal.

### Reglas de Inferencia Lógica (Excepción de Seguridad)
Implementamos un mecanismo de **anulación selectiva** (*Override Rule*) para casos críticos. Si definimos $C \subset S$ como el subconjunto de síntomas cardinales (Peso 3), la lógica de decisión sigue este comportamiento:

$$Riesgo = \begin{cases} \text{Alto} & \text{si } |C| \ge 2 \\ \text{Evaluación Ponderada} & \text{en otro caso} \end{cases}$$

**Defensa:** "Profesor, el sistema no es un simple contador. Posee una capa de 'prioridad clínica' donde ciertos síntomas tienen un valor diagnóstico tan alto que pueden determinar el riesgo por sí solos, emulando el juicio de un especialista".

---

## 3. Ingeniería de Software: Desacoplamiento y Modularidad 🧩

El sistema sigue el principio de **Separación de Intereses** (*Separation of Concerns*).

*   **Expert System Shell:** El motor de inferencia (`inference_engine.py`) es agnóstico a la interfaz. No sabe que existe una base de datos o una página web; solo recibe objetos de conocimiento y devuelve inferencias.
*   **Escalabilidad:** Esta arquitectura permite que la "Base de Conocimientos" (MySQL) crezca o cambie sin modificar el "Motor de Inferencia". Si quisiéramos detectar Hipertensión, solo cambiaríamos los datos del catálogo y las reglas lógicas, manteniendo el 90% del código intacto.

---

## 4. Justificación del Stack Tecnológico (Flask + PostgreSQL) 💻

### Flask como Microframework (Backend)
Elegimos **Flask** por su naturaleza de microframework modular. En el desarrollo de Sistemas Expertos, se busca que la interfaz no esté fuertemente acoplada a la lógica. 
*   **Renderizado de Servidor (SSR):** La integración nativa con **Jinja2** nos permitió crear interfaces dinámicas basadas en la lógica de control del servidor, asegurando que el motor de inferencia (Python) dicte directamente el estado de la vista HTML.
*   **Estabilidad:** Flask es un estándar de la industria, extremadamente maduro y predecible, lo que minimiza los errores de la capa de red al procesar datos médicos sensibles.

### Persistencia ACID con PostgreSQL
La exigencia de usar **PostgreSQL** eleva el estándar del proyecto a nivel empresarial.
*   **Cumplimiento de Estándares:** PostgreSQL es el motor de base de datos relacional de código abierto más avanzado. Su estricto cumplimiento del estándar SQL y su robusto manejo de concurrencia garantizan que no haya condiciones de carrera al guardar diagnósticos.
*   **Integridad Referencial Estricta:** Utilizamos **SQLAlchemy (ORM)** para gestionar las relaciones entre Usuarios, Pacientes e Historiales. Si un diagnóstico falla en completarse en la base de datos, la transacción hace *rollback*, evitando historiales médicos corruptos o huérfanos.

---

## 6. Guía de Respuestas Rápidas (Q&A) ⚡

**P: ¿Cómo validaron la base de conocimientos?**
**R:** "Se utilizaron los criterios de la **ADA (American Diabetes Association)** e **ISPAD**, traduciendo los síntomas clínicos en pesos numéricos (1-3) según su correlación con la patología".

**P: ¿Por qué no usar Redes Neuronales?**
**R:** "En medicina, la **explicabilidad** es vital. Una Red Neuronal es una caja negra; un Sistema Experto basado en reglas puede explicar exactamente por qué llegó a una conclusión (explicabilidad de traza)".

**P: ¿Cómo manejan la seguridad de los datos?**
**R:** "Implementamos sesiones encriptadas y el desacoplamiento de credenciales mediante variables de entorno (`.env`), siguiendo las mejores prácticas de desarrollo seguro".

---
**Elaborado por el Equipo 7 - 2026**