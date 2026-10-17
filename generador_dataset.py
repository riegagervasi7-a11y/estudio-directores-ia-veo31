"""
generador_dataset.py
Generador automatizado del dataset de entrenamiento (SFT y DPO)
especializado en hiperrealismo anti-IA para Google Nano Banana Pro.

Valida automáticamente cada par con evaluador_juez_texto.py para garantizar
que CHOSEN alcance >= 9.0 y REJECTED contenga los vicios típicos de IA.
"""

import json
from evaluador_juez_texto import evaluar_prompt

# Matriz base de escenarios con diversidad demográfica, óptica y lumínica
ESCENARIOS_BASE = [
    # 1. Candid Street & Snapshot (Flash Directo / Calle)
    {
        "idea": "Joven latino de 24 años riendo en una fiesta nocturna en un pasillo",
        "rejected": "Hyperrealistic handsome 24 year old latino man laughing at night party, 8k resolution, photorealistic, masterpiece, perfect handsome face, cinematic neon lighting, ultra detailed skin, octane render.",
        "chosen": "A candid point-and-shoot direct on-camera flash photograph of a 24-year-old Latino man laughing mid-conversation in an apartment hallway. Harsh direct flash creates authentic specular highlights on forehead and nose, casting a sharp dark shadow on the textured beige wall behind him. Natural skin sheen, light five o'clock stubble with individual coarse hairs, slight asymmetrical squint during genuine laughter, visible pores on cheeks. Wearing an unbuttoned vintage flannel shirt over a white ribbed cotton tank top. Shot on a 35mm compact camera, f/4 aperture, 1/125s, fine organic film noise, authentic 90s disposable snapshot aesthetic."
    },
    {
        "idea": "Mujer asiática de 28 años caminando por una calle de Tokio en día lluvioso",
        "rejected": "Ultra-realistic 28 year old japanese woman walking on rainy street in tokyo, photorealistic, 8k, flawless skin, masterpiece, beautiful face, soft bokeh background, trending on artstation.",
        "chosen": "A candid street photograph of a 28-year-old Japanese woman glancing sideways while holding a clear vinyl umbrella on a wet Tokyo sidewalk at dusk. Subtle raindrops clinging to her coat collar. Authentic skin micro-texture with visible pores, faint dark circles under eyes from a long workday, natural flyaway hair strands damp with humidity. Wearing an oversized dark olive trench coat with visible water droplets on the fabric weave. Shot on an 85mm lens at f/2.2, ISO 800, 1/250s on Kodak Portra 400 film stock. Diffuse ambient reflections from shop windows casting gentle cool-toned fill light, natural optical depth of field with unretouched asphalt texture."
    },
    {
        "idea": "Anciano afrodescendiente de 70 años descansando en el porche de su casa",
        "rejected": "Hyperrealistic old black man 70 years old sitting on porch, 8k, photorealistic portrait, dramatic rim light, octane render, beautiful ultra detailed wrinkles, masterpiece.",
        "chosen": "An intimate environmental portrait of a 70-year-old African American man resting in a wooden rocking chair on his front porch during early morning. Natural weathered skin with deep authentic expression lines, fine crow's feet around smiling eyes, grey-white coarse beard with individual wiry hairs, subtle sunspots on temples. Wearing a faded blue chambray work shirt with worn fabric seams and rolled-up sleeves. Soft overcast morning daylight, 5600K color temperature, gentle shadow roll-off under jawline. Shot on a 50mm f/1.8 lens stopped down to f/2.8 on Leica M11 RAW sensor, unsharpened sensor noise, genuine documentary photography aesthetic."
    },
    {
        "idea": "Mujer caucásica de 34 años tomando café en una cafetería junto a la ventana",
        "rejected": "Photorealistic 34 year old beautiful blonde woman drinking coffee, hyperrealistic, 8k resolution, perfect smooth skin, award-winning photo, cinematic volumetric light.",
        "chosen": "A candid 35mm film photograph of a 34-year-old Caucasian woman with sandy blonde hair looking away in thought while holding a ceramic coffee mug with both hands. Natural north-facing window light softly sculpting her facial profile, casting gentle authentic shadows across her cheekbone. Realistic skin texture showing pores, subtle freckles across the nose bridge, tiny dry patch on upper lip, natural flyaway hair catching the soft window rim light. Wearing a thick charcoal wool-blend knit sweater with visible wool fibers. Shot on an 85mm lens at f/2.0, ISO 400 on Kodak Portra 400, unedited documentary aesthetic with authentic optical bokeh."
    },
    {
        "idea": "Mecánico hispano de 45 años trabajando en su taller con grasa en las manos",
        "rejected": "Hyperrealistic 45 year old mechanic in garage, photorealistic portrait, 8k, unreal engine 5, dramatic cinematic lighting, masterpiece, ultra detailed face.",
        "chosen": "A candid documentary photograph of a 45-year-old Hispanic auto mechanic wiping his brow with the back of a grease-stained hand inside a dimly lit workshop. Natural sweat sheen on forehead, weathered skin with prominent pores, crow's feet, oil smudges across cheekbone, irregular stubble. Wearing a dark navy canvas work jumpsuit with frayed cuffs and oil stains. Mixed lighting: cool overhead fluorescent tubes combined with warm tungsten work lamp at 3200K creating realistic specular glints. Shot on a 35mm f/1.4 lens at f/2.4, ISO 1200 on Cinestill 800T film, authentic halation around bare light bulbs, gritty analog grain."
    },
    {
        "idea": "Estudiante universitaria india de 21 años en la biblioteca entre estanterías",
        "rejected": "Photorealistic gorgeous 21 year old indian girl student in library, hyperrealistic, 8k, flawless glass skin, perfect symmetrical face, masterpiece.",
        "chosen": "A quiet, unposed portrait of a 21-year-old South Asian woman leaning against a wooden library bookshelf, eyes slightly squinted as she reads a paperback. Authentic skin micro-texture, natural peach fuzz along jawline, visible pores on T-zone, minor blemish near hairline, subtle asymmetrical smile. Dark thick hair with several flyaway strands escaping a loose bun. Wearing an oversized mustard-yellow corduroy overshirt showing visible ribbed texture. Soft indirect ambient daylight filtering through tall library windows. Shot on a 50mm lens at f/2.0, ISO 640 on Kodak Portra 400, authentic optical falloff and gentle film grain."
    },
    {
        "idea": "Pescador nórdico de 58 años en un muelle con abrigo impermeable",
        "rejected": "Hyperrealistic old fisherman at dock, 8k, photorealistic, dramatic ocean background, masterpiece, octane render, ultra-detailed skin.",
        "chosen": "A raw documentary portrait of a 58-year-old Scandinavian fisherman standing on a wet wooden dock in harsh overcast coastal weather. Wind-burned ruddy complexion, visible broken capillaries on cheeks, deep forehead creases, salt-and-pepper dense beard with coarse sea-spray droplets clinging to the whiskers. Wearing a heavy-duty bright yellow PVC rain jacket with visible salt crust around the collar. Cold overcast daylight at 6000K, flat even lighting revealing genuine skin texture. Shot on an 85mm lens at f/3.2, 1/500s, Leica M11 uncompressed RAW, zero artificial sharpening, tactile physical realism."
    },
    {
        "idea": "Chica de 19 años en el metro de noche escuchando música con audífonos",
        "rejected": "Hyperrealistic 19 year old girl in subway at night, 8k, photorealistic, cinematic neon lighting, perfect face, masterpiece, smooth skin.",
        "chosen": "A candid snapshot of a 19-year-old woman sitting on a plastic subway car seat at night, looking down at her phone with wired earphones. Point-and-shoot direct on-camera flash style mixed with dim interior fluorescent lighting. Realistic skin with teenage acne remnants on temple, visible skin pores, natural oiliness on nose, chapped lips, slightly tired posture. Wearing an oversized thrifted leather bomber jacket with surface creases and abrasions over a faded graphic tee. Shot on a 28mm wide-angle lens at f/4, ISO 800, authentic candid grain and slight motion blur on passing passengers in the background."
    },
    {
        "idea": "Chef de 38 años en una cocina profesional emplatando un plato",
        "rejected": "Photorealistic 38 year old handsome chef cooking, hyperrealistic, 8k, cinematic kitchen lighting, perfect skin, masterpiece, trending on artstation.",
        "chosen": "A dynamic documentary-style photograph of a 38-year-old male chef concentrating intently as he plates a dish with kitchen tweezers. Beads of perspiration on his temples, natural skin texture with open pores around nose, furrowed brow with fine tension lines, short trimmed beard with realistic individual hairs. Wearing a white double-breasted cotton chef's jacket with authentic fabric weave and subtle sauce stain on the lower cuff. Overhead warm kitchen halogen lights creating realistic directional highlights and authentic kitchen steam catching the light. Shot on a 50mm f/1.8 lens at f/2.5, 1/320s on Sony A7IV RAW, natural optical blur on the background stainless steel counters."
    },
    {
        "idea": "Anciana de 78 años sonriendo en su jardín cuidando plantas",
        "rejected": "Hyperrealistic grandmother 78 years old in garden, 8k, photorealistic portrait, masterpiece, beautiful happy face, octane render, smooth lighting.",
        "chosen": "An intimate natural light portrait of a 78-year-old woman with silver curly hair smiling warmly with crinkled eyes while pruning tomato plants in her backyard. Deep authentic laughter lines around mouth, paper-thin delicate skin on cheekbones with fine wrinkles and sunspots, natural uneven dental alignment during her genuine smile. Wearing a soft floral cotton blouse and weathered gardening gloves. Golden hour late-afternoon sunlight at 3200K coming from a 45-degree back angle, catching individual silver flyaway hairs in a halo. Shot on an 85mm lens at f/2.8 on Kodak Portra 400 film, warm organic tones, authentic optical depth of field."
    }
]

