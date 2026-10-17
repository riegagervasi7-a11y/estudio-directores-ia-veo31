"""
generador_dataset_video.py
Generador de Dataset de Video (DPO y SFT) en "Modo Bestia" para Google Veo 3.1 y Higgsfield.
Especializado en Spots Publicitarios, Avatares a Cámara y Escenas Cinemáticas.

Garantiza:
1. Frase obligatoria de anclaje inicial ("Maintain the exact...").
2. CÁMARA física primero (lock-off o slow push-in con inercia).
3. GESTIVULACIÓN FACIAL ACTIVA: Erradica el 'Stiff Upper Face' (cejas móviles con modulación vocal,
   ojos vivos con micro-sacadas, contracción orbicular Duchenne, cero frente congelada).
4. ENTORNO e Iluminación constante + etiqueta Audio:.
5. Castigo en DPO de caras rígidas, zooms digitales y clichés de IA.
"""

import json
from evaluador_juez_video import evaluar_prompt_video

PRESENTADORES_COMERCIALES = [
    {
        "ancla": "Anchor photo of an articulate Latina tech founder in a tailored charcoal blazer in a modern office",
        "accion": "she speaks directly to camera explaining the company vision with persuasive confidence",
        "tema": "tech commercial"
    },
    {
        "ancla": "Anchor photo of an East Asian corporate strategist in a midnight-navy blazer in an architectural loft",
        "accion": "he speaks directly to camera presenting quarterly strategic insights with calm authority",
        "tema": "corporate spot"
    },
    {
        "ancla": "Anchor photo of a confident African American female medical director in a lab blazer in a healthcare center",
        "accion": "she speaks directly to camera detailing a breakthrough in patient care with empathetic warmth",
        "tema": "healthcare ad"
    },
    {
        "ancla": "Anchor photo of a Caucasian clean-tech entrepreneur in an unstructured grey jacket in a green headquarters",
        "accion": "he speaks directly to camera outlining sustainable energy solutions with inspiring cadence",
        "tema": "sustainability spot"
    },
    {
        "ancla": "Anchor photo of a Middle Eastern female creative director in a black minimalist blazer in a bright loft",
        "accion": "she speaks directly to camera introducing new design software features with vibrant energy",
        "tema": "creative agency ad"
    },
    {
        "ancla": "Anchor photo of a South Asian financial consultant in a bespoke dark wool blazer in an executive lounge",
        "accion": "he speaks directly to camera sharing wealth management principles with trustworthy composure",
        "tema": "financial commercial"
    },
    {
        "ancla": "Anchor photo of a Brazilian AI research specialist in a slate-grey blazer in a high-tech glass atrium",
        "accion": "she speaks directly to camera explaining autonomous AI workflows with sharp articulation",
        "tema": "B2B AI commercial"
    },
    {
        "ancla": "Anchor photo of a Western European commercial spokesperson in a sand-beige linen blazer in a photo studio",
        "accion": "he speaks directly to camera presenting a luxury product launch with refined charm",
        "tema": "luxury commercial"
    },
    {
        "ancla": "Anchor photo of an East Asian female e-commerce operations director in a forest-green blazer",
        "accion": "she speaks directly to camera demonstrating global fulfillment logistics with energetic clarity",
        "tema": "e-commerce spot"
    },
    {
        "ancla": "Anchor photo of a Latina corporate legal counsel in a navy double-breasted blazer in a law library",
        "accion": "she speaks directly to camera reviewing enterprise compliance ethics with firm professionalism",
        "tema": "institutional spot"
    },
    {
        "ancla": "Anchor photo of a luxury real estate broker in a crisp tailored beige suit in a penthouse",
        "accion": "he speaks directly to camera showcasing luxury architectural amenities with polished elegance",
        "tema": "real estate spot"
    },
    {
        "ancla": "Anchor photo of a female FinTech product manager in an olive modern blazer in a glass conference room",
        "accion": "she speaks directly to camera explaining cross-border payment security with reassuring clarity",
        "tema": "fintech ad"
    },
    {
        "ancla": "Anchor photo of an automotive design engineer in an indigo unstructured blazer in a design studio",
        "accion": "he speaks directly to camera detailing aerodynamic performance innovations with sharp focus",
        "tema": "automotive commercial"
    },
    {
        "ancla": "Anchor photo of a female edtech university professor in a burgundy jacket in a sunlit modern campus",
        "accion": "she speaks directly to camera inspiring students on digital learning accessibility with warm passion",
        "tema": "edtech commercial"
    },
    {
        "ancla": "Anchor photo of a boutique hotel brand ambassador in a linen blend jacket in a luxury lounge",
        "accion": "he speaks directly to camera narrating curated hospitality experiences with inviting warmth",
        "tema": "hospitality spot"
    }
]

