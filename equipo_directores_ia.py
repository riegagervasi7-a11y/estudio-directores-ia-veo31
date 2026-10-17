"""
equipo_directores_ia.py
Sistema Multi-Agente de Producción de Video Corto (Nano Banana Pro & Veo 3.1).
Consta de un Director General (Router Inteligente) y 5 Subagentes Directores
Especializados con auto-auditoría forense, generación inteligente con Gemini 3.8 Flash
y cumplimiento estricto de las reglas anti-IA de Google Flow.
"""

import os
import sys
import json
import re
import subprocess
from typing import Dict, Any, Tuple

# Cargar API Key si existe en .env
GEMINI_KEY = ""
for p in [".env", os.path.join(r"c:\Users\Gabo\Documents\entrenamiento de ai", ".env"), os.path.join(r"C:\Users\Gabo\Documents\cerebro-hibrido-v2", ".env")]:
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        GEMINI_KEY = line.strip().split("=", 1)[1].strip()
                        break
        except Exception:
            pass
        if GEMINI_KEY:
            break

# ==============================================================================
# PROMPT SISTEMA FORENSE PARA GEMINI 3.8 FLASH
# ==============================================================================
SYSTEM_PROMPT_DIRECTOR = """Eres el Director de Fotografía y Prompt Engineer Forense para Nano Banana Pro (Imagen 3) y Google Veo 3.1 en Google Flow.
Tu misión es recibir una idea y un texto de voz/diálogo, y redactar DOS prompts en inglés cinematográfico y forense, adaptados con precisión al tema del usuario.

REGLAS OBLIGATORIAS:
1. prompt_ancla (Para generar el fotograma ancla en Nano Banana Pro, 9:16 vertical):
   - Escribe como un FOTÓGRAFO EN SET, nunca como un ilustrador.
   - PROHIBIDO terminantemente usar palabras cliché de IA: cinematic, photorealistic, hyperrealistic, 8k, 4k, masterpiece, ultra detailed, sharp focus, crisp, stunning, octane.
   - Nombra la cámara y lente física según el formato seleccionado:
     * talkinghead: 50mm f/2.8 en sensor full-frame, plano medio pecho (MCU), luz suave difusa a 45 grados, fondo reconocible con bokeh sutil f/2.8.
     * podcast: 85mm prime f/1.8 en ángulo 3/4 (35 grados fuera de eje), micrófono Shure SM7B negro en brazo articulado a 10cm de la boca sin taparla, short lighting 5:1.
     * ugc: cámara frontal de smartphone 24mm a distancia de brazo, profundidad de campo amplia, micro-temblor de mano, luz natural de ventana.
     * street: 28mm f/5.6 callejero documental, micrófono de mano con flag sólida sostenido por el entrevistador apuntando a la boca, transeúntes desenfocados.
     * product: 100mm macro f/4, ángulo heroico 20 grados, luces de recorte duras de 5600K, microtextura física y sombras de contacto reales.
   - Adapta el sujeto, vestuario y entorno exactamente a la idea del usuario (no impongas oficinas ni trajes a menos que la idea lo pida).
   - Describe piel humana real con poros visibles, microtextura y asimetría natural.
   - IMPORTANTE: La boca del sujeto debe estar relajada y completamente cerrada con labios sellados (frame 0 de reposo).
   - Frase de cierre negativa obligatoria al final del ancla: "No studio equipment visible, no text, no logos, no watermarks, no plastic skin, no HDR glow, no distorted fingers."

2. prompt_video (Para animar con Veo 3.1 en modo Image-to-Video / Frames to Video):
   - Inicia SIEMPRE con: "Maintain the exact subject, wardrobe, and environment from the first frame. No morphing, no added objects."
   - No vuelvas a describir ropa ni rasgos físicos (ya viven en el ancla).
   - Estructura obligatoria en 3 bloques en este orden exacto:
     CAMERA: [Movimiento de cámara con inercia física real (dolly tracking, push-in, o cámara en mano según el formato)].
     SUBJECT: [Acción sencilla a velocidad humana real. Si habla o gesticula, describe micro-sacadas oculares, parpadeos naturales, sutil elevación de cejas y labios cerrando en pausas. NUNCA transcribas el diálogo como audio de Veo].
     ENVIRONMENT: [Entorno en positivo con iluminación constante idéntica al ancla].
   - Audio obligatorio al final: "Audio: quiet room tone only, no music, no voices." (La locución se maneja con ElevenLabs y lip-sync en postproducción).
   - Duración obligatoria al final: "Duration: 8 seconds."

Responde ÚNICAMENTE en JSON válido con esta estructura:
{
  "formato_elegido": "talkinghead | podcast | ugc | street | product",
  "director": "Nombre descriptivo del director",
  "prompt_ancla": "...",
  "prompt_video": "..."
}"""