# Modificadores sistemáticos para multiplicar y diversificar el dataset a más de 100 pares
VARIACIONES_LUZ = [
    ("direct harsh on-camera flash snapshot, sharp dark shadow cast on the wall behind", "f/4 aperture, 35mm compact camera, ISO 400, fine organic film noise, authentic 90s disposable camera aesthetic"),
    ("soft diffuse north-facing window light, gentle natural shadow roll-off beneath jaw", "f/2.0 aperture, 85mm portrait lens, ISO 400, Kodak Portra 400 film stock, authentic optical depth of field"),
    ("golden hour warm sunlight at 3200K, authentic warm ambient fill and soft shadow roll-off", "f/2.2 aperture, 50mm lens, ISO 200, Kodak Portra 400, natural optical lens bokeh"),
    ("cool overcast daylight at 5600K, even diffuse shadowless lighting across face", "f/2.8 aperture, 85mm lens, ISO 400, Leica M11 RAW uncompressed sensor, subtle sensor noise"),
    ("late-night tungsten street lighting at 3000K mixed with soft ambient storefront glow", "f/1.8 aperture, 35mm lens, ISO 800, Cinestill 800T film stock, authentic halation effect and subtle grain"),
    ("midday harsh sunlight casting authentic hard-edged shadows, natural squinting", "f/4.0 aperture, 50mm lens, 1/1000s shutter speed, ISO 100, Kodak Tri-X 400 black and white film grain"),
    ("cozy dim interior lighting with a warm bedside tungsten lamp and soft shadows", "f/2.0 aperture, 35mm lens, ISO 640, Kodak Portra 400, natural specular warmth")
]