ESCENARIOS_DOCUMENTALES = [
    {
        "ancla": "Anchor photo of an elderly Scandinavian fisherman in a heavy yellow rain slicker on a wet dock",
        "accion": "he exhales a visible mist of cold breath and turns his gaze slowly towards the open sea",
        "audio": "Audio: cold coastal wind whistling softly, quiet harbor water lap against dock pylons, zero music."
    },
    {
        "ancla": "Anchor photo of two mechanics under the open hood of a vintage pickup in a workshop",
        "accion": "the senior mechanic tightens a bolt with steady torque while the apprentice holds the inspection light",
        "audio": "Audio: metallic click of wrench ratchet, low fluorescent ballast hum, quiet workshop breathing."
    },
    {
        "ancla": "Anchor photo of a female doctor resting in a quiet hospital hallway between rounds",
        "accion": "she lowers her shoulders with a slow exhale of fatigue, glancing briefly at her wristwatch",
        "audio": "Audio: distant muffled hospital ventilation hum, quiet rubber sole squeak in hallway, no music."
    },
    {
        "ancla": "Anchor photo of an elderly potter shaping clay on a rotating wheel in a sunlit studio",
        "accion": "his clay-coated fingers smooth the vessel rim with continuous gentle centrifugal pressure",
        "audio": "Audio: wet friction sound of hands on spinning clay, quiet wooden studio room tone."
    },
    {
        "ancla": "Anchor photo of a woman holding a warm ceramic mug by a rain-streaked cafe window",
        "accion": "she raises the mug to her lips for a slow sip while gazing thoughtfully through the glass",
        "audio": "Audio: gentle steady rain patter against glass window, distant muffled espresso machine hiss."
    }
]

MOVIMIENTOS_CAMARA_COMERCIAL = [
    ("Static commercial lock-off shot with faint organic operator breathing motion on an 85mm prime lens at eye level", "Perfect horizon, zero camera shake, high-end commercial tripod stability, no fast pans, no digital zoom."),
    ("Slow subtle push-in on an 85mm portrait prime lens at eye level with gentle physical inertia", "Steadily maintaining intimate commercial framing, zero digital zooming."),
    ("Steady commercial tripod shot with locked horizon and subtle human operator breath", "Constant focal length, perfectly grounded framing, zero artificial stabilization jitter.")
]

VARIACIONES_GESTICULACION = [
    (
        "The presenter speaks directly to the camera with rich, natural, and expressive facial articulation: {accion}. "
        "Active upper-face dynamics: her eyebrows lift naturally and modulate with vocal inflections to emphasize key points, with subtle forehead engagement. "
        "Lively, engaged eyes with authentic ocular micro-saccades, blinking naturally at second 2 and second 5, with warm crinkling at the outer corners during confident delivery. "
        "Organic jaw movement with clean articulation, subtle head tilts complementing cadence, relaxed neck and shoulders. "
        "Zero stiffness, zero mask-like frozen forehead, no exaggerated hand gestures, no morphing, no facial distortion."
    ),
    (
        "The presenter delivers dialogue directly to camera with dynamic human engagement: {accion}. "
        "Expressive brow mobility with natural eyebrow raises coordinated with verbal emphasis, eliminating any robotic stiffness. "
        "Warm, lively gaze with natural eye micro-movements, blinking at second 2.5, authentic eye crinkles during approachable moments. "
        "Clean phoneme formation with natural mouth pacing, gentle rhythmic head nods on pivotal words. "
        "Smooth facial cohesion across forehead, eyes, and mouth, zero frozen face, zero facial warping."
    ),
    (
        "The presenter speaks directly into the lens with authentic commercial charisma: {accion}. "
        "Fluid upper-face articulation: subtle brow modulation and eyebrow elevation synchronized with speech rhythm, creating credible conversational warmth. "
        "Engaged eyes maintaining magnetic direct eye contact with subtle ocular micro-movements, natural blink at second 2. "
        "Natural mouth opening and closing without exaggerated jaw slack, relaxed neck and still shoulders. "
        "Zero mask-like paralysis, zero stiff facial features, flawless identity stability from the first frame."
    )
]

VICIOS_VIDEO_REJECTED = [
    # Vicio 1: Frente y cejas congeladas (Stiff Upper Face)
    lambda p: (
        f"Maintain the exact presenter from the first frame. "
        f"CAMERA: Smooth digital zoom. "
        f"SUBJECT: The presenter speaks with completely static frozen eyebrows, unmoving forehead, rigid fixed stare, micro-movements only, marionette jaw movement with stiff face. "
        f"ENVIRONMENT: Studio lighting. Audio: voice."
    ),
    # Vicio 2: Clichés de IA y zoom rápido
    lambda p: (
        f"Cinematic 8k smooth camera zooming fast around the presenter, hyperrealistic video, masterpiece, "
        f"she smiles and laughs with open mouth, fast head turns, octane render, beautiful motion."
    ),
    # Vicio 3: Re-descripción de rostro y ropa (causa morphing)
    lambda p: (
        f"Camera tracks the woman with brown eyes wearing a tailored blazer and white shirt, "
        f"she has handsome face and smiling mouth, smooth 4k video, dramatic lighting."
    )
]

