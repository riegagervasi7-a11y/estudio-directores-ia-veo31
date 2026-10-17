"""
generador_datasets_por_formato.py
Generador automatizado de Datasets DPO y SFT especializados para cada uno
de los 5 Formatos Maestros de Video Corto (Veo 3.1 & Nano Banana Pro).

Aplica la estrategia de "Aislar una sola variable por par DPO":
- Formato 1: Cejas activas vs Frente congelada / Boca abierta.
- Formato 2: Mirada off-camera al entrevistador vs Mirada al lente / Micrófono fusionado.
- Formato 3: Jitter orgánico y mirada a pantalla vs Gimbal rígido y mirada fija.
- Formato 4: Turnos de habla y cápsula orientada vs Voces solapadas y mic flotante.
- Formato 5: Integridad geométrica y física de fluidos vs Mutación de producto.
"""

import json
import random

# ==============================================================================
# FORMATO 1: TALKING HEAD COMERCIAL
# ==============================================================================
TALKING_HEAD_IDEAS = [
    ("Fundadora SaaS B2B en oficina de cristal moderna", "Tu equipo comercial pierde el treinta por ciento de los leads por responder tarde. Nosotros lo resolvemos en segundos."),
    ("Consultor financiero en atrio corporativo elegante", "Guardar tu dinero en una cuenta de ahorros tradicional te está costando diez por ciento anual en poder adquisitivo."),
    ("Directora de ciberseguridad en espacio arquitectónico", "El noventa por ciento de los ciberataques a empresas entran por un correo electrónico que parecía legítimo."),
    ("Emprendedor de logística en sede corporativa limpia", "Reducir tus tiempos de entrega a la mitad no requiere más camiones, sino mejor automatización de rutas."),
    ("Especialista en IA corporativa en estudio contemporáneo", "Las empresas que integren flujos autónomos este año multiplicarán por cuatro su margen operativo.")
]

def generar_par_talkinghead(idea, speech):
    ancla = (
        f"Photorealistic medium close-up portrait of an articulate professional presenter at eye level, "
        f"facing the camera directly and looking straight into the lens with a calm, attentive expression. "
        f"Mouth gently closed, lips relaxed and sealed, neutral corners, no smile, no teeth visible. "
        f"Shot on a full-frame camera with a 50mm lens at f/2.8: background softly defocused but readable modern glass-walled office atrium. "
        f"Key light: large soft box at 45 degrees off-camera, 5600K, subtle fill, faint hair rim light. "
        f"Natural skin texture with visible pores, no plastic retouching. Clean tailored blazer over white shirt. 9:16 vertical, zero text, zero watermarks."
    )
    chosen = (
        f"Maintain the exact presenter, facial geometry, tailored blazer, and glass office atrium from the first frame. No morphing, no added objects.\n\n"
        f"CAMERA: Locked-off 50mm medium close-up, eye level, frontal to the axis, with a slow, steady push-in of about 4% over the full 8 seconds and barely perceptible handheld breathing drift. Background stays softly defocused and readable. No cuts, no zoom jumps.\n\n"
        f"SUBJECT: She speaks directly to the lens with warm, confident authority: \"{speech}\" Her eyebrows lift subtly on the first key statistic and again, softer, on the final benefit. Natural micro-saccades between the viewer's eyes; blinks naturally three times at phrase pauses. Lips fully close on every p, b, and m. At midpoint, her right hand rises briefly at chest height with open palm, then lowers out of frame. Ends with lips softly closed and slight genuine composure.\n\n"
        f"ENVIRONMENT: Modern glass office atrium, soft 45-degree key light, warm practical lamps glowing in background, calm professional atmosphere.\n\n"
        f"Audio: clear close-mic'd vocal audio in neutral Spanish, quiet office room tone, faint HVAC hum, no music, no subtitles."
    )
    rejected = (
        f"Maintain the presenter from first frame. "
        f"CAMERA: Fast digital zoom in. "
        f"SUBJECT: She speaks with completely frozen unmoving eyebrows, rigid fixed stare, micro-movements only, marionette jaw movement with stiff face, grinning smile with open teeth from the start. Both hands waving fast. "
        f"ENVIRONMENT: Studio lighting. Audio: voice."
    )
    return ancla, chosen, rejected