# ==============================================================================
# SUBAGENTES FALLBACK (En caso de no haber conexión o API)
# ==============================================================================
class SubagenteTalkingHead:
    nombre = "Director de Presentadores Comerciales (Talking Head)"
    def generar(self, idea: str, speech: str = "") -> Tuple[str, str]:
        ancla = (
            f"Vertical 9:16 medium close-up portrait shot on 50mm f/2.8 lens. {idea}. "
            f"Facing camera directly at eye level with calm, attentive engagement. "
            f"Mouth gently closed, lips relaxed and completely sealed, neutral expression. "
            f"Soft key lighting positioned at 45 degrees, balanced with subtle ambient fill. "
            f"Natural human skin with visible pores, fine texture, zero retouching. "
            f"No studio equipment visible, no text, no logos, no watermarks, no plastic skin, no HDR glow, no distorted fingers."
        )
        video = (
            f"Maintain the exact subject, wardrobe, and environment from the first frame. No morphing, no added objects.\n"
            f"CAMERA: Locked-off 50mm medium close-up at eye level with a slow, steady push-in of 4% over 8 seconds and slight natural operator inertia.\n"
            f"SUBJECT: Speaks directly to the viewer with calm confidence. Eyebrows lift subtly on emphasis, natural micro-saccades, blinks naturally at phrase pauses, lips close fully on pauses.\n"
            f"ENVIRONMENT: Consistent background depth and constant soft directional lighting matching the initial frame without shifting reflections.\n"
            f"Audio: quiet room tone only, no music, no voices.\nDuration: 8 seconds."
        )
        return ancla, video

class SubagentePodcast:
    nombre = "Director de Podcast & Storytelling (3/4 Profile)"
    def generar(self, idea: str, speech: str = "") -> Tuple[str, str]:
        ancla = (
            f"Vertical 9:16 tight medium shot on 85mm prime lens at f/1.8. {idea}. "
            f"Seen in three-quarter profile, looking 35 degrees off-axis toward an off-camera interviewer. "
            f"Mouth closed, lips sealed, reflective listening expression. "
            f"A black Shure SM7B dynamic microphone on an articulated boom arm enters from lower camera side, positioned 10 cm from mouth without covering lips. "
            f"Short lighting from far side of face with warm practical ambient bokeh in background. "
            f"Natural skin micro-texture, visible pores. No studio equipment visible, no text, no logos, no watermarks, no plastic skin, no HDR glow, no distorted fingers."
        )
        video = (
            f"Maintain the exact subject, wardrobe, microphone position, and environment from the first frame. No morphing, no added objects. The microphone remains completely stable and never merges with the face.\n"
            f"CAMERA: Tripod-locked 85mm three-quarter profile with an extremely subtle 5% push-in starting at second 4.\n"
            f"SUBJECT: The speaker maintains eye line with the off-camera interviewer, breathing naturally with thoughtful micro-expressions, gentle brow articulation, and periodic natural blinks.\n"
            f"ENVIRONMENT: Intimate studio atmosphere, constant warm rim lighting, unchanging soft background shadows.\n"
            f"Audio: quiet room tone only, no music, no voices.\nDuration: 8 seconds."
        )
        return ancla, video

