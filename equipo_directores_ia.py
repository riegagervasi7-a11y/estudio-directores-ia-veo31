"""
equipo_directores_ia.py
Sistema Multi-Agente de Producción de Video Corto (Nano Banana Pro & Veo 3.1).
Consta de un Director General (Router Inteligente) y 5 Subagentes Directores
Especializados con auto-auditoría forense, generación inteligente con Gemini 3.8 Flash,
cumplimiento de las reglas anti-IA y estética REAL de Instagram Reels y TikTok (Mobile First).
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
# PROMPT SISTEMA FORENSE PARA GEMINI 3.8 FLASH (ESTÉTICA SOCIAL REELS / TIKTOK)
# ==============================================================================
SYSTEM_PROMPT_DIRECTOR = """Eres el Director de Contenido y Prompt Engineer Forense especializado en Instagram Reels y TikTok de alta conversión para marcas modernas (Benchmark: Swiss Office Business Club, B2B Creators).
Trabajas con Google Nano Banana Pro (Imagen 3) y Google Veo 3.1 en Google Flow.

⚠️ REGLA DE ORO: ELIMINAR EL SESGO DE "SUPERPRODUCCIÓN / PELÍCULA DE HOLLYWOOD"
La mayor delación de que un video es IA es que parece una película dramática de cine con sombras oscuras, contrastes teatrales, bokeh extremo de f/1.2, lámparas incandescentes flotando en la penumbra, atrios colosales vacíos de ciencia ficción y personas con cara de póquer rígidas y serias.
Los videos REALES de Instagram y TikTok son frescos, luminosos, acogedores, humanos y grabados con tecnología móvil de alta gama (iPhone 15/16 Pro o Sony FX3 / A7IV a 28-35mm).

REGLAS OBLIGATORIAS:
1. prompt_ancla (Para generar el fotograma ancla en Nano Banana Pro, 9:16 vertical):
   - DISPOSITIVO & ÓPTICA: Captura en sensor móvil 4K / mirrorless moderna con lente 28mm o 35mm f/3.5-f/4. Profundidad de campo amplia y nítida donde el entorno se reconoce con claridad (NO desenfoque borroso irreal).
   - ILUMINACIÓN REAL: Luz comercial limpia, diáfana, clara y acogedora. Paneles LED de techo empotrados (4000K blanco neutro) combinados con abundante luz natural diurna de ventanales. Cero sombras dramáticas de cine negro, cero contraluces de fantasía, cero lámparas amarillas en la oscuridad.
   - EXPRESIÓN & ACTITUD HUMANA: Sonrisa genuina y cálida (Duchenne smile con arruguitas en los ojos), actitud de bienvenida, expresión cercana y accesible. Cabeza con micro-inclinación natural, hombros relajados (postura humana normal, no rígida militar).
   - VESTUARIO CONTEMPORÁNEO (Smart Casual): Ropa de negocios moderna: blazer ligero desestructurado (beige, crema, azul claro o gris suave) sobre una playera básica limpia de algodón o blusa fresca sin rigidez.
   - ESPACIO TANGIBLE Y VIVO: Oficinas y espacios reales donde vive gente: mostrador de recepción en madera o mármol, macetas con plantas verdes (monstera, ficus), salas de cristal con sillas ergonómicas, laptops, tazas de café. Espacio real, no una nave espacial vacía.
   - COMPOSICIÓN: Si el formato o la toma requiere espacio para gráficos o UI, posicionar a la persona en el tercio izquierdo o derecho dejando el tercio opuesto despejado.
   - BOCA & PIEL: Piel real con poros visibles, micro-brillo natural en zona T, boca en reposo relajada con labios suaves y sellados para el frame 0.
   - Cierre negativo obligatorio: "No studio lighting equipment visible, no softbox, no light stands, no moody dark shadows, no dramatic theatrical contrast, no orange-and-teal grading, no text, no logos, no watermarks, no plastic airbrushed skin, no distorted hands."