def generar_dataset_video_completo():
    dpo_items = []
    sft_items = []

    # 1. Procesar Presentadores Comerciales con Gesticulación Facial Activa
    ACCIONES_EXTRA_PRES = [
        "speaks directly to camera explaining key value propositions with engaging articulation",
        "delivers a persuasive commercial message directly to the viewer with warm confidence",
        "introduces the core benefits of the service with articulate cadence and friendly eye contact"
    ]

    idx = 0
    for pres in PRESENTADORES_COMERCIALES:
        acciones = [pres["accion"]] + [f"she {act}" if "female" in pres["ancla"] or "Latina" in pres["ancla"] else f"he {act}" for act in ACCIONES_EXTRA_PRES[:2]]
        for acc in acciones:
            for cam, cam_desc in MOVIMIENTOS_CAMARA_COMERCIAL:
                gest_template = VARIACIONES_GESTICULACION[idx % len(VARIACIONES_GESTICULACION)]
                vicio_fn = VICIOS_VIDEO_REJECTED[idx % len(VICIOS_VIDEO_REJECTED)]
                idx += 1

                subj_action = gest_template.format(accion=acc)

                chosen = (
                    f"Maintain the exact presenter, facial identity, wardrobe, and modern architectural background from the first frame.\n\n"
                    f"CAMERA: {cam}. {cam_desc}\n\n"
                    f"SUBJECT: {subj_action}\n\n"
                    f"ENVIRONMENT: Commercial studio softbox lighting remains completely constant throughout the shot. Continuous atmospheric coherence.\n\n"
                    f"Audio: natural ambient room tone and clean studio acoustics, subtle presenter presence, no music, no spoken dialogue."
                )

                rejected = vicio_fn(pres)

                prompt_user = f"Generate an Image-to-Video (I2V) prompt for Veo 3.1 based on this anchor: {pres['ancla']}. Action: {acc}"

                res_c = evaluar_prompt_video(chosen)
                res_r = evaluar_prompt_video(rejected)

                if res_c["score"] >= 9.5 and res_r["score"] <= 5.0:
                    dpo_items.append({
                        "prompt": prompt_user,
                        "chosen": chosen,
                        "rejected": rejected,
                        "score_chosen": res_c["score"],
                        "score_rejected": res_r["score"]
                    })

                    sft_items.append({
                        "instruction": "You are an elite cinematic commercial director and Image-to-Video (I2V) prompt engineer for Veo 3.1 and Higgsfield. Formulate video prompts with anchor preservation, stable physical camera movement, active upper-face facial gesticulation (eyebrow modulation, lively eyes, eliminating frozen forehead), constant lighting, and explicit ambient Audio tag.",
                        "input": f"Anchor: {pres['ancla']}\nAction: {acc}",
                        "output": chosen
                    })

    # 2. Procesar Escenarios Documentales
    for doc in ESCENARIOS_DOCUMENTALES:
        for cam, cam_desc in MOVIMIENTOS_CAMARA_COMERCIAL[:2]:
            chosen = (
                f"Maintain the exact subject, facial identity, wardrobe, and environment from the first frame.\n\n"
                f"CAMERA: {cam}. {cam_desc}\n\n"
                f"SUBJECT: The subject performs the intended action with natural human cadence: {doc['accion']}. "
                f"At second 2, a natural blink, subtle chest breath, and realistic weight transfer. "
                f"Natural expressive ocular engagement, zero robotic stiffness, no morphing, no facial distortion.\n\n"
                f"ENVIRONMENT: Ambient lighting remains completely constant throughout the shot. Continuous atmospheric coherence.\n\n"
                f"{doc['audio']}"
            )
            rejected = f"Cinematic 8k smooth camera moving around the subject, hyperrealistic video, fast motion, masterpiece, {doc['accion']}, octane render."

            prompt_user = f"Generate an Image-to-Video (I2V) prompt for Veo 3.1 based on this anchor: {doc['ancla']}. Action: {doc['accion']}"

            res_c = evaluar_prompt_video(chosen)
            res_r = evaluar_prompt_video(rejected)

            if res_c["score"] >= 9.5 and res_r["score"] <= 5.0:
                dpo_items.append({
                    "prompt": prompt_user,
                    "chosen": chosen,
                    "rejected": rejected,
                    "score_chosen": res_c["score"],
                    "score_rejected": res_r["score"]
                })
                sft_items.append({
                    "instruction": "You are an elite cinematic director for Veo 3.1.",
                    "input": f"Anchor: {doc['ancla']}\nAction: {doc['accion']}",
                    "output": chosen
                })

    # Guardar en JSONL
    with open("dataset_video_dpo.jsonl", "w", encoding="utf-8") as f:
        for item in dpo_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    with open("dataset_video_sft.jsonl", "w", encoding="utf-8") as f:
        for item in sft_items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print("[OK] Dataset de Video regenerado con exito:")
    print(f"     - DPO: dataset_video_dpo.jsonl ({len(dpo_items)} pares)")
    print(f"     - SFT: dataset_video_sft.jsonl ({len(sft_items)} pares)")
    return len(dpo_items), len(sft_items)

if __name__ == "__main__":
    generar_dataset_video_completo()
