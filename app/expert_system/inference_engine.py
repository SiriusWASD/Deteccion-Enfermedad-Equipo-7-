# Archivo: app/expert_system/inference_engine.py

class MotorInferenciaDiabetes:
    def __init__(self):
        # Aquí podríamos cargar configuraciones extra en el futuro
        self.umbral_riesgo_moderado = 3
        self.umbral_riesgo_alto = 5

    def evaluar_paciente(self, edad: int, es_menor: bool, sintomas: list) -> dict:
        """
        Evalúa los síntomas de un paciente y retorna el diagnóstico inferido.
        sintomas: Lista de diccionarios, ej. [{"nombre": "Poliuria", "peso": 3}, ...]
        """
        puntuacion_total = sum(sintoma["peso"] for sintoma in sintomas)
        nombres_sintomas = [sintoma["nombre"].lower() for sintoma in sintomas]
        
        # 1. Determinar Nivel de Riesgo
        nivel_riesgo = self._calcular_nivel_riesgo(puntuacion_total, nombres_sintomas)
        
        # 2. Inferir Tipo de Diabetes
        tipo_inferido = self._inferir_tipo_diabetes(es_menor, nombres_sintomas, nivel_riesgo)

        return {
            "puntuacion_total": puntuacion_total,
            "nivel_riesgo": nivel_riesgo,
            "tipo_diabetes_inferido": tipo_inferido
        }

    def _calcular_nivel_riesgo(self, puntuacion: int, nombres_sintomas: list) -> str:
        # Una regla de oro médica: Si hay 2 o más síntomas cardinales (peso 3), el riesgo es Alto automático
        sintomas_cardinales = ["poliuria", "polidipsia", "pérdida de peso", "acantosis nigricans", "enuresis"]
        conteo_cardinales = sum(1 for s in nombres_sintomas if s in sintomas_cardinales)

        if puntuacion >= self.umbral_riesgo_alto or conteo_cardinales >= 2:
            return "Alto"
        elif puntuacion >= self.umbral_riesgo_moderado:
            return "Moderado"
        else:
            return "Bajo"

    def _inferir_tipo_diabetes(self, es_menor: bool, nombres_sintomas: list, nivel_riesgo: str) -> str:
        if nivel_riesgo == "Bajo":
            return "Sin riesgo evidente. Mantener hábitos saludables."

        if es_menor:
            # Lógica para menores de edad (Bifurcación Infantil)
            if "acantosis nigricans" in nombres_sintomas or "sobrepeso/obesidad" in nombres_sintomas:
                return "Riesgo de Diabetes Infantil Tipo 2 (Resistencia a la insulina)"
            elif "enuresis" in nombres_sintomas or "pérdida de peso" in nombres_sintomas:
                return "Riesgo Alto de Diabetes Infantil Tipo 1 (Aguda)"
            else:
                return "Posible anomalía glucémica. Requiere evaluación pediátrica."
        else:
            # Lógica para adultos
            if "pérdida de peso" in nombres_sintomas and "poliuria" in nombres_sintomas:
                return "Riesgo de Diabetes Tipo 1 (Posible LADA) o Tipo 2 descompensada"
            elif "visión borrosa" in nombres_sintomas or "cicatrización lenta" in nombres_sintomas:
                return "Riesgo de Diabetes Tipo 2 (Progresiva)"
            elif "sobrepeso/obesidad" in nombres_sintomas or "sedentarismo" in nombres_sintomas:
                return "Riesgo de Prediabetes o Diabetes Tipo 2 temprana"
            else:
                return "Riesgo de anomalía glucémica general."