2. prompt_video (Para animar con Veo 3.1 en modo Image-to-Video / Frames to Video):
   - Inicia SIEMPRE con: "Maintain the exact subject, friendly welcoming presence, wardrobe, and environment from the first frame. No morphing, no added objects."
   - Estructura obligatoria en 3 bloques en este orden exacto:
     CAMERA: [Movimiento de cámara móvil dinámico y fluido (walk-and-talk en gimbal o cámara en mano estabilizada a la altura de los ojos, ritmo de paso natural acompañando a la persona por el espacio)].
     SUBJECT: [La persona camina hacia adelante con energía y paso relajado, sonriendo de forma cercana y cálida al espectador. Gestos naturales y abiertos con una mano como mostrando el espacio o explicando una idea con empatía. Pestañeo humano, movimientos suaves de cabeza y cejas comunicativas. NUNCA transcribir el texto como audio sonoro].
     ENVIRONMENT: [Entorno de oficina/coworking moderno, luminoso y vivo, con plantas interiores y luz natural constante sin parpadeo].
   - Audio obligatorio al final: "Audio: quiet room tone only, no music, no voices." (La voz maestra la provee ElevenLabs en postproducción).
   - Duración obligatoria: "Duration: 8 seconds."

Responde ÚNICAMENTE en JSON válido con esta estructura:
{
  "formato_elegido": "talkinghead | podcast | ugc | street | product",
  "director": "Nombre descriptivo del director (Enfoque Social Reels / TikTok)",
  "prompt_ancla": "...",
  "prompt_video": "..."
}"""

# ==============================================================================
# SUBAGENTES FALLBACK SOCIAL FIRST (En caso de no haber conexión o API)
# ==============================================================================
class SubagenteTalkingHead:
    nombre = "Director de Contenido B2B & Reels Comerciales (Social First)"
    def generar(self, idea: str, speech: str = "") -> Tuple[str, str]:
        ancla = (
            f"Vertical 9:16 authentic commercial Instagram reel still shot on a 28mm wide-angle lens on a 4K mobile sensor. {idea}. "
            f"A warm, friendly, and approachable professional with a genuine welcoming smile and expressive eyes, positioned naturally in the left third of the frame. "
            f"Wearing a modern smart-casual beige tailored blazer over a crisp white tee. "
            f"Mouth relaxed with lips gently closed in a welcoming smile. Natural skin texture with visible pores and authentic daylight sheen. "
            f"Environment is a bright, upscale, well-lit modern workspace with an open wooden reception counter, lush indoor green plants (monstera), and clean glass partitions softly visible in readable background depth. "
            f"Abundant natural daytime window light blended with clean overhead 4000K commercial LED panels, creating a bright, airy, and inviting atmosphere without dark moody shadows. "
            f"No studio lighting equipment visible, no softbox, no light stands, no moody dark shadows, no dramatic theatrical contrast, no text, no logos, no watermarks, no plastic skin."
        )
        video = (
            f"Maintain the exact subject, friendly welcoming presence, wardrobe, and environment from the first frame. No morphing, no added objects.\n"
            f"CAMERA: Smooth handheld gimbal walk-and-talk tracking shot moving backward at an even, natural walking pace, maintaining eye-level framing and keeping the subject on the left third with the right third clear.\n"
            f"SUBJECT: The presenter walks forward through the bright office at a confident, relaxed pace, smiling warmly and engaging directly with the viewer. Natural open hand gestures explaining ideas warmly, organic blinks, friendly head tilts, and lively communicative facial expression.\n"
            f"ENVIRONMENT: Bright, airy modern office interior with reception desk and green foliage drifting past smoothly, consistent bright commercial ambient lighting throughout.\n"
            f"Audio: quiet room tone only, no music, no voices.\nDuration: 8 seconds."
        )
        return ancla, video

class SubagentePodcast:
    nombre = "Director de Podcast & Conversaciones de Autoridad (Reels 3/4)"
    def generar(self, idea: str, speech: str = "") -> Tuple[str, str]:
        ancla = (
            f"Vertical 9:16 crisp social media podcast clip still, 35mm lens perspective on 4K sensor. {idea}. "
            f"Three-quarter angle, subject engaged in an authentic thoughtful conversation looking 30 degrees off-camera. "
            f"A matte black Shure SM7B dynamic microphone on a clean low-profile arm sits 10 cm from the mouth without obscuring the face. "
            f"Warm, clean studio ambient lighting with readable acoustic wood slat wall and subtle warm practical shelf lighting behind. "
            f"Natural human skin with pores and realistic texture, casual stylish knit crewneck sweater, approachable authentic presence. "
            f"No studio lighting equipment visible, no softbox, no moody noir shadows, no plastic skin, no watermarks."
        )
        video = (
            f"Maintain the exact subject, wardrobe, microphone position, and environment from the first frame. No morphing, no added objects.\n"
            f"CAMERA: Stable eye-level tripod shot with a very gentle 4% slow push-in feeling like a clean YouTube/Instagram podcast clip.\n"
            f"SUBJECT: The speaker talks to the off-camera host with authentic emotional cadence, natural head nodding, brow articulation, thoughtful micro-pauses, and natural blinks.\n"
            f"ENVIRONMENT: Cozy, contemporary podcast studio with steady acoustic wood paneling and warm ambient background glow.\n"
            f"Audio: quiet room tone only, no music, no voices.\nDuration: 8 seconds."
        )
        return ancla, video

class SubagenteUGC:
    nombre = "Director de UGC & Creadores (TikTok / Reels Nativo)"
    def generar(self, idea: str, speech: str = "") -> Tuple[str, str]:
        ancla = (
            f"Vertical 9:16 authentic iPhone 15 front-camera selfie perspective, 24mm wide angle with deep focus. {idea}. "
            f"Held casually at arm's length, slightly above eye level. Natural daylight coming from a nearby window. "
            f"A vibrant, expressive creator looking straight into the front lens with an energetic, relatable, warm smile. "
            f"Authentic unedited skin texture with natural skin details, wearing casual trendy streetwear. "
            f"Real lived-in modern apartment or workspace background with authentic room depth. "
            f"No studio equipment, no softbox, no professional lighting rigs, no plastic beauty filter, no watermarks."
        )
        video = (
            f"Maintain the exact creator, casual styling, natural window light, and room from the first frame. No morphing, no added objects.\n"
            f"CAMERA: Casual handheld smartphone selfie at arm's length with subtle organic micro-wobbles and human hand inertia.\n"
            f"SUBJECT: Speaks fast, enthusiastically and naturally directly into the lens, showing subtle head bobs, expressive eyebrow lifts, genuine smiles, and animated gestures.\n"
            f"ENVIRONMENT: Real room interior with unchanging natural daylight throughout the clip.\n"
            f"Audio: quiet room tone only, no music, no voices.\nDuration: 8 seconds."
        )
        return ancla, video

class SubagenteStreet:
    nombre = "Director de Entrevistas Callejeras (Vox Pop Social)"
    def generar(self, idea: str, speech: str = "") -> Tuple[str, str]:
        ancla = (
            f"Vertical 9:16 mobile street interview shot on 28mm smartphone perspective. {idea}. "
            f"Subject stands on a clean modern pedestrian promenade, looking casually toward an interviewer. "
            f"A black handheld dynamic mic with a clean square cube flag is held by an interviewer's hand near the subject's chest level. "
            f"Authentic bright daytime natural outdoor light, genuine candid expression with a friendly curious smile. "
            f"Real city storefronts and passersby naturally visible in background. No studio equipment, no artificial HDR glow."
        )
        video = (
            f"Maintain the exact subject, clothing, microphone, and street setting from the first frame. No morphing, no added objects.\n"
            f"CAMERA: Documentary handheld mobile camera at eye level with gentle natural operator body sway.\n"
            f"SUBJECT: Reacts with genuine amusement, laughing warmly, gesticulating casually with hands, natural eye contact alternating between interviewer and camera.\n"
            f"ENVIRONMENT: Bustling daytime pedestrian street with natural daylight and continuous realistic city movement.\n"
            f"Audio: quiet room tone only, no music, no voices.\nDuration: 8 seconds."
        )
        return ancla, video

class SubagenteProduct:
    nombre = "Director de Producto Social (Reels Unboxing & Demo)"
    def generar(self, idea: str, speech: str = "") -> Tuple[str, str]:
        ancla = (
            f"Vertical 9:16 crisp modern product video still shot on 50mm macro lens on 4K sensor. {idea}. "
            f"Clean, bright, modern tabletop aesthetic with soft diffused daylight and warm wood or stone surface. "
            f"Product is sharply in focus showing tactile authentic texture and clean premium packaging. "
            f"Contemporary lifestyle setting with a green indoor plant and coffee cup in background. "
            f"No dark dramatic movie shadows, no sci-fi neon lights, no plastic CGI textures."
        )
        video = (
            f"Maintain the exact product shape, texture, materials, and bright tabletop lighting from the first frame. No morphing.\n"
            f"CAMERA: Smooth, bright overhead sliding push-in with gentle natural momentum.\n"
            f"SUBJECT: A clean, natural hand enters the frame, interacting realistically with the product, picking it up or opening it with authentic physical resistance.\n"
            f"ENVIRONMENT: Bright contemporary lifestyle workspace with consistent daylight illumination.\n"
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

        # 1. Intentar generación inteligente con Gemini 3.8 Flash con el System Prompt Social First
        if GEMINI_KEY:
            try:
                from google import genai
                client = genai.Client(api_key=GEMINI_KEY)
                prompt_input = (
                    f"Idea / Escena: {idea_usuario}\n"
                    f"Speech / Locución: {speech_usuario}\n"
                    f"Formato forzado: {formato}\n\n"
                    f"Asegúrate de aplicar la estética fresca y real de Instagram Reels/TikTok (Luz natural brillante, sonrisas cálidas, oficinas vivas con plantas y madera, sin película dramática ni superproducción de Hollywood)."
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

        # 2. Fallback local Social First si no hay API Key o falla
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
    print("  ESTUDIO MULTI-AGENTE: 5 DIRECTORES ESPECIALIZADOS DE VIDEO CORTO (REELS / TIKTOK)")
    print("=" * 75)
    print("Ingresa tu idea libremente. El Director General enrutará automáticamente")
    print("hacia el Subagente especialista con estética social auténtica (Social Realism).\n")
    print("  [0] Auto-Detectar según mi idea (Recomendado)")
    print("  [1] Forzar Subagente Talking Head Comercial (Social Reels / Tour)")
    print("  [2] Forzar Subagente Podcast 3/4 (Reels Conversación)")
    print("  [3] Forzar Subagente UGC Testimonial (TikTok Creator Nativo)")
    print("  [4] Forzar Subagente Entrevista Callejera (Vox Pop)")
    print("  [5] Forzar Subagente Demostración Producto Lifestyle")
    print("=" * 75)

    opc = input("\nElige una opción (0-5) [Default 0]: ").strip() or "0"
    mapa_opc = {"1": "talkinghead", "2": "podcast", "3": "ugc", "4": "street", "5": "product"}
    formato_forzado = mapa_opc.get(opc, None)

    idea = input("\nDescribe la idea del video: ").strip()
    if not idea:
        idea = "Una oficina de coworking premium que te hace sentir bien recibido desde que llegas, mostrando la recepción y un equipo atento"

    speech = input("Frase o diálogo clave (Opcional, presiona Enter para usar sugerido): ").strip()

    resultado = router.procesar(idea, speech, formato_forzado)

    print("\n" + "=" * 75)
    print(f"  [ROUTER] Enrutado con éxito a: {resultado['director']}")
    print("=" * 75)

    print("\n[1] PROMPT ANCLA (Nano Banana Pro / Imagen 3):")
    print("-" * 75)
    print(resultado["prompt_ancla"])
    print("-" * 75)

    print("\n[2] PROMPT DE VIDEO (Google Veo 3.1):")
    print("-" * 75)
    print(resultado["prompt_video"])
    print("-" * 75)

if __name__ == "__main__":
    main()
