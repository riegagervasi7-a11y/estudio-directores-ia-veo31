"""
equipo_directores_ia.py
Sistema Multi-Agente de Producción de Video Corto (Nano Banana Pro & Veo 3.1).
Consta de un Director General (Router Inteligente) y 5 Subagentes Directores
Especializados con auto-auditoría forense y copiado al portapapeles.
"""

import sys
import re
import random
import subprocess
from typing import Dict, Any, Tuple

# ==============================================================================
# SUBAGENTE 1: TALKING HEAD COMERCIAL (Corporate & Ads)
# ==============================================================================
class SubagenteTalkingHead:
    def __init__(self):
        self.nombre = "Director de Presentadores Comerciales (Talking Head)"
        self.focal = "50mm full-frame lens at f/2.8"
        self.encuadre = "MCU (mid-chest framing), eye level, frontal to the axis"
        self.iluminacion = "Large soft box key light at 45 degrees off-camera (5600K), gentle fill (-1.5 stops), faint rim light on hair, warm 3200K practical background lamps"

    def generar(self, idea: str, speech: str = "") -> Tuple[str, str]:
        if not speech:
            speech = "Tu equipo comercial pierde el treinta por ciento de los leads por responder tarde. Nosotros lo resolvemos en segundos."

        ancla = (
            f"Photorealistic medium close-up portrait of an articulate professional presenter for: {idea}. "
            f"Facing camera directly at eye level, looking straight into the lens with a calm, attentive expression. "
            f"Mouth gently closed, lips relaxed and sealed, neutral corners, zero smile, no teeth visible. "
            f"Shot on {self.focal}: background softly defocused modern architectural glass atrium with warm practical ambient lamps. "
            f"{self.iluminacion}. "
            f"Natural skin texture with visible pores, fine vellus hair, zero plastic retouching, tailored professional blazer over plain shirt. "
            f"9:16 vertical, no visible studio equipment, no text, no watermarks."
        )

        video = (
            f"Maintain the exact presenter, facial geometry, tailored blazer, and glass office background from the first frame. No morphing, no added objects.\n\n"
            f"CAMERA: Locked-off 50mm medium close-up, eye level, frontal to the axis, with a slow, steady push-in of about 4% over the full 8 seconds and barely perceptible handheld breathing drift. Background stays softly defocused and readable. No cuts, no zoom jumps.\n\n"
            f"SUBJECT: She speaks directly to the lens with warm, confident authority: \"{speech}\" Her eyebrows lift subtly on key emphasis words and again, softer, on the final benefit. Natural micro-saccades between the viewer's eyes; blinks naturally three times at phrase pauses. Lips fully close on every p, b, and m. At midpoint, her right hand rises briefly at chest height with open palm, then lowers out of frame. Ends with lips softly closed and slight genuine composure. Zero stiffness, zero frozen forehead.\n\n"
            f"ENVIRONMENT: Modern glass office atrium, soft 45-degree key light, warm practical lamps glowing in background, calm professional atmosphere.\n\n"
            f"Audio: clear close-mic'd vocal audio in neutral Spanish, quiet office room tone, faint HVAC hum, no music, no subtitles."
        )
        return ancla, video

# ==============================================================================
# SUBAGENTE 2: PODCAST / MASTERCLASS 3/4 (Storytelling & Authority)
# ==============================================================================
class SubagentePodcast:
    def __init__(self):
        self.nombre = "Director de Podcast & Storytelling (3/4 Profile)"
        self.focal = "85mm prime lens at f/1.8 (creamy bokeh)"
        self.encuadre = "Tight MCU / close-up at collarbone, three-quarter profile (35 degrees off-axis)"

    def generar(self, idea: str, speech: str = "") -> Tuple[str, str]:
        if not speech:
            speech = "Tardé diez años en entender que el problema nunca fue el dinero. Era el miedo a fracasar en público."

        ancla = (
            f"Photorealistic cinematic podcast still. A thoughtful, articulate speaker for: {idea}. "
            f"Seen in three-quarter profile, camera positioned 35 degrees off eyeline, looking off-camera toward an unseen interviewer with lead room in that direction. "
            f"Mouth gently closed, lips relaxed and sealed, contemplative expression with slight corrugator tension between brows. "
            f"A black Shure SM7B dynamic microphone on an articulated boom arm enters from lower camera side, positioned 10 cm from mouth, angled toward it without covering lips. "
            f"Shot on {self.focal}: dark studio background with warm 2700K Edison practical bulbs in creamy bokeh, faint cool accent light. "
            f"Short lighting: large soft key from far side of face, near side falling into gentle shadow (5:1 ratio). "
            f"Natural skin micro-texture, visible pores, charcoal crewneck sweater, elbows resting on dark wooden table. 9:16 vertical, no text, no logos."
        )

        video = (
            f"Maintain the exact person, sweater, the SM7B microphone and boom arm position, lighting ratio and dark bokeh background from the first frame. The microphone never moves, never merges with the face, and never covers the mouth.\n\n"
            f"CAMERA: Tripod-locked 85mm three-quarter profile, shallow depth of field, completely stable, with an extremely slow push-in of about 6% starting at second 4. No cuts, no handheld shake.\n\n"
            f"SUBJECT: The speaker never looks at the camera. First glances down and slightly away (15 degrees) recalling a memory, brows gently knitted, then takes a visible breath and lifts eyes back to the off-camera interviewer to deliver slowly: \"{speech}\" Inner brows lift softly on key emotional words; a long slow blink (300ms) in the reflective pause. Lips close fully on b, m, and p. Left hand turns slowly palm-up on the table. Ends with lips sealed, holding eye contact with the interviewer.\n\n"
            f"ENVIRONMENT: Intimate dark podcast studio, warm Edison practicals in creamy bokeh, quiet late-night atmosphere.\n\n"
            f"Audio: warm, intimate, close-mic'd broadcast-quality voice with dynamic microphone proximity effect, low studio room tone, no music, no subtitles."
        )
        return ancla, video