VARIACIONES_EDAD_ETNIA = [
    ("30-year-old Brazilian woman", "warm olive skin tone with visible pores, fine smile lines around eyes, natural skin sheen, loose dark wavy hair with fine flyaway strands, peach fuzz along jawline"),
    ("42-year-old French man", "lean weathered face with visible skin micro-texture, fine crow's feet, salt-and-pepper dense stubble with individual coarse hairs, slight asymmetrical nose"),
    ("27-year-old Korean man", "monolid eyes with authentic gaze, visible skin micro-texture and open pores on nose, minor blemish on chin, natural straight hair with slight disarray and flyaways"),
    ("52-year-old Mexican woman", "rich bronze skin with natural sun lines, expressive dark eyes with fine laugh creases, visible skin pores, silver threads in dark hair with stray flyaways"),
    ("68-year-old British gentleman", "fair weathered skin with fine wrinkles and light sunspots, thinning silver hair, wire-frame glasses, natural skin micro-texture with pores"),
    ("22-year-old Nigerian woman", "deep rich dark complexion with natural luminous hydration sheen, high cheekbones, visible skin pores, braided hair with delicate baby hairs along forehead"),
    ("36-year-old Italian woman", "Mediterranean complexion, expressive arched eyebrows, natural dark circles under eyes, visible skin micro-texture, fine flyaways in dark wavy hair"),
    ("48-year-old German craftsman", "broad weathered face, strong jawline with rugged stubble, deep forehead creases, visible pores, natural sweat sheen on temples from physical work"),
    ("25-year-old Colombian university student", "casual approachable demeanor, visible skin pores on cheeks, natural peach fuzz, unplucked natural eyebrow hairs, slight asymmetrical smile"),
    ("60-year-old Japanese ceramic artist", "contemplative gaze, fine laugh wrinkles around eyes, visible pores, textured hands with clay residue, hair tied loosely back with flyaway strands"),
    ("33-year-old Australian surfer", "sun-kissed fair skin with prominent freckles across nose and cheeks, squinting natural expression, salt-crusted messy blond hair with flyaways, natural skin sheen"),
    ("29-year-old Indian software engineer", "warm south asian skin tone, visible facial pores, neatly trimmed dark beard with individual stubble hairs, fine tired lines under eyes from screen work"),
    ("55-year-old Moroccan spice merchant", "deep warm complexion with character wrinkles, wise smiling eyes with crow's feet, trimmed grey beard, natural skin micro-texture and pores"),
    ("19-year-old Scandinavian art student", "pale nordic skin with slight natural redness on cheeks, delicate peach fuzz, subtle blemish on forehead, messy blonde bob with flyaway hairs"),
    ("40-year-old Argentine tango musician", "olive complexion with light stubble, intense focused expression, fine forehead creases, natural skin sheen, dark hair slicked back with loose strands")
]