# ==============================================================================
# FORMATO 2: PODCAST CLIP / 3/4 STORYTELLING
# ==============================================================================
PODCAST_IDEAS = [
    ("Fundador de startup tecnológica recordando sus inicios", "Tardé diez años en entender que el problema nunca fue el dinero. Era el miedo a fracasar en público."),
    ("Autor bestseller analizando hábitos de alto rendimiento", "La disciplina no es levantarse a las cinco de la mañana. Es aprender a decir que no a las cosas buenas."),
    ("Inversor veterano compartiendo su peor lección", "El peor error de mi carrera fue pensar que el éxito pasado garantizaba el resultado futuro."),
    ("Psicólogo clínico hablando de agotamiento profesional", "El agotamiento no viene de trabajar demasiado, sino de pasar demasiado tiempo haciendo lo que no tiene sentido."),
    ("Director creativo explicando la obsesión por la calidad", "Cuando amas lo que haces, los detalles que nadie más nota son los únicos que de verdad te importan.")
]

def generar_par_podcast(idea, speech):
    ancla = (
        f"Photorealistic cinematic podcast still. A thoughtful professional in their 40s seen in a three-quarter profile, camera positioned 35 degrees off eyeline. "
        f"Looks off-camera toward an unseen interviewer on the opposite side, leaving lead room in that direction. Mouth gently closed, lips relaxed and sealed, contemplative expression. "
        f"A black Shure SM7B dynamic microphone on an articulated boom arm enters from lower camera side, positioned 10 cm from mouth, angled toward it without covering lips. "
        f"Shot on an 85mm lens at f/1.8: creamy bokeh, dark studio background with warm 2700K Edison bulbs as soft orbs. Short lighting: large soft key from far side, near side in gentle shadow 5:1 ratio. "
        f"Natural skin texture, pores, charcoal crewneck sweater, elbows on dark wooden table. 9:16 vertical, no text, no logos."
    )
    chosen = (
        f"Maintain the exact person, sweater, the SM7B microphone and boom arm position, lighting ratio and dark bokeh background from the first frame. The microphone never moves, never merges with the face, and never covers the mouth.\n\n"
        f"CAMERA: Tripod-locked 85mm three-quarter profile, shallow depth of field, completely stable, with an extremely slow push-in of about 6% starting at second 4. No cuts, no handheld shake.\n\n"
        f"SUBJECT: The speaker never looks at the camera. First glances down and slightly away, recalling a memory, brows gently knitted, then takes a visible breath and lifts eyes back to the off-camera interviewer to deliver: \"{speech}\" Inner brows lift softly on key emotional words; a long slow blink in the pause. Lips close fully on b, m, and p. Left hand turns slowly palm-up on the table. Ends with lips sealed, holding eye contact with interviewer.\n\n"
        f"ENVIRONMENT: Intimate dark podcast studio, warm Edison practicals in creamy bokeh, quiet late-night atmosphere.\n\n"
        f"Audio: warm, intimate, close-mic'd broadcast-quality voice with dynamic microphone proximity effect, low studio room tone, no music, no subtitles."
    )
    rejected = (
        f"Maintain the speaker. "
        f"CAMERA: Fast camera rotation. "
        f"SUBJECT: The speaker stares directly into the camera lens with wide open eyes, laughing and smiling brightly, microphone shifts and covers the mouth, hand touching the microphone capsule. "
        f"ENVIRONMENT: Flat bright office background. Audio: voice."
    )
    return ancla, chosen, rejected

# ==============================================================================
# FORMATO 3: TESTIMONIAL UGC ORGÁNICO
# ==============================================================================
UGC_IDEAS = [
    ("Creadora recomendando serum facial para el acné", "Ok, llevo dos semanas usando esto y mira mi piel… o sea, ¿qué? No lo puedo creer."),
    ("Joven mostrando app de productividad y finanzas", "Llevaba meses intentando ahorrar y esta tontería fue lo único que me funcionó de verdad."),
    ("Creador mostrando audífonos inalámbricos con cancelación", "Si trabajas en un café ruidoso necesitas esto ya mismo. Es literalmente magia."),
    ("Chica recomendando suplemento de magnesio para dormir", "Mi nivel de energía cambió por completo en cinco días. No vuelvo a comprar otra marca."),
    ("Emprendedor mostrando teclado ergonómico mecánico", "Mis dolores de muñeca desaparecieron después de una semana programando con esto.")
]

