"""
generador_prompt_video_veo.py
Generador local de prompts para Video (Veo 3.1 & Higgsfield) en Google Flow.
Aplica la arquitectura de 3 bloques (CÁMARA + SUJETO + ENTORNO + AUDIO)
y audita el resultado con el Juez de Video.
"""

import sys
import random
import re
import subprocess
from evaluador_juez_video import evaluar_prompt_video

MOVIMIENTOS_CAMARA_PRESETS = [
    ("Slow, subtle push-in on an 85mm prime lens with natural handheld camera breath and gentle physical inertia.", "No fast pans, no digital zoom."),
    ("Gentle lateral tracking from left to right on a smooth dolly track at chest height.", "Steady cinematic motion, zero camera roll."),
    ("Steady tripod shot with subtle organic vibration, locked horizon and constant focal length.", "Natural operator breath."),
    ("Slow micro push-in on a 50mm lens, keeping intimate eye-level documentary framing.", "Gentle physical inertia."),
    ("Static lock-off shot with faint human operator breathing motion, grounded framing.", "Zero artificial stabilization jitter.")
]

def sintetizar_prompt_video(ancla: str, accion: str) -> str:
    es_comercial = any(k in (ancla + " " + accion).lower() for k in ["habla", "presentador", "avatar", "spot", "comercial", "camara", "cámara", "speaks"])
    
    if es_comercial:
        cam = "Static commercial lock-off shot with faint organic operator breathing motion on an 85mm prime lens at eye level. Perfect horizon, zero camera shake, high-end commercial tripod stability."
        cam_restriccion = "No fast pans, no digital zoom."
        accion_final = (
            f"The presenter speaks directly to the camera with rich, natural, and expressive facial articulation: {accion}. "
            f"Active upper-face dynamics: eyebrows lift naturally and modulate with vocal inflections to emphasize key points, subtle expressive forehead engagement. "
            f"Lively, engaged eyes with authentic ocular micro-saccades, blinking naturally at second 2 and second 5, subtle warm crinkling at the outer corners during confident delivery. "
            f"Organic jaw movement with clean articulation, subtle head tilts complementing cadence, relaxed neck. "
            f"Zero stiffness, zero mask-like frozen forehead, no exaggerated hand gestures, no morphing, no facial distortion."
        )
        audio = "natural ambient room tone and clean studio acoustics, subtle presenter presence, no music, no spoken dialogue."
    else:
        cam, cam_restriccion = random.choice(MOVIMIENTOS_CAMARA_PRESETS)
        accion_final = (
            f"The subject performs the intended action with natural human cadence: {accion}. "
            f"At second 2, a natural blink and subtle breath, micro-movements only, realistic weight transfer. "
            f"No fast hand gestures, no morphing, no facial distortion."
        )
        audio = "natural ambient room tone and environmental background sound, no music, no spoken dialogue."

    prompt = (
        f"Maintain the exact subject, facial identity, wardrobe, and environment from the first frame.\n\n"
        f"CAMERA: {cam} {cam_restriccion}\n\n"
        f"SUBJECT: {accion_final}\n\n"
        f"ENVIRONMENT: Studio and ambient lighting remain completely constant throughout the shot. Continuous atmospheric coherence.\n\n"
        f"Audio: {audio}"
    )
    return prompt

def main():
    print("=" * 70)
    print("  GENERADOR DE PROMPTS DE VIDEO VEO 3.1 / HIGGSFIELD (GOOGLE FLOW)")
    print("=" * 70)

    if len(sys.argv) > 2:
        ancla = sys.argv[1]
        accion = " ".join(sys.argv[2:])
    else:
        print("\nEjemplo de uso:")
        print("  python generador_prompt_video_veo.py \"Pescador en el muelle\" \"Exhala vapor y mira al horizonte\"\n")
        ancla = input("Describe el ancla (ej. 'Pescador en el muelle'): ").strip() or "Pescador en un muelle bajo llovizna"
        accion = input("¿Qué acción debe hacer? (ej. 'Exhala vaho y parpadea'): ").strip() or "Exhala vaho frío y gira la mirada lentamente hacia el mar"

    prompt_veo = sintetizar_prompt_video(ancla, accion)

    print("\n" + "-" * 70)
    print("PROMPT MAESTRO PARA VEO 3.1 EN GOOGLE FLOW:")
    print("-" * 70)
    print(prompt_veo)
    print("-" * 70)

    # Auditar con Juez de Video
    evaluacion = evaluar_prompt_video(prompt_veo)
    print(f"\n[AUDITORÍA DEL JUEZ DE VIDEO]")
    print(f"Puntuación: {evaluacion['score']} / 10.0 | Clasificación: {evaluacion['clasificacion']}")
    for b in evaluacion["bonificaciones"]:
        print(f"  [+] {b}")
    for p in evaluacion["penalizaciones"]:
        print(f"  [-] {p}")

    # Guardar en archivo y copiar al portapapeles
    with open("ultimo_prompt_video.txt", "w", encoding="utf-8") as f:
        f.write(prompt_veo)

    try:
        subprocess.run(['powershell', '-Command', 'Set-Clipboard -Value (Get-Content "ultimo_prompt_video.txt" -Raw)'], check=True)
        print("\n[✓] ¡Prompt de video copiado automáticamente al portapapeles de Windows!")
    except Exception:
        pass
    print("=" * 70)

if __name__ == "__main__":
    main()