# ==============================================================================
# SUBAGENTE 3: UGC TESTIMONIAL ORGÁNICO (TikTok / Creator)
# ==============================================================================
class SubagenteUGC:
    def __init__(self):
        self.nombre = "Director de UGC & Creadores (Handheld Selfie)"
        self.focal = "24mm smartphone front-camera perspective (deep focus)"
        self.encuadre = "Arm's length selfie perspective, camera 5-10 degrees above eye level"

    def generar(self, idea: str, speech: str = "") -> Tuple[str, str]:
        if not speech:
            speech = "Ok, llevo dos semanas usando esto y mira mi piel… o sea, ¿qué? No lo puedo creer."

        ancla = (
            f"Authentic smartphone front-camera selfie, vertical 9:16. A relatable natural creator filming at arm's length: {idea}. "
            f"Wide-angle 24mm smartphone perspective, deep depth of field with lived-in room details in focus behind. "
            f"Soft natural window daylight from side, realistic phone-camera color balance. "
            f"Holds small product packaging in free hand near cheek, label facing camera and crisp. Eyes look slightly below lens at screen. "
            f"Mouth closed, lips relaxed and sealed. Real unedited skin with visible pores, minor blemishes, no beauty filter. Slight sensor grain. Zero logos."
        )

        video = (
            f"Maintain the exact creator, casual attire, room background, natural window light and product packaging from the first frame. The product never morphs or changes proportions.\n\n"
            f"CAMERA: Handheld smartphone selfie at arm's length, 24mm front-camera perspective, deep focus throughout. Continuous organic micro-jitter from hand holding phone, one small natural reframe when bringing product closer, brief focus hunting as product nears lens. No gimbal smoothness.\n\n"
            f"SUBJECT: Talks fast and casually, mostly watching own screen just below the lens, but snaps direct eye contact to the lens on the punchline: \"{speech}\" Begins with skeptical frown, then eyebrows shoot up asymmetrically on emphasis. Tilts head, briefly glances down at product while rotating it toward camera, then back. Frequent natural blinks; short genuine laugh at the end. Free hand moves product naturally.\n\n"
            f"ENVIRONMENT: Lived-in interior with natural window daylight, casual morning atmosphere.\n\n"
            f"Audio: phone-microphone recording of natural upbeat voice, slight room acoustic reverb, faint background street noise, no music, no subtitles."
        )
        return ancla, video

# ==============================================================================
# SUBAGENTE 4: ENTREVISTA CALLEJERA (Street Interview / Vox Pop)
# ==============================================================================
class SubagenteStreet:
    def __init__(self):
        self.nombre = "Director de Entrevista Callejera (Vox Pop)"
        self.focal = "28mm wide-angle lens at f/5.6 (readable street depth)"
        self.encuadre = "Handheld medium shot, 15-25 degrees off-axis from interviewer"

    def generar(self, idea: str, speech: str = "") -> Tuple[str, str]:
        pregunta = "¿Qué harías si un robot te contesta el WhatsApp?"
        respuesta = speech or "Mientras me conteste rápido… ¡mejor que mi ex!"

        ancla = (
            f"Photorealistic street interview still, vertical 9:16. A friendly authentic person on a busy pedestrian shopping street: {idea}. "
            f"Looking just to the side of the camera at an off-frame interviewer. "
            f"From bottom-left edge, the interviewer's hand holds a black handheld dynamic microphone with a plain solid mic flag cube (no text), its capsule pointed at subject's mouth 15 cm away, mouth fully visible. "
            f"Mouth closed, lips relaxed and sealed, curious listening expression, eyebrows slightly raised. "
            f"Shot on 28mm lens at f/5.6: storefronts and softly blurred pedestrians readable behind. Warm low sun creating rim light on hair. Natural skin texture, pores, documentary handheld feel. Zero logos."
        )

        video = (
            f"Maintain the exact subject, wardrobe, the mic flag, microphone and interviewer's hand position, golden-hour light and street background from the first frame. The microphone stays firmly pointed at the subject's mouth.\n\n"
            f"CAMERA: Documentary handheld 28mm at eye level, natural operator body sway and small inertial reframes; no cuts, no gimbal smoothness. Background pedestrians walk naturally with consistent shapes.\n\n"
            f"SUBJECT: First, off-screen interviewer asks: \"{pregunta}\" During question the subject listens with lips sealed, eyebrows popping up in surprise, then glances up-lateral for one second, thinking. Laughs briefly and answers to the interviewer, not the camera: \"{respuesta}\" Gestures loosely with free hand, then shoots one quick playful glance into lens at the end. Only one person speaks at a time; lips close fully on m and p.\n\n"
            f"ENVIRONMENT: Lively pedestrian shopping street at golden hour, warm backlight, soft-focus passersby, urban street energy.\n\n"
            f"Audio: two distinct voices captured by handheld dynamic mic — off-screen interviewer's question, then subject's laughing answer in Spanish; street ambience with footsteps and city murmur, no music, no subtitles."
        )
        return ancla, video

