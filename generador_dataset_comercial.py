"""
generador_dataset_comercial.py
Generador automatizado de Dataset (DPO y SFT) en "Modo Bestia"
Especializado en Spots Publicitarios y Presentadores / Avatares a Cámara
para Google Nano Banana Pro (Imágenes Ancla listas para Video & Lip-Sync).

Garantiza:
1. Boca cerrada y relajada (lip-sync ready).
2. Iluminación comercial off-camera (prohibido equipo o trípodes en el encuadre).
3. Cero marcas de agua ni texto EXIF.
4. Piel sana, creíble y fresca con microporos (sin plástico y sin envejecer al sujeto).
5. Mirada directa al lente con catchlight.
"""

import json
import random
from evaluador_juez_texto import evaluar_prompt

AVATARES_COMERCIALES = [
    {
        "rol_es": "Fundadora tech latina de 30 años en una oficina contemporánea de arquitectura limpia",
        "sujeto": "an articulate Latina tech founder in her early 30s",
        "ropa": "tailored charcoal wool-blend blazer over a crisp ivory silk collarless blouse",
        "fondo": "softly blurred contemporary architectural office with warm Scandinavian timber slats and diffuse glass partitions"
    },
    {
        "rol_es": "Estratega corporativo asiático de 34 años en un estudio corporativo moderno",
        "sujeto": "a poised East Asian corporate strategist in his mid-30s",
        "ropa": "tailored midnight-navy unstructured suit jacket with a fine cotton crew-neck knit",
        "fondo": "minimalist architectural loft with large diffuse frosted windows in soft background bokeh"
    },
    {
        "rol_es": "Directora médica afroamericana de 35 años para spot de innovación en salud",
        "sujeto": "a confident African American female medical director in her mid-30s",
        "ropa": "clean modern tailored white lab blazer over a navy blue structured silk shirt",
        "fondo": "high-end healthcare innovation center with soft natural ambient daylight and subtle architectural glass"
    },
    {
        "rol_es": "Emprendedor de energías renovables caucásico de 32 años en sede central moderna",
        "sujeto": "an engaging Caucasian clean-tech entrepreneur in his early 30s",
        "ropa": "tailored deep-grey unstructured blazer over a crisp light-blue spread-collar shirt",
        "fondo": "modern sustainable corporate headquarters with lush vertical green garden wall softly blurred in background"
    },
    {
        "rol_es": "Directora creativa de origen árabe de 29 años para campaña de software de diseño",
        "sujeto": "a dynamic Middle Eastern female creative director in her late 20s",
        "ropa": "minimalist tailored black architectural jacket with clean geometric lapels",
        "fondo": "bright contemporary creative agency loft with polished concrete and diffused daylight"
    },
    {
        "rol_es": "Consultor financiero de 38 años para anuncio de plataforma de inversiones",
        "sujeto": "a trustworthy South Asian financial consultant in his late 30s",
        "ropa": "bespoke dark-charcoal wool blazer with crisp lapels and tailored sky-blue shirt",
        "fondo": "sophisticated modern executive lounge with muted walnut paneling and warm ambient background"
    },
    {
        "rol_es": "Especialista en inteligencia artificial brasileña de 31 años para spot tecnológico B2B",
        "sujeto": "an articulate Brazilian AI research specialist in her early 30s",
        "ropa": "tailored slate-grey single-breasted blazer over a fine-knit ribbed navy top",
        "fondo": "high-tech research campus with glass atrium and soft cool natural daylight falloff"
    },
    {
        "rol_es": "Portavoz corporativo europeo de 33 años en plató editorial de publicidad",
        "sujeto": "a charismatic Western European commercial spokesperson in his early 30s",
        "ropa": "tailored unstructured sand-beige linen-wool blend blazer over an open-collar white linen shirt",
        "fondo": "warm neutral grey textured studio backdrop with soft organic shadow gradation"
    },
    {
        "rol_es": "Líder de operaciones de comercio electrónico de 30 años para anuncio publicitario",
        "sujeto": "a vibrant East Asian female e-commerce operations director in her early 30s",
        "ropa": "tailored forest-green blazer with crisp sharp lines over a neutral silk shell",
        "fondo": "modern logistics innovation lab with softly out-of-focus warm ambient workstation lights"
    },
    {
        "rol_es": "Abogada corporativa y asesora legal de 36 años para spot institucional",
        "sujeto": "an authoritative Latina corporate legal counsel in her mid-30s",
        "ropa": "tailored double-breasted navy blazer with matte horn buttons and pristine silk blouse",
        "fondo": "contemporary law firm library with warm floor-to-ceiling glass and softly blurred city skyline"
    }
]

