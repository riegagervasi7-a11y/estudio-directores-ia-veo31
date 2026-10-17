"""
juez_vision_vlm.py
Módulo del Juez 2 (Visión - VLM Critic) para Google Nano Banana Pro.

Este script define la plantilla de auditoría forense visual para modelos multimodales
(como Gemini 1.5/2.0 Pro Vision o GPT-4o). Puede ejecutarse contra la API de Gemini
o como función de evaluación en el pipeline.
"""

import os
import json
from typing import Dict, Any

# Prompt forense especializado para el Juez de Visión
PROMPT_AUDITORIA_FORENSE = """
Actúa como un perito forense de fotografía y director de fotografía analógica de élite.
Tu misión es inspeccionar esta imagen minuciosamente para determinar si es una FOTOGRAFÍA REAL
o si presenta CUALQUIER indicio de haber sido generada por Inteligencia Artificial (Aspecto IA / CGI).

Analiza rigurosamente los siguientes 5 puntos críticos:
1. TEXTURA DE LA PIEL:
   - ¿Se observan microporos reales, vello facial fino (peach fuzz) y brillo orgánico por sebo natural?
   - ¿O la piel tiene textura de cera, plástico, aerógrafo o muñeca de silicona?
2. OJOS Y MIRADA:
   - ¿Los reflejos especulares (catchlights) en las córneas son físicamente coherentes con las fuentes de luz visibles?
   - ¿O tienen el típico brillo vidrioso, idéntico o descentrado de IA?
3. CABELLO Y BORDES:
   - ¿Hay hebras individuales sueltas (flyaways) con desenfoque de movimiento óptico natural?
   - ¿O el cabello parece una masa sólida recortada digitalmente?
4. FÍSICA ÓPTICA Y BOKEH:
   - ¿La profundidad de campo tiene una transición gradual auténtica de lente físico (ej. 85mm o 35mm)?
   - ¿O es un recorte de mapa de profundidad digital con bordes borrosos falsos?
5. IMPERFECCIONES Y GRANO:
   - ¿Existe ruido de sensor o grano químico orgánico (ej. Kodak Portra / Cinestill)?
   - ¿O la imagen tiene esa nitidez digital sobresaturada ("over-sharpened") típica de IA?

Responde ÚNICAMENTE en formato JSON con la siguiente estructura exacta:
{
  "puntuacion_realismo": <float de 1.0 a 10.0>,
  "es_indistinguible_de_foto_real": <true si puntuacion >= 9.0, false si no>,
  "defectos_ia_detectados": [<lista de strings con defectos encontrados, ej: "piel suavizada", "reflejo ocular falso">],
  "puntos_fuertes_fotograficos": [<lista de aciertos, ej: "poros auténticos", "flash creíble">],
  "recomendacion_para_el_prompt": "<instrucción concreta en inglés para que el generador de prompts corrija los defectos visuales detectados>"
}
"""

def simular_o_evaluar_vision(ruta_imagen: str, api_key: str = None) -> Dict[str, Any]:
    """
    Envía la imagen generada por Nano Banana Pro a Gemini Vision (si hay API key)
    o provee la estructura de auditoría para la integración en la nube.
    """
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        # Modo simulación / template de integración
        return {
            "status": "template_ready",
            "instrucciones": "Configura la variable de entorno GEMINI_API_KEY para llamar a Gemini Vision automáticamente.",
            "prompt_auditoria": PROMPT_AUDITORIA_FORENSE.strip()
        }

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        # Cargar archivo de imagen
        with open(ruta_imagen, "rb") as f:
            image_bytes = f.read()

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                image_bytes,
                PROMPT_AUDITORIA_FORENSE
            ]
        )
        
        # Limpieza de bloque json si el modelo incluye markdown
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
            
        return json.loads(text)
    except Exception as e:
        return {"error": f"Error al evaluar con Gemini Vision: {str(e)}"}

if __name__ == "__main__":
    print("Módulo Juez 2 (Visión) cargado correctamente.")
    print("Prompt de peritaje forense listo para inspeccionar fotos de Nano Banana Pro.")
