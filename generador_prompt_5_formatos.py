"""
generador_prompt_5_formatos.py
Generador interactivo para la suite de los 5 Formatos Maestros de Video Corto
(Google Nano Banana Pro + Google Veo 3.1).
Copia automáticamente el resultado al portapapeles de Windows.
"""

import sys
import subprocess
from generador_datasets_por_formato import (
    generar_par_talkinghead,
    generar_par_podcast,
    generar_par_ugc,
    generar_par_street,
    generar_par_product
)

FORMATOS = [
    ("1", "Presentador Comercial a Cámara (Corporate / B2B-B2C Talking Head)"),
    ("2", "Clip Viral de Podcast / Masterclass (Diary of a CEO - Ángulo 3/4 y Shure SM7B)"),
    ("3", "Testimonial UGC Orgánico (Creador en Primera Persona / TikTok Shop)"),
    ("4", "Entrevista Callejera Dinámica (Street Interview / Vox Pop)"),
    ("5", "Demostración de Producto con Hook Visual y B-Roll Narrativo")
]

def main():
    print("=" * 75)
    print("  SUITE DE 5 FORMATOS DE VIDEO CORTO (NANO BANANA PRO & VEO 3.1)")
    print("=" * 75)
    print("Selecciona el formato que deseas generar:\n")
    for num, nombre in FORMATOS:
        print(f"  [{num}] {nombre}")
    print("=" * 75)

    opcion = input("\nElige una opción (1-5) [Default 1]: ").strip() or "1"

    if opcion == "1":
        idea = input("Describe el sujeto / empresa (ej: 'Fundadora de SaaS'): ").strip() or "Fundadora SaaS B2B en oficina de cristal moderna"
        speech = input("Frase / Hook que dirá a cámara: ").strip() or "Tu equipo comercial pierde el treinta por ciento de los leads por responder tarde. Nosotros lo resolvemos en segundos."
        ancla, chosen, _ = generar_par_talkinghead(idea, speech)
        formato_nombre = "TALKING HEAD COMERCIAL"

    elif opcion == "2":
        idea = input("Describe al invitado / temática (ej: 'Fundador reflexionando'): ").strip() or "Fundador de startup tecnológica recordando sus inicios"
        speech = input("Frase íntima o lección de vida: ").strip() or "Tardé diez años en entender que el problema nunca fue el dinero. Era el miedo a fracasar en público."
        ancla, chosen, _ = generar_par_podcast(idea, speech)
        formato_nombre = "PODCAST 3/4 (DIARY OF A CEO)"

    elif opcion == "3":
        idea = input("Describe al creador / producto (ej: 'Serum anti-acné'): ").strip() or "Creadora recomendando serum facial para el acné"
        speech = input("Reacción / Frase coloquial de TikTok: ").strip() or "Ok, llevo dos semanas usando esto y mira mi piel… o sea, ¿qué? No lo puedo creer."
        ancla, chosen, _ = generar_par_ugc(idea, speech)
        formato_nombre = "UGC TESTIMONIAL ORGÁNICO"

    elif opcion == "4":
        idea = input("Contexto de la calle: ").strip() or "Joven profesional en calle peatonal concurrida"
        preg = input("Pregunta del entrevistador: ").strip() or "¿Qué harías si un robot te contesta el WhatsApp?"
        resp = input("Respuesta espontánea: ").strip() or "Mientras me conteste rápido… ¡mejor que mi ex!"
        ancla, chosen, _ = generar_par_street(idea, preg, resp)
        formato_nombre = "ENTREVISTA CALLEJERA (VOX POP)"

    elif opcion == "5":
        idea = input("Producto y superficie (ej: 'Smartwatch sobre grava volcánica'): ").strip() or "Estuche de auriculares inalámbricos negro mate sobre piedra húmeda"
        accion = input("Hook físico de los primeros 2s (ej: 'un splash de agua y apertura'): ").strip() or "un splash de agua en cámara lenta y apertura con clic magnético"
        ancla, chosen, _ = generar_par_product(idea, accion)
        formato_nombre = "DEMOSTRACIÓN DE PRODUCTO CON HOOK MACRO"
    else:
        print("Opción no válida.")
        return

    print("\n" + "=" * 75)
    print(f"  RESULTADO CALIBRADO: {formato_nombre}")
    print("=" * 75)
    print("\n[1] PROMPT ANCLA (Pégalo en Google Nano Banana Pro):")
    print("-" * 75)
    print(ancla)
    print("-" * 75)

    print("\n[2] PROMPT DE VIDEO (Pégalo en Google Veo 3.1):")
    print("-" * 75)
    print(chosen)
    print("-" * 75)

    # Guardar en archivo y copiar al portapapeles el ancla
    with open("ultimo_ancla_5formatos.txt", "w", encoding="utf-8") as f:
        f.write(ancla)
    with open("ultimo_video_5formatos.txt", "w", encoding="utf-8") as f:
        f.write(chosen)

    try:
        subprocess.run(['powershell', '-Command', 'Set-Clipboard -Value (Get-Content "ultimo_ancla_5formatos.txt" -Raw)'], check=True)
        print("\n[✓] ¡Prompt ancla de imagen copiado automáticamente al portapapeles de Windows!")
        print("    (Para copiar el de video, ejecuta: Get-Content ultimo_video_5formatos.txt | Set-Clipboard)")
    except Exception:
        pass
    print("=" * 75)

if __name__ == "__main__":
    main()