MATRIZ_VARIACIONES = [
    {
        "expresion": "warm, confident, engaging expression",
        "luz": "high-end commercial production lighting, soft diffuse off-camera studio key light at 45 degrees casting gentle flattering shadow falloff across cheekbones, subtle clean edge rim light cleanly separating shoulders from the background",
        "textura": "unretouched healthy skin showing genuine pores, natural skin sheen, fine stray hairs along hairline, authentic human presence, zero waxy plastic CGI"
    },
    {
        "expresion": "calm, poised, trustworthy commercial expression",
        "luz": "diffuse off-camera softbox key illumination at 45 degrees with gentle natural fill, balanced 5600K clean daylight color temperature, clean separation rim light on shoulders",
        "textura": "authentic healthy skin micro-texture, visible pores on cheeks, natural hydration sheen, delicate baby hairs near temples, realistic human skin with zero artificial smoothing"
    },
    {
        "expresion": "approachable, articulate, friendly professional expression",
        "luz": "soft off-camera commercial octabox key light with wide gentle wrap-around, soft shadow roll-off under jawline, subtle edge rim light adding dimensional depth",
        "textura": "clean professional skin micro-texture with natural pores, subtle authentic specular highlights on nose bridge and cheekbones, fine stray hair strands, genuine presence"
    }
]

VICIOS_REJECTED = [
    # Vicio 1: Clichés de plástico AI
    lambda a: f"Hyperrealistic beautiful {a['sujeto']}, 8k resolution, photorealistic, masterpiece, flawless porcelain smooth skin, perfect symmetrical face, cinematic studio lighting, octane render, trending on artstation.",
    # Vicio 2: Equipos dentro del cuadro (softbox dibujado)
    lambda a: f"Commercial advertising portrait of {a['sujeto']} standing next to a large Profoto 5-foot softbox and light stand on the right side of the frame, studio umbrellas visible, dramatic lighting, 8k photo.",
    # Vicio 3: Metadatos EXIF / Marcas de agua impresas
    lambda a: f"Hasselblad H6D 85mm f/2.8 1/250s ISO 100 metadata printed in white text on bottom left corner, portrait of {a['sujeto']}, commercial photography, 4k, award-winning shot.",
    # Vicio 4: Envejecimiento artificial excesivo
    lambda a: f"A photo of {a['sujeto']}, heavy deep forehead wrinkles, prominent crow's feet, weathered sagging facial skin, tired under-eye bags, aged complexion, unretouched documentary style.",
    # Vicio 5: Boca abierta riendo que arruina el lip-sync
    lambda a: f"A candid photo of {a['sujeto']} laughing with wide open mouth showing all teeth, exaggerated jaw movement, head thrown back mid-laugh, cinematic studio lighting, perfect face."
]

def generar_dataset_comercial(cantidad_total: int = 120):
    pares_dpo = []
    pares_sft = []

    contador = 0
    while len(pares_dpo) < cantidad_total:
        base = random.choice(AVATARES_COMERCIALES)
        var = random.choice(MATRIZ_VARIACIONES)
        vicio_fn = random.choice(VICIOS_REJECTED)

        prompt_usuario = f"Generate a commercial advertising portrait prompt for an AI presenter: {base['rol_es']}"

        chosen = (
            f"A high-end commercial advertising portrait of {base['sujeto']}, medium close-up framing, "
            f"looking directly into the camera lens with a {var['expresion']}. "
            f"Mouth closed in a natural relaxed rest position with gentle lip seal, perfectly primed for speech animation. "
            f"Wearing a {base['ropa']}. "
            f"{var['luz'].capitalize()}. "
            f"Shot on 85mm portrait prime lens at f/2.8, RAW camera sensor, tack-sharp iris focus with natural catchlight reflections. "
            f"{var['textura'].capitalize()}, "
            f"no visible studio equipment, no light stands in shot, zero text or watermarks."
        )

        rejected = vicio_fn(base)

        eval_chosen = evaluar_prompt(chosen)
        eval_rejected = evaluar_prompt(rejected)

        # Filtro de calidad estricto
        if eval_chosen["score"] >= 9.5 and eval_rejected["score"] <= 4.0:
            par_dpo = {
                "prompt": prompt_usuario,
                "chosen": chosen,
                "rejected": rejected,
                "score_chosen": eval_chosen["score"],
                "score_rejected": eval_rejected["score"]
            }
            pares_dpo.append(par_dpo)

            par_sft = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a master commercial photography prompt engineer. Your prompts produce flawless high-end advertising portraits of presenters speaking to camera for commercial video spots, strictly avoiding AI plastic, visible studio gear, text watermarks, or distorted lip poses."
                    },
                    {
                        "role": "user",
                        "content": prompt_usuario
                    },
                    {
                        "role": "assistant",
                        "content": chosen
                    }
                ]
            }
            pares_sft.append(par_sft)
            contador += 1
            if contador % 20 == 0:
                print(f"[+] Generados y auditados {contador}/{cantidad_total} pares comerciales...")

    # Guardar archivos JSONL
    with open("dataset_comercial_dpo.jsonl", "w", encoding="utf-8") as f:
        for p in pares_dpo:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    with open("dataset_comercial_sft.jsonl", "w", encoding="utf-8") as f:
        for p in pares_sft:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    print("\n[OK] Dataset Comercial completado con exito!")
    print(f"    - DPO: dataset_comercial_dpo.jsonl ({len(pares_dpo)} pares)")
    print(f"    - SFT: dataset_comercial_sft.jsonl ({len(pares_sft)} pares)")

if __name__ == "__main__":
    generar_dataset_comercial(120)