class SubagenteUGC:
    nombre = "Director de UGC & Creadores (Handheld Selfie)"
    def generar(self, idea: str, speech: str = "") -> Tuple[str, str]:
        ancla = (
            f"Vertical 9:16 authentic smartphone front-camera perspective, 24mm wide angle with deep focus. {idea}. "
            f"Held at arm's length, slightly above eye level. Soft natural directional window daylight. "
            f"Natural creator looking toward the phone camera, mouth closed, lips relaxed and sealed. "
            f"Real unedited skin texture with visible pores and natural complexion. "
            f"No studio equipment visible, no text, no logos, no watermarks, no plastic skin, no HDR glow, no distorted fingers."
        )
        video = (
            f"Maintain the exact subject, wardrobe, and environment from the first frame. No morphing, no added objects.\n"
            f"CAMERA: Handheld smartphone selfie at arm's length, 24mm perspective, continuous subtle organic micro-jitter from hand holding phone with natural arm inertia.\n"
            f"SUBJECT: Speaks casually toward camera with energetic conversational pacing, expressive eyebrow lifts, frequent natural blinks, and relaxed lip closures during speech pauses.\n"
            f"ENVIRONMENT: Lived-in interior space with unchanging natural window daylight throughout.\n"
            f"Audio: quiet room tone only, no music, no voices.\nDuration: 8 seconds."
        )
        return ancla, video

class SubagenteStreet:
    nombre = "Director de Entrevista Callejera (Vox Pop)"
    def generar(self, idea: str, speech: str = "") -> Tuple[str, str]:
        ancla = (
            f"Vertical 9:16 documentary street interview shot on 28mm lens at f/5.6. {idea}. "
            f"Subject looks 15 degrees off-axis toward an interviewer. "
            f"From lower edge, an interviewer's hand holds a clean black dynamic microphone with a solid flag pointed at subject's mouth 15 cm away. "
            f"Mouth closed, lips sealed, curious engaging expression. Pedestrians softly blurred in background. "
            f"Natural daylight with warm ambient fill. No studio equipment visible, no text, no logos, no watermarks, no plastic skin, no HDR glow, no distorted fingers."
        )
        video = (
            f"Maintain the exact subject, wardrobe, microphone, and street setting from the first frame. No morphing, no added objects.\n"
            f"CAMERA: Documentary handheld 28mm at eye level with organic operator breathing sway and gentle inertial reframing.\n"
            f"SUBJECT: The subject reacts with expressive curiosity, eyebrows lifting in surprise, gesturing naturally with free hand, lips closing cleanly at speech pauses.\n"
            f"ENVIRONMENT: Open pedestrian street environment with consistent daylight and natural background movement.\n"
            f"Audio: quiet room tone only, no music, no voices.\nDuration: 8 seconds."
        )
        return ancla, video

class SubagenteProduct:
    nombre = "Director de Demostración de Producto & Macro"
    def generar(self, idea: str, speech: str = "") -> Tuple[str, str]:
        ancla = (
            f"Vertical 9:16 macro product hero shot on 100mm macro lens at f/4. {idea}. "
            f"Low 20-degree heroic angle, razor-thin focal plane on front detailing, background falling into soft dark depth. "
            f"Dual 5600K hard strip rim lights tracing contours with subtle colored accent glow. "
            f"Physically accurate surface textures, seam lines, and specular highlights. "
            f"No studio equipment visible, no text, no logos, no watermarks, no plastic skin, no HDR glow, no distorted fingers."
        )
        video = (
            f"Maintain the exact product shape, proportions, materials, and lighting from the first frame. No morphing, no duplication.\n"
            f"CAMERA: 100mm macro on a motorized slider performing a smooth, continuous 15-degree orbital pan with steady mechanical inertia.\n"
            f"SUBJECT: An anatomically correct hand enters frame with five distinct fingers, interacting with the product with realistic physical contact shadows and damped motion.\n"
            f"ENVIRONMENT: Minimalist tabletop set with unchanging rim highlights and consistent specular reflections.\n"
            f"Audio: quiet room tone only, no music, no voices.\nDuration: 8 seconds."
        )
        return ancla, video