def generar_par_ugc(idea, speech):
    ancla = (
        f"Authentic smartphone front-camera selfie, vertical 9:16. A natural relatable creator filming at arm's length from slightly above eye level in a lived-in bedroom. "
        f"Wide-angle 24mm smartphone perspective, deep depth of field with unmade bed and room details in focus behind. Soft natural window light from side, realistic phone-camera color balance. "
        f"Holds a small product bottle in free hand near cheek, label facing camera and crisp. Eyes look slightly below lens at screen. Mouth closed, lips relaxed and sealed. "
        f"Real skin with visible pores, minor blemishes, no beauty filter. Slight smartphone sensor noise. Zero watermarks."
    )
    chosen = (
        f"Maintain the exact creator, casual hoodie, bedroom background, natural window light and product packaging from the first frame. The product never morphs or changes proportions.\n\n"
        f"CAMERA: Handheld smartphone selfie at arm's length, 24mm front-camera perspective, deep focus throughout. Continuous organic micro-jitter from hand holding phone, one small natural reframe when bringing product closer, brief focus hunting as product nears lens. No gimbal smoothness.\n\n"
        f"SUBJECT: Talks fast and casually, mostly watching own screen just below the lens, but snaps direct eye contact to the lens on the punchline: \"{speech}\" Begins with skeptical frown, then eyebrows shoot up asymmetrically on emphasis. Tilts head, briefly glances down at product while rotating it toward camera, then back. Frequent natural blinks; short genuine laugh at the end. Free hand moves product naturally.\n\n"
        f"ENVIRONMENT: Lived-in bedroom with natural daylight, casual morning atmosphere.\n\n"
        f"Audio: phone-microphone recording of natural upbeat voice, slight room acoustic reverb, faint background street noise, no music, no subtitles."
    )
    rejected = (
        f"Maintain creator. "
        f"CAMERA: Perfectly stabilized smooth gimbal tracking, cinematic f/1.4 blur. "
        f"SUBJECT: Actor stares rigidly into camera lens with porcelain airbrushed skin, product label blurs and transforms into alien text, formal teleprompter voice delivery. "
        f"ENVIRONMENT: Studio 3-point lighting. Audio: studio voice."
    )
    return ancla, chosen, rejected

# ==============================================================================
# FORMATO 4: ENTREVISTA CALLEJERA (STREET INTERVIEW / VOX POP)
# ==============================================================================
STREET_IDEAS = [
    ("Joven profesional en calle peatonal concurrida", "¿Qué harías si un robot te contesta el WhatsApp?", "Mientras me conteste rápido… ¡mejor que mi ex!"),
    ("Estudiante universitario frente a cafetería urbana", "¿Cuánto dinero consideras que es suficiente para ser feliz?", "El suficiente para no tener que mirar los precios en el supermercado."),
    ("Turista en avenida comercial de compras", "¿Qué le dirías a tu versión de hace diez años?", "Que compre Bitcoin y no se preocupe tanto por el qué dirán."),
    ("Empresario casual en distrito financiero", "¿Cuál es el peor consejo de dinero que te han dado?", "Que compres casa propia a los veinte años con deuda bancaria."),
    ("Chica con café caminando por un parque", "¿Qué habilidad consideras imprescindible hoy en día?", "Aprender a adaptarse rápido y comunicarse con claridad.")
]

