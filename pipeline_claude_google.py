"""
pipeline_claude_google.py
Orquestador del flujo entre Claude Code, el Generador de Prompts y Google Nano Banana Pro.

Uso desde Claude Code:
  python pipeline_claude_google.py --idea "anciano artesano tallando madera"
"""

import os
import sys
import argparse
import json
from generador_prompt_nano_banana import sintetizar_prompt
from evaluador_juez_texto import evaluar_prompt

def ejecutar_paso_generar_prompt(idea: str):
    print(f"\n[PASO 1] Claude Code propone la idea: '{idea}'")
    
    # Sintetizar prompt con nuestro modelo/pipeline de 7 capas
    prompt_maestro = sintetizar_prompt(idea)
    
    # Auditar con Juez 1
    evaluacion = evaluar_prompt(prompt_maestro)
    
    # Guardar en archivo para que Claude Code y Google puedan leerlo
    with open("ultimo_prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt_maestro)
        
    print(f"[PASO 2] Prompt maestro anti-IA generado y guardado en 'ultimo_prompt.txt'")
    print(f"       -> Calificación del Juez de Texto: {evaluacion['score']}/10 ({evaluacion['clasificacion']})")
    return prompt_maestro

def ejecutar_paso_google_render(prompt: str, api_key: str = None):
    print("\n[PASO 3] Enviando prompt a Google (Nano Banana Pro / Imagen)...")
    
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("[!] No se detectó GEMINI_API_KEY en las variables de entorno.")
        print("    -> El prompt quedó listo en 'ultimo_prompt.txt'.")
        print("    -> Si usas Google AI Studio / Google Flow web, pega 'ultimo_prompt.txt' y guarda la imagen como 'ultima_imagen.png'.")
        return None

    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        # Llamada al motor de imagen de Google
        resultado = client.models.generate_images(
            model="imagen-3.0-generate-002", # o nano-banana-pro según tu acceso
            prompt=prompt,
            config=dict(
                number_of_images=1,
                aspect_ratio="1:1"
            )
        )
        
        for i, imagen in enumerate(resultado.generated_images):
            with open("ultima_imagen.png", "wb") as f:
                f.write(imagen.image.image_bytes)
        print("✅ Imagen generada por Google y guardada como 'ultima_imagen.png'.")
        return "ultima_imagen.png"
    except Exception as e:
        print(f"[!] Error al llamar a la API de Google: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Orquestador Claude Code + Google")
    parser.add_argument("--idea", type=str, default="Anciano relojero suizo de 68 años reparando un mecanismo con lupa de ojo", help="Idea propuesta por Claude")
    args = parser.parse_args()

    prompt = ejecutar_paso_generar_prompt(args.idea)
    print("\n--- PROMPT GENERADO ---")
    print(prompt)
    print("------------------------")
    
    ruta_img = ejecutar_paso_google_render(prompt)
    
    print("\n[PASO 4] Instrucciones para Claude Code:")
    print("1. Claude Code debe leer 'ultima_imagen.png' con su herramienta de visión.")
    print("2. Debe auditar la piel, los ojos, las manos y el grano fotográfico.")
    print("3. Debe redactar su crítica forense final en la sesión.")

if __name__ == "__main__":
    main()