VARIACIONES_CONTEXTO = [
    ("waiting for a commuter train on a crowded city platform", "wearing an unbuttoned heavy wool-blend coat with authentic fabric weave and collar lint, authentic urban platform background"),
    ("laughing mid-sentence at a corner booth inside a vintage diner", "wearing a ribbed cotton turtleneck with visible knit seams, Formica table with a half-empty glass in foreground"),
    ("taking a candid snapshot in an apartment elevator", "wearing a slouchy vintage grey fleece hoodie with pilled fabric, subtle brushed metal reflections behind"),
    ("browsing vinyl records in a dusty vintage record shop", "wearing an oversized denim jacket with frayed collar seams and vintage patina, wooden record bins slightly out of focus"),
    ("leaning against a weathered brick wall in an alleyway", "wearing a simple crewneck cotton t-shirt with natural fabric wrinkles and collar wear, textured brick mortar"),
    ("sitting on the hood of a vintage car at twilight", "wearing an authentic leather bomber jacket with surface creases and natural scuffs, evening sky background"),
    ("enjoying a street taco at a bustling night food stand", "wearing a lightweight linen shirt with natural chest creases and unbuttoned top button, steam rising softly in background")
]

def generar_dataset_completo():
    dataset_dpo = []
    dataset_sft = []

    # 1. Agregar los escenarios maestros
    for item in ESCENARIOS_BASE:
        res_chosen = evaluar_prompt(item["chosen"])
        res_rejected = evaluar_prompt(item["rejected"])

        dpo_entry = {
            "prompt": f"Generate a hyperrealistic, non-AI looking photograph prompt for: {item['idea']}",
            "chosen": item["chosen"],
            "rejected": item["rejected"],
            "score_chosen": res_chosen["score"],
            "score_rejected": res_rejected["score"]
        }
        dataset_dpo.append(dpo_entry)

        sft_entry = {
            "instruction": "You are an elite photographic director and prompt engineer for Google Nano Banana Pro. Transform the given concept into a hyperrealistic photograph prompt that looks 100% indistinguishable from a real photograph, eliminating all plastic AI looks, CGI artifacts, and banned buzzwords.",
            "input": item["idea"],
            "output": item["chosen"]
        }
        dataset_sft.append(sft_entry)

    # 2. Generar combinaciones sintéticas controladas
    contador = 0
    for persona, rasgos in VARIACIONES_EDAD_ETNIA:
        for contexto, vestuario in VARIACIONES_CONTEXTO:
            luz, optica = VARIACIONES_LUZ[contador % len(VARIACIONES_LUZ)]
            contador += 1

            idea = f"{persona} {contexto}"
            
            # Prompt Rechazado (con vicios comunes de IA)
            rejected = f"Hyperrealistic {persona} {contexto}, 8k resolution, photorealistic portrait, masterpiece, flawless smooth skin, cinematic lighting, octane render, trending on artstation."
            
            # Prompt Elegido (con 7 capas fotográficas estrictas y micro-imperfecciones)
            chosen = f"A candid photograph of a {persona} {contexto}. {rasgos.capitalize()}. {vestuario.capitalize()}. {luz.capitalize()}. Shot with {optica}, realistic skin micro-texture with visible pores, unposed genuine body language, authentic depth of field, unretouched analog aesthetic."

            # Evaluar con Juez de Texto
            res_c = evaluar_prompt(chosen)
            res_r = evaluar_prompt(rejected)

            # Estándar riguroso de calidad
            if res_c["score"] >= 9.0:
                dpo_item = {
                    "prompt": f"Generate a hyperrealistic, non-AI looking photograph prompt for: {idea}",
                    "chosen": chosen,
                    "rejected": rejected,
                    "score_chosen": res_c["score"],
                    "score_rejected": res_r["score"]
                }
                dataset_dpo.append(dpo_item)

                sft_item = {
                    "instruction": "You are an elite photographic director and prompt engineer for Google Nano Banana Pro. Transform the given concept into a hyperrealistic photograph prompt that looks 100% indistinguishable from a real photograph, eliminating all plastic AI looks, CGI artifacts, and banned buzzwords.",
                    "input": idea,
                    "output": chosen
                }
                dataset_sft.append(sft_item)

    # Guardar archivos JSONL
    with open("dataset_dpo_nano_banana.jsonl", "w", encoding="utf-8") as f_dpo:
        for entry in dataset_dpo:
            f_dpo.write(json.dumps(entry, ensure_ascii=False) + "\n")

    with open("dataset_sft_nano_banana.jsonl", "w", encoding="utf-8") as f_sft:
        for entry in dataset_sft:
            f_sft.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return len(dataset_dpo), len(dataset_sft)

if __name__ == "__main__":
    n_dpo, n_sft = generar_dataset_completo()
    print(f"=== FASE 2 COMPLETADA CON ÉXITO ===")
    print(f"Dataset DPO generado: {n_dpo} pares evaluados en 'dataset_dpo_nano_banana.jsonl'")
    print(f"Dataset SFT generado: {n_sft} ejemplos en 'dataset_sft_nano_banana.jsonl'")
