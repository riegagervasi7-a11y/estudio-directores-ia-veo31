"""
juez_claude.py
Conecta con la API de Anthropic (Claude 3.5 Sonnet / Claude 3.7 Sonnet)
para auditar prompts e inspeccionar imágenes generadas por Google Nano Banana Pro.
"""

import os
import sys
import base64
import json
from typing import Dict, Any

def obtener_cliente_claude():
    try:
        import anthropic
    except ImportError:
        print("[!] La librería 'anthropic' no está instalada. Instalando...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "anthropic"])
        import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n[!] ERROR: No se encontró la variable de entorno 'ANTHROPIC_API_KEY'.")
        print("Para configurarla temporalmente en PowerShell escribe:")
        print('$env:ANTHROPIC_API_KEY = "tu-clave-aqui"')
        return None

    return anthropic.Anthropic(api_key=api_key)

def claude_auditar_prompt(prompt_a_evaluar: str) -> str:
    """Envía el prompt a Claude para que lo audite con rigor fotográfico."""
    client = obtener_cliente_claude()
    if not client:
        return "Falta configurar ANTHROPIC_API_KEY."

    sistema = (
        "Eres un director de fotografía analógica y perito en detección de arte generado por IA. "
        "Tu misión es evaluar el siguiente prompt diseñado para Google Nano Banana Pro. "
        "Determina si el prompt garantiza una fotografía 100% hiperrealista o si provocará defectos de IA "
        "(piel de cera, iluminación plástica, poses falsas). Califica de 1 a 10 y da tu crítica técnica."
    )

    mensaje = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=600,
        system=sistema,
        messages=[
            {"role": "user", "content": f"Audita este prompt:\n\n{prompt_a_evaluar}"}
        ]
    )
    return mensaje.content[0].text

def claude_auditar_imagen(ruta_imagen: str) -> str:
    """Envía una imagen a Claude Vision para una inspección visual forense de aspecto IA."""
    client = obtener_cliente_claude()
    if not client:
        return "Falta configurar ANTHROPIC_API_KEY."

    if not os.path.exists(ruta_imagen):
        return f"No se encontró el archivo de imagen: {ruta_imagen}"

    # Leer imagen y codificar en base64
    extension = ruta_imagen.split(".")[-1].lower()
    media_type = "image/jpeg" if extension in ["jpg", "jpeg"] else "image/png"

    with open(ruta_imagen, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    sistema = (
        "Actúa como un perito forense de imágenes. Inspecciona esta imagen generada por IA para detectar "
        "cualquier aspecto sintético: textura plástica de la piel, incoherencias en catchlights de los ojos, "
        "bordes de cabello, aberraciones en manos y fidelidad óptica. Di con honestidad si pasaría como foto real ante humanos."
    )

    mensaje = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=800,
        system=sistema,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": img_b64
                        }
                    },
                    {
                        "type": "text",
                        "text": "Analiza esta fotografía generada por Google Nano Banana Pro. ¿Parece una foto 100% real o tiene aspecto de IA? Detalla tus hallazgos."
                    }
                ]
            }
        ]
    )
    return mensaje.content[0].text

if __name__ == "__main__":
    prompt_prueba = (
        "A candid point-and-shoot direct on-camera flash photograph of a 28-year-old woman "
        "laughing mid-conversation in a dim hallway. Harsh direct flash creates authentic specular highlights "
        "on her forehead and nose bridge, casting a sharp dark shadow on the textured wall behind her. "
        "Natural skin sheen in T-zone, visible skin pores on cheeks, fine flyaway strands of hair. "
        "Wearing an oversized vintage leather jacket. Shot on a 35mm compact camera, f/4 aperture, "
        "ISO 400, fine organic film noise, authentic snapshot aesthetic, zero CGI."
    )

    print("=== PROBANDO CONEXIÓN CON CLAUDE COMO JUEZ DE TEXTO ===")
    resultado = claude_auditar_prompt(prompt_prueba)
    print(resultado)