def generar_par_street(idea, pregunta, respuesta):
    ancla = (
        f"Photorealistic street interview still, vertical 9:16. A friendly person stands on a busy pedestrian shopping street at golden hour, looking just to the side of the camera at an off-frame interviewer. "
        f"From bottom-left edge, the interviewer's hand holds a black handheld dynamic microphone with a plain solid mic flag cube (no text), its capsule pointed at the subject's mouth 15 cm away, mouth fully visible. "
        f"Mouth closed, lips relaxed and sealed, curious listening expression, eyebrows slightly raised. Shot on 28mm lens at f/5.6: storefronts and softly blurred pedestrians readable behind. "
        f"Warm low sun behind creating rim light on hair. Natural skin texture, pores, documentary handheld feel. Zero logos, zero watermarks."
    )
    chosen = (
        f"Maintain the exact subject, wardrobe, the mic flag, microphone and interviewer's hand position, golden-hour light and street background from the first frame. The microphone stays firmly pointed at the subject's mouth.\n\n"
        f"CAMERA: Documentary handheld 28mm at eye level, natural operator body sway and small inertial reframes; no cuts, no gimbal smoothness. Background pedestrians walk naturally with consistent shapes.\n\n"
        f"SUBJECT: First, off-screen interviewer asks: \"{pregunta}\" During question the subject listens with lips sealed, eyebrows popping up in surprise, then glances up-lateral for one second, thinking. Laughs briefly and answers to the interviewer, not the camera: \"{respuesta}\" Gestures loosely with free hand, then shoots one quick playful glance into lens at the end. Only one person speaks at a time; lips close fully on m and p.\n\n"
        f"ENVIRONMENT: Lively pedestrian shopping street at golden hour, warm backlight, soft-focus passersby, urban street energy.\n\n"
        f"Audio: two distinct voices captured by handheld dynamic mic — off-screen interviewer's question, then subject's laughing answer in Spanish; street ambience with footsteps and city murmur, no music, no subtitles."
    )
    rejected = (
        f"Maintain subject. "
        f"CAMERA: Tripod locked static shot. "
        f"SUBJECT: Both interviewer and subject speak at the same time with voice overlap, microphone is pointed at the camera instead of the mouth, subject stares unblinkingly at the lens like a commercial, crowd morphs in background. "
        f"ENVIRONMENT: Artificial studio lights on street. Audio: music."
    )
    return ancla, chosen, rejected

# ==============================================================================
# FORMATO 5: DEMOSTRACIÓN DE PRODUCTO CON HOOK MACRO
# ==============================================================================
PRODUCT_IDEAS = [
    ("Estuche de auriculares inalámbricos negro mate sobre piedra húmeda", "un splash de agua en cámara lenta y apertura con clic magnético"),
    ("Botella de perfume de cristal tallado sobre pedestal de concreto", "una gota de perfume que resbala revelando el atomizador dorado"),
    ("Smartwatch deportivo con bisel de titanio sobre grava volcánica", "un chorro de agua a presión que limpia la pantalla OLED encendiéndose"),
    ("Serum facial en gotero de vidrio ámbar sobre mármol blanco", "una gota densa que cae del gotero formando una corona perfecta"),
    ("Lente de cámara fotográfica sobre base de madera de nogal", "un giro suave del anillo de enfoque con rack focus milimétrico")
]

def generar_par_product(idea, accion):
    ancla = (
        f"Photorealistic premium product macro shot, vertical 9:16. {idea}, shot from a low heroic angle of 20 degrees with a 100mm macro lens at f/4: "
        f"razor-thin focus on product's front edge, background falling into deep darkness. Dramatic lighting: two hard 5600K strip rim lights from left and right tracing contours, "
        f"subtle teal brand-color accent glow from behind, crisp specular highlights on surface textures. Physically accurate micro-surface texture, precise seam line, clean luxury look. Zero text, zero watermarks."
    )
    chosen = (
        f"Maintain the exact product shape, size, matte finish, seam lines and materials from the first frame. It never morphs, duplicates or changes proportions. Keep rim lighting and accent glow exactly.\n\n"
        f"CAMERA: 100mm macro on a motorized slider: extreme slow-motion opening for the first 2 seconds, then smooth speed ramp to real time as camera performs a slow 20-degree orbit and push-in. One gentle rack focus across the surface. Perfectly stable, no shake, no cuts.\n\n"
        f"SUBJECT: Hook: in slow motion, {accion}. Realistic hand with five well-proportioned fingers enters frame from right, pressing and interacting with damped physical resistance. Contact shadows and fingertip pressure look physically real. Zero distortion of product dimensions.\n\n"
        f"ENVIRONMENT: Dark premium tabletop set, hard rim lights, colored accent glow, minimalist luxury mood.\n\n"
        f"Audio: crisp amplified impact sound, satisfying mechanical click, deep low-frequency whoosh during speed ramp, no voice, no music, no subtitles."
    )
    rejected = (
        f"Maintain product. "
        f"CAMERA: Shaky handheld camera in macro. "
        f"SUBJECT: Product changes size and shape, buttons duplicate, liquid flows upwards defying gravity, hand has six deformed fingers that phase through the solid product casing. "
        f"ENVIRONMENT: Flat wash lighting. Audio: loud synthesizer music."
    )
    return ancla, chosen, rejected

