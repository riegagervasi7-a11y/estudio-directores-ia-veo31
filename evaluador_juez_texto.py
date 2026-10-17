"""
evaluador_juez_texto.py
Evaluador automatizado (Juez 1 de Texto) basado en la Rúbrica Maestra Anti-IA
para Google Nano Banana Pro.
"""

import re
from typing import Dict, Any, List

POISON_WORDS = [
    "hyperrealistic", "photorealistic", "ultra-realistic", "hyper-realistic",
    "8k", "4k", "uhd", "masterpiece", "award-winning", "trending on artstation",
    "unreal engine", "octane render", "perfect skin", "smooth skin", "flawless",
    "cinematic lighting", "dramatic rim light", "volumetric lighting", "best quality",
    "sharp focus" # cuando se usa solo como buzzword
]

OPTICAL_TERMS = [
    r"\b(28mm|35mm|50mm|85mm|105mm|135mm)\b",
    r"\bf/[1-9](\.[0-9])?\b",
    r"\b(iso\s*\d{2,4})\b",
    r"\b(shutter speed|1/\d{2,4}s)\b",
    r"\b(depth of field|bokeh|focal length)\b",
    r"\b(kodak|cinestill|portra|fujifilm|leica|sony a7|canon eos|film stock|raw)\b"
]

IMPERFECTION_TERMS = [
    r"\b(pores|skin texture|micro-texture)\b",
    r"\b(peach fuzz|vellus hair|stubble|flyaway|stray hair|flyaways)\b",
    r"\b(blemishes|freckles|wrinkles|crow's feet|fine lines|creases|sunspots)\b",
    r"\b(natural skin sheen|subtle sweat|perspiration|specular highlight|asymmetry|asymmetrical)\b"
]

LIGHTING_TERMS = [
    r"\b(direct flash|on-camera flash|point-and-shoot)\b",
    r"\b(window light|overcast|diffuse light|diffuse ambient|natural ambient|ambient daylight|ambient reflections|harsh sunlight|tungsten|halogen|softbox|octabox|profoto|key light|rim light|studio lighting)\b",
    r"\b(shadow roll-off|specular|shadow falloff|kelvin|\d{4}k)\b"
]

def evaluar_prompt(prompt: str) -> Dict[str, Any]:
    score = 10.0
    penalizaciones: List[str] = []
    bonificaciones: List[str] = []
    prompt_lower = prompt.lower()

    # 1. Chequeo de palabras tóxicas (Poison List)
    palabras_toxicas_encontradas = []
    for word in POISON_WORDS:
        pattern = r"\b" + re.escape(word) + r"\b"
        if re.search(pattern, prompt_lower):
            palabras_toxicas_encontradas.append(word)
            score -= 3.0

    if palabras_toxicas_encontradas:
        penalizaciones.append(f"Palabras tóxicas detectadas (-3.0 c/u): {', '.join(palabras_toxicas_encontradas)}")

    # 2. Chequeo de Óptica y Cámara
    optica_match = [p for p in OPTICAL_TERMS if re.search(p, prompt_lower)]
    if len(optica_match) >= 3:
        bonificaciones.append(f"Excelente especificación de óptica/cámara ({len(optica_match)} parámetros encontrados)")
    elif len(optica_match) == 0:
        score -= 2.5
        penalizaciones.append("Falta total de especificaciones ópticas/lente/cámara (-2.5 pts)")

    # 3. Chequeo de Micro-imperfecciones humanas
    imperfecciones_match = [p for p in IMPERFECTION_TERMS if re.search(p, prompt_lower)]
    if len(imperfecciones_match) >= 2:
        bonificaciones.append("Micro-imperfecciones de piel y cabello descritas explícitamente")
    else:
        score -= 2.0
        penalizaciones.append("Faltan descripciones de imperfección dérmica (poros, vello fino, arrugas o asimetría) (-2.0 pts)")

    # 4. Chequeo de Iluminación física real
    iluminacion_match = [p for p in LIGHTING_TERMS if re.search(p, prompt_lower)]
    if len(iluminacion_match) >= 1:
        bonificaciones.append("Iluminación física realista definida")
    else:
        score -= 1.5
        penalizaciones.append("Iluminación genérica o ausente (-1.5 pts)")

    # Ajuste de rango 0 a 10
    score = max(0.0, min(10.0, score))
    
    # Clasificación DPO
    if score >= 9.0:
        clasificacion = "CHOSEN (Aprobado para Dataset de Oro)"
    elif score <= 6.5:
        clasificacion = "REJECTED (Candidato para Rechazado DPO)"
    else:
        clasificacion = "NEUTRAL (Requiere refinamiento)"

    return {
        "score": round(score, 1),
        "clasificacion": clasificacion,
        "penalizaciones": penalizaciones,
        "bonificaciones": bonificaciones
    }


if __name__ == "__main__":
    prompt_malo = "Hyperrealistic beautiful 25 year old woman smiling at the camera in a coffee shop, 8k resolution, photorealistic, masterpiece, perfect lighting, ultra detailed skin, bokeh background, octane render."
    
    prompt_bueno = "A candid 35mm film photograph of a 26-year-old woman taking a sip of iced coffee at an outdoor café table. Unposed, relaxed natural smile with slight squint. Visible skin micro-texture, natural pores on cheeks, fine flyaway strands of hair, peach fuzz along the jawline. Wearing a relaxed beige linen shirt. Shot on an 85mm lens at f/2.2, ISO 400 on Kodak Portra 400 film stock. Soft overcast ambient lighting with gentle shadow roll-off, unretouched aesthetic."

    print("--- EVALUACIÓN PROMPT MALO (TÍPICO IA) ---")
    res_malo = evaluar_prompt(prompt_malo)
    print(f"Puntuación: {res_malo['score']}/10 | Clasificación: {res_malo['clasificacion']}")
    for p in res_malo['penalizaciones']:
        print(f"  [X] {p}")

    print("\n--- EVALUACIÓN PROMPT BUENO (FOTOGRÁFICO REALISTA) ---")
    res_bueno = evaluar_prompt(prompt_bueno)
    print(f"Puntuación: {res_bueno['score']}/10 | Clasificación: {res_bueno['clasificacion']}")
    for b in res_bueno['bonificaciones']:
        print(f"  [+] {b}")