# ==============================================================================
# SUBAGENTE 5: PRODUCTO MACRO & B-ROLL NARRATIVO
# ==============================================================================
class SubagenteProduct:
    def __init__(self):
        self.nombre = "Director de Demostración de Producto & Macro"
        self.focal = "100mm macro lens at f/4 (razor-thin depth of field)"
        self.encuadre = "Heroic 20-degree low angle or 90-degree top-down"

    def generar(self, idea: str, speech: str = "") -> Tuple[str, str]:
        hook_action = speech or "a heavy water droplet splashes onto the surface in slow-motion, followed by a damped mechanical opening"

        ancla = (
            f"Photorealistic premium product macro shot, vertical 9:16: {idea}. "
            f"Shot from a low heroic angle of 20 degrees with a 100mm macro lens at f/4: razor-thin focus on product's front edge, background falling into deep darkness. "
            f"Dramatic lighting: two hard 5600K strip rim lights from left and right tracing contours, subtle brand accent glow from behind, crisp specular highlights on surface textures. "
            f"Physically accurate micro-surface texture, precise seam line, clean luxury commercial look. Zero text, zero extra objects, zero watermarks."
        )

        video = (
            f"Maintain the exact product shape, size, matte finish, seam lines and materials from the first frame. It never morphs, duplicates or changes proportions. Keep rim lighting and accent glow exactly.\n\n"
            f"CAMERA: 100mm macro on a motorized slider: extreme slow-motion opening for the first 2 seconds, then smooth speed ramp to real time as camera performs a slow 20-degree orbit and push-in. One gentle rack focus across the surface. Perfectly stable, no shake, no cuts.\n\n"
            f"SUBJECT: Hook: in slow motion, {hook_action}. A realistic hand with five well-proportioned fingers enters frame from right, pressing and interacting with damped physical resistance. Contact shadows and fingertip pressure look physically real. Zero distortion of product dimensions.\n\n"
            f"ENVIRONMENT: Dark premium tabletop set, hard rim lights, colored accent glow, minimalist luxury mood.\n\n"
            f"Audio: crisp amplified impact sound, satisfying mechanical click, deep low-frequency whoosh during speed ramp, no voice, no music, no subtitles."
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
        elif any(k in p for k in ["ugc", "selfie", "celular", "tiktok shop", "creador", "probando", "recomiendo", "reseña"]):
            return "ugc"
        elif any(k in p for k in ["calle", "street", "vox pop", "transeunte", "microfono de mano", "pregunta calle"]):
            return "street"
        elif any(k in p for k in ["producto", "macro", "splash", "unboxing", "reloj", "perfume", "audifono", "botella"]):
            return "product"
        else:
            # Por defecto: Talking Head Comercial
            return "talkinghead"

    def procesar(self, idea_usuario: str, speech_usuario: str = "", formato_forzado: str = None) -> Dict[str, Any]:
        formato = formato_forzado if formato_forzado in self.agentes else self.enrutar(idea_usuario)
        agente = self.agentes[formato]

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

    # Guardar en archivo y copiar al portapapeles el ancla
    with open("ultimo_ancla_multiagente.txt", "w", encoding="utf-8") as f:
        f.write(resultado["prompt_ancla"])
    with open("ultimo_video_multiagente.txt", "w", encoding="utf-8") as f:
        f.write(resultado["prompt_video"])

    try:
        subprocess.run(['powershell', '-Command', 'Set-Clipboard -Value (Get-Content "ultimo_ancla_multiagente.txt" -Raw)'], check=True)
        print("\n[✓] ¡Prompt ancla copiado automáticamente al portapapeles de Windows!")
        print("    (Para el video, ejecuta: Get-Content ultimo_video_multiagente.txt | Set-Clipboard)")
    except Exception:
        pass
    print("=" * 75)

if __name__ == "__main__":
    main()
