"""
generador_prompt_nano_banana.py
Herramienta de consola para generar prompts de Nano Banana Pro al instante
aplicando las 7 capas fotográficas y evaluándolos con el Juez de Texto.
"""

import sys
import random
import re
from evaluador_juez_texto import evaluar_prompt

ESTILOS_FOTOGRAFICOS = [
    {
        "nombre": "Spot Publicitario Comercial High-End (Hasselblad / Arri Alexa - Presentador a Cámara)",
        "optica": "85mm commercial prime lens at f/2.8, 1/250s, ISO 100, Hasselblad medium format sensor, tack-sharp eye focus, clean optical falloff",
        "luz": "high-end commercial production lighting, large Profoto 5-foot softbox key light at 45 degrees, subtle clean edge rim light on shoulders, balanced 5600K daylight fill"
    },
    {
        "nombre": "Retrato Editorial Corporativo Moderno (Leica M11 / Oficina Arquitectónica)",
        "optica": "85mm prime lens at f/2.5, 1/500s, Leica M11 uncompressed RAW sensor, zero digital over-sharpening",
        "luz": "diffuse natural architectural window daylight mixed with balanced soft ambient fill, clean contemporary office atmosphere"
    },
    {
        "nombre": "Retrato Intimista con Luz Natural de Ventana (Kodak Portra 400)",
        "optica": "85mm portrait prime lens at f/2.0, ISO 400, Kodak Portra 400 film stock, authentic optical depth of field",
        "luz": "soft diffuse north-facing window light, gentle natural shadow roll-off beneath cheekbones and jawline"
    },
    {
        "nombre": "Retrato Editorial RAW Luz de Día Nublado (Leica M11)",
        "optica": "85mm prime lens stopped down to f/2.8, 1/500s, Leica M11 uncompressed RAW sensor, zero digital over-sharpening",
        "luz": "cool overcast afternoon daylight at 5600K, even shadowless illumination revealing genuine skin micro-texture"
    },
    {
        "nombre": "Candid Snapshot 35mm (Flash Directo - Estética 90s / Paparazzi)",
        "optica": "35mm compact point-and-shoot camera, f/4 aperture, 1/125s, ISO 400, fine organic film grain",
        "luz": "direct harsh on-camera flash casting a crisp dark drop-shadow on the wall behind, authentic specular highlights on forehead and nose bridge"
    }
]

MICRO_IMPERFECCIONES = [
    "genuine skin micro-texture with visible pores, natural hydration sheen on cheekbones, subtle fine expression lines around eyes, delicate stray hair strands, mouth closed in relaxed poised expression ready for speaking",
    "authentic skin pores on nose and cheeks, delicate peach fuzz along jawline, natural skin sheen, fine flyaway hair strands, relaxed confident neutral mouth posture",
    "unretouched commercial skin texture with authentic pores, faint smile creases around eyes, natural lip creases with closed lips, subtle asymmetrical realism",
    "clean professional skin micro-texture, authentic pores, natural skin specular reflections, crisp focus on eye iris, poised mouth closed in calm confidence"
]

DICCIONARIO_ES_EN = {
    "mujer": "woman",
    "chica": "young woman",
    "hombre": "man",
    "chico": "young man",
    "anciano": "elderly man",
    "anciana": "elderly woman",
    "niño": "boy",
    "niña": "girl",
    "de 20 años": "in her early 20s",
    "de 30 años": "in her 30s",
    "de 40 años": "in his 40s",
    "de 50 años": "in her 50s",
    "de 60 años": "in his 60s",
    "en un café": "at a coffee shop",
    "en la calle": "on a city street",
    "esperando el metro": "waiting at a subway station",
    "con audífonos": "wearing headphones",
    "en una fiesta": "at a party",
    "cocinando": "cooking in a kitchen"
}

def normalizar_idea_ingles(idea: str) -> str:
    idea_en = idea
    for es, en in DICCIONARIO_ES_EN.items():
        idea_en = re.sub(rf"\b{re.escape(es)}\b", en, idea_en, flags=re.IGNORECASE)
    return idea_en

def sintetizar_prompt(idea: str, estilo_idx: int = None) -> str:
    """Convierte una idea en un prompt maestro para Google Nano Banana Pro."""
    if estilo_idx is None or estilo_idx < 0 or estilo_idx >= len(ESTILOS_FOTOGRAFICOS):
        estilo = random.choice(ESTILOS_FOTOGRAFICOS)
    else:
        estilo = ESTILOS_FOTOGRAFICOS[estilo_idx]

    idea_adaptada = normalizar_idea_ingles(idea)
    imperfecciones = random.choice(MICRO_IMPERFECCIONES)

    prompt = (
        f"A candid, unposed photograph of a {idea_adaptada}. "
        f"{imperfecciones.capitalize()}. "
        f"Wearing textured clothing with authentic fabric weave and natural wrinkles. "
        f"{estilo['luz'].capitalize()}. "
        f"Shot on {estilo['optica']}. "
        f"Unretouched documentary aesthetic, authentic analog character, zero CGI rendering."
    )
    return prompt

def main():
    print("=" * 70)
    print("  GENERADOR DE PROMPTS HIPERREALISTAS PARA GOOGLE NANO BANANA PRO")
    print("=" * 70)

    if len(sys.argv) > 1:
        idea = " ".join(sys.argv[1:])
    else:
        idea = input("\nIngresa tu idea para la foto (ej: 'mujer de 30 años en un café'): ").strip()
        if not idea:
            idea = "Hombre de 35 años caminando por una calle lluviosa en la noche"

    print(f"\n[+] Procesando idea: '{idea}'...")
    prompt_generado = sintetizar_prompt(idea)

    print("\n" + "-" * 70)
    print("PROMPT MAESTRO PARA GOOGLE NANO BANANA PRO (Copia y pega esto):")
    print("-" * 70)
    print(prompt_generado)
    print("-" * 70)

    # Evaluación en vivo con el Juez 1
    evaluacion = evaluar_prompt(prompt_generado)
    print(f"\n[AUDITORÍA DEL JUEZ 1 (TEXTO)]")
    print(f"Puntuación de Realismo: {evaluacion['score']} / 10.0")
    print(f"Clasificación: {evaluacion['clasificacion']}")
    for b in evaluacion["bonificaciones"]:
        print(f"  [+] {b}")
    for p in evaluacion["penalizaciones"]:
        print(f"  [-] {p}")
    # Guardar en archivo y copiar al portapapeles
    with open("ultimo_prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt_generado)

    import subprocess
    try:
        subprocess.run(['powershell', '-Command', 'Set-Clipboard -Value (Get-Content "ultimo_prompt.txt" -Raw)'], check=True)
        print("\n[✓] ¡Prompt ancla copiado automáticamente al portapapeles de Windows!")
    except Exception:
        pass
    print("=" * 70)

if __name__ == "__main__":
    main()