# ==============================================================================
# GENERADOR MAESTRO Y EXPORTADOR
# ==============================================================================
def exportar_datasets_completos():
    formatos = {
        "talkinghead": [],
        "podcast": [],
        "ugc": [],
        "street": [],
        "product": []
    }

    # 1. Generar pares Talking Head (30 pares)
    for _ in range(6):
        for idea, speech in TALKING_HEAD_IDEAS:
            ancla, c, r = generar_par_talkinghead(idea, speech)
            formatos["talkinghead"].append({
                "format": "talking_head_commercial",
                "prompt": f"Generate an Image-to-Video (I2V) prompt for Veo 3.1 based on this anchor: {ancla[:120]}... Action: Presenter delivers speech directly to camera",
                "chosen": c,
                "rejected": r
            })

    # 2. Generar pares Podcast (30 pares)
    for _ in range(6):
        for idea, speech in PODCAST_IDEAS:
            ancla, c, r = generar_par_podcast(idea, speech)
            formatos["podcast"].append({
                "format": "podcast_storytelling_3_4",
                "prompt": f"Generate an Image-to-Video (I2V) prompt for Veo 3.1 based on this anchor: {ancla[:120]}... Action: Thoughtful podcast interview delivery with SM7B",
                "chosen": c,
                "rejected": r
            })

    # 3. Generar pares UGC (30 pares)
    for _ in range(6):
        for idea, speech in UGC_IDEAS:
            ancla, c, r = generar_par_ugc(idea, speech)
            formatos["ugc"].append({
                "format": "ugc_creator_testimonial",
                "prompt": f"Generate an Image-to-Video (I2V) prompt for Veo 3.1 based on this anchor: {ancla[:120]}... Action: Fast casual smartphone selfie creator review",
                "chosen": c,
                "rejected": r
            })

    # 4. Generar pares Street (30 pares)
    for _ in range(6):
        for idea, preg, resp in STREET_IDEAS:
            ancla, c, r = generar_par_street(idea, preg, resp)
            formatos["street"].append({
                "format": "street_interview_voxpop",
                "prompt": f"Generate an Image-to-Video (I2V) prompt for Veo 3.1 based on this anchor: {ancla[:120]}... Action: Street interview reaction and answer",
                "chosen": c,
                "rejected": r
            })

    # 5. Generar pares Product (30 pares)
    for _ in range(6):
        for idea, act in PRODUCT_IDEAS:
            ancla, c, r = generar_par_product(idea, act)
            formatos["product"].append({
                "format": "product_macro_hook",
                "prompt": f"Generate an Image-to-Video (I2V) prompt for Veo 3.1 based on this anchor: {ancla[:120]}... Action: Luxury macro product reveal with physical splash",
                "chosen": c,
                "rejected": r
            })

    # Guardar cada dataset individualmente
    for k, items in formatos.items():
        fname = f"dataset_dpo_{k}.jsonl"
        with open(fname, "w", encoding="utf-8") as f:
            for item in items:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        print(f"[OK] Exportado: {fname} con {len(items)} pares DPO.")

    # Guardar también el DATASET MAESTRO MULTI-FORMATO (150 pares de oro)
    todos = []
    for items in formatos.values():
        todos.extend(items)
    with open("dataset_video_maestro_5_formatos_dpo.jsonl", "w", encoding="utf-8") as f:
        for item in todos:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"\n[OK] DATASET MAESTRO UNIFICADO: dataset_video_maestro_5_formatos_dpo.jsonl ({len(todos)} pares DPO)")

if __name__ == "__main__":
    exportar_datasets_completos()
