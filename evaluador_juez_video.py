"""
evaluador_juez_video.py
Evaluador automatizado (Juez de Video) basado en la Rúbrica Maestra para Veo 3.1.
Califica de 0.0 a 10.0 los prompts de Image-to-Video (I2V).
"""

import re
from typing import Dict, Any, List

POISON_WORDS_VIDEO = [
    "cinematic", "smooth stabilized", "hyperrealistic", "ultra realistic",
    "8k", "4k", "masterpiece", "octane render", "cgi", "drone shot",
    "fast zoom", "stunning", "beautiful", "perfect motion", "unreal engine"
]

RE_DESCRIPTION_PATTERNS = [
    r"\b(wearing a [a-z]+ [a-z]+|wearing [a-z]+ coat|wearing [a-z]+ jacket)\b",
    r"\b(with blue eyes|with green eyes|with brown eyes|with grey beard|with blonde hair)\b",
    r"\b(handsome face|beautiful face|aged face|pretty face)\b"
]

CAMERA_PATTERNS = [
    r"\b(push-in|pull-out|tracking|dolly|pan|tilt|tripod|handheld|lock-off|camera breath|crane)\b",
    r"\b(slow|subtle|steady|gentle|static)\b"
]

TIMING_ACTION_PATTERNS = [
    r"\b(at second \d|at \ds|between second \d and \d)\b",
    r"\b(blink|blinks|breath|exhale|inhale|glance|shifts weight|squint|micro-movement)\b"
]

def evaluar_prompt_video(prompt: str) -> Dict[str, Any]:
    score = 10.0
    penalizaciones: List[str] = []
    bonificaciones: List[str] = []
    prompt_lower = prompt.lower()

    # 1. Palabras tóxicas
    toxicas = [w for w in POISON_WORDS_VIDEO if re.search(r"\b" + re.escape(w) + r"\b", prompt_lower)]
    if toxicas:
        score -= len(toxicas) * 3.0
        penalizaciones.append(f"Palabras tóxicas detectadas (-3.0 c/u): {', '.join(toxicas)}")

    # 2. Re-descripción de apariencia (Causa de morphing / derretimiento)
    redesc = [p for p in RE_DESCRIPTION_PATTERNS if re.search(p, prompt_lower)]
    if redesc:
        score -= 2.5
        penalizaciones.append("Re-describe ropa o rostro (riesgo crítico de derretimiento facial) (-2.5 pts)")

    # 3. Frase de anclaje
    if re.search(r"\bmaintain.*from the first frame\b", prompt_lower):
        bonificaciones.append("Frase obligatoria de preservación de ancla presente (+2.0 pts)")
    else:
        score -= 2.0
        penalizaciones.append("Falta frase de preservación del ancla ('Maintain... from the first frame') (-2.0 pts)")

    # 4. Movimiento de Cámara con Inercia
    cam_matches = [p for p in CAMERA_PATTERNS if re.search(p, prompt_lower)]
    if len(cam_matches) >= 2:
        bonificaciones.append("Movimiento de cámara físico con inercia y velocidad definidos")
    else:
        score -= 2.0
        penalizaciones.append("Falta movimiento de cámara físico o carece de inercia/velocidad (-2.0 pts)")

    # 5. Micro-acciones del Sujeto a velocidad humana
    timing_matches = [p for p in TIMING_ACTION_PATTERNS if re.search(p, prompt_lower)]
    if len(timing_matches) >= 1:
        bonificaciones.append("Micro-acción humana con cadencia o segundo específico")
    else:
        score -= 1.5
        penalizaciones.append("Acción del sujeto genérica o sin segundo de inicio (-1.5 pts)")

    # 6. Audio explícito
    if "audio:" in prompt_lower:
        bonificaciones.append("Etiqueta 'Audio:' explícita para sonido ambiental")
    else:
        score -= 1.0
        penalizaciones.append("Falta etiqueta 'Audio:' (Veo no generará sonido ambiental) (-1.0 pts)")

    # Rango 0 a 10
    score = max(0.0, min(10.0, score))

    if score >= 9.0:
        clasificacion = "CHOSEN (Aprobado para Video)"
    elif score <= 6.5:
        clasificacion = "REJECTED (Rechazado para DPO)"
    else:
        clasificacion = "NEUTRAL (Requiere ajuste)"

    return {
        "score": round(score, 1),
        "clasificacion": clasificacion,
        "penalizaciones": penalizaciones,
        "bonificaciones": bonificaciones
    }

if __name__ == "__main__":
    prompt_malo = "Cinematic 8k smooth camera moving fast around the handsome fisherman smiling and walking, hyperrealistic video, masterpiece, octane render."
    prompt_bueno = (
        "Maintain the exact subject, facial features, and environment from the first frame. "
        "CAMERA: Slow subtle push-in on an 85mm lens with natural handheld camera breath and gentle physical inertia. "
        "SUBJECT: The subject remains nearly still. At second 2, he blinks naturally and exhales a faint mist of breath into the chilly air. Micro-movements only, natural human weight. "
        "ENVIRONMENT: Overcast 5600K lighting remains completely constant. "
        "Audio: cold coastal wind whistling softly, quiet harbor water lap, zero music."
    )

    print("--- TEST PROMPT MALO VIDEO ---")
    r_m = evaluar_prompt_video(prompt_malo)
    print(f"Score: {r_m['score']} | {r_m['clasificacion']}")

    print("\n--- TEST PROMPT BUENO VIDEO ---")
    r_b = evaluar_prompt_video(prompt_bueno)
    print(f"Score: {r_b['score']} | {r_b['clasificacion']}")