# ==============================================================================
# DIRECTOR GENERAL (Router Inteligente)
# ==============================================================================
class DirectorGeneralRouter:
    def __init__(self):
        self.agentes = {
            "talkinghead": SubagenteTalkingHead(),
            "podcast": SubagentePodcast(),
            "ugc": SubagenteUGC(),
            "street": SubagenteStreet(),
            "product": SubagenteProduct()
        }

    def enrutar(self, peticion_usuario: str) -> str:
        p = peticion_usuario.lower()
        if any(k in p for k in ["podcast", "shure", "sm7b", "entrevista estudio", "diary", "conversacion", "leccion de vida"]):
            return "podcast"
        elif any(k in p for k in ["ugc", "selfie", "celular", "tiktok shop", "creador", "probando", "recomiendo", "reseña", "unboxing"]):
            return "ugc"
        elif any(k in p for k in ["calle", "street", "vox pop", "transeunte", "microfono de mano", "pregunta calle"]):
            return "street"
        elif any(k in p for k in ["producto", "macro", "splash", "reloj", "perfume", "audifono", "botella"]):
            return "product"
        else:
            return "talkinghead"

    def procesar(self, idea_usuario: str, speech_usuario: str = "", formato_forzado: str = None) -> Dict[str, Any]:
        formato = formato_forzado if (formato_forzado and formato_forzado in self.agentes) else self.enrutar(idea_usuario)

        # 1. Intentar generación inteligente con Gemini 3.8 Flash si hay API Key
        if GEMINI_KEY:
            try:
                from google import genai
                client = genai.Client(api_key=GEMINI_KEY)
                prompt_input = (
                    f"Idea: {idea_usuario}\n"
                    f"Speech/Diálogo: {speech_usuario}\n"
                    f"Formato forzado: {formato}"
                )
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=SYSTEM_PROMPT_DIRECTOR + "\n\n" + prompt_input,
                    config={"response_mime_type": "application/json"}
                )
                data = json.loads(response.text)
                if "prompt_ancla" in data and "prompt_video" in data:
                    return {
                        "formato_elegido": data.get("formato_elegido", formato),
                        "director": data.get("director", self.agentes[formato].nombre),
                        "prompt_ancla": data["prompt_ancla"].strip(),
                        "prompt_video": data["prompt_video"].strip()
                    }
            except Exception as e:
                print(f"[Aviso] Gemini Fallback: {e}")

        # 2. Fallback local si no hay API Key o falla
        agente = self.agentes.get(formato, self.agentes["talkinghead"])
        ancla, video = agente.generar(idea_usuario, speech_usuario)
        return {
            "formato_elegido": formato,
            "director": agente.nombre,
            "prompt_ancla": ancla,
            "prompt_video": video
        }

# ==============================================================================
# CLI PRINCIPAL
# ==============================================================================
def main():
    router = DirectorGeneralRouter()

    print("=" * 75)
    print("  ESTUDIO MULTI-AGENTE: 5 DIRECTORES ESPECIALIZADOS DE VIDEO CORTO")
    print("=" * 75)
    print("Ingresa tu idea libremente. El Director General enrutará automáticamente")
    print("hacia el Subagente especialista, o puedes forzar un formato específico.\n")
    print("  [0] Auto-Detectar según mi idea (Recomendado)")
    print("  [1] Forzar Subagente Talking Head Comercial")
    print("  [2] Forzar Subagente Podcast 3/4 (Diary of a CEO)")
    print("  [3] Forzar Subagente UGC Testimonial (TikTok Creator)")
    print("  [4] Forzar Subagente Entrevista Callejera (Vox Pop)")
    print("  [5] Forzar Subagente Demostración Producto Macro")
    print("=" * 75)

    opc = input("\nElige una opción (0-5) [Default 0]: ").strip() or "0"
    mapa_opc = {"1": "talkinghead", "2": "podcast", "3": "ugc", "4": "street", "5": "product"}
    formato_forzado = mapa_opc.get(opc, None)

    idea = input("\nDescribe la idea del video: ").strip()
    if not idea:
        idea = "Experto en finanzas compartiendo el error más común que comete la gente con su dinero"

    speech = input("Frase o diálogo clave (Opcional, presiona Enter para usar sugerido): ").strip()

    resultado = router.procesar(idea, speech, formato_forzado)

    print("\n" + "=" * 75)
    print(f"  [ROUTER] Enrutado con éxito a: {resultado['director']}")
    print("=" * 75)

    print("\n[1] PROMPT ANCLA (Google Nano Banana Pro):")
    print("-" * 75)
    print(resultado["prompt_ancla"])
    print("-" * 75)

    print("\n[2] PROMPT DE VIDEO (Google Veo 3.1):")
    print("-" * 75)
    print(resultado["prompt_video"])
    print("-" * 75)

if __name__ == "__main__":
    main()
