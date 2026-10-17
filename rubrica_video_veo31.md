# Rúbrica Maestra de Video: Image-to-Video (I2V) para Veo 3.1 y Higgsfield
## Modo Bestia (Llama-3.1-8B DPO)

Esta especificación técnica rige el entrenamiento del modelo de video para que transforme una imagen ancla y una acción deseada en un prompt cinematográfico que evite el derretimiento (*morphing*), los movimientos robóticos y los artefactos de IA.

---

## 1. La Regla de Oro del Image-to-Video (I2V)

En la generación de video a partir de un ancla:
> **"La imagen ancla ya define el rostro, la ropa, los poros y el lugar. NUNCA se deben volver a describir en el prompt de video."**

Si el prompt re-describe la apariencia física del personaje, el modelo de video intenta "redibujarlo" en cada frame, lo que genera:
* Derretimiento de rostro (*face melting*).
* Parpadeo de barba o peinado (*flickering*).
* Deformación de extremidades y manos.

---

## 2. Estructura Obligatoria de 3 Bloques

Todo prompt de video debe estructurarse en este orden exacto:

### Frase Inicial de Anclaje (Mandatoria)
`"Maintain the exact subject, facial identity, wardrobe, and environment from the first frame."`

### Bloque 1: CÁMARA (Va al inicio con su verbo de movimiento)
Veo 3.1 prioriza lo que lee al inicio. Debe describir un único movimiento físico de cámara con inercia de operador humano:
* **Verbos recomendados:** `Slow subtle push-in`, `Gentle lateral tracking`, `Steady tripod shot with minor handheld camera breath`, `Slow crane down`, `Low-angle static lock-off`.
* **Prohibido:** `Smooth cinematic camera zoom` (provoca movimiento irreal de dron digital).

### Bloque 2: SUJETO (Micro-acciones a velocidad humana)
Una sola acción física o micro-movimiento con su segundo exacto (`at second 2...`):
* Pestañeo natural, pecho elevándose con la respiración, exhalación con vaho en frío, leve cambio de peso corporal, giro lento de mirada.
* Sin gestos rápidos de manos (las manos son propensas a glitch).
* Sin caminar mientras habla (provoca deslizamiento de pies sobre el suelo).

### Bloque 3: ENTORNO e Iluminación Constante + Audio
* **Iluminación:** `"Lighting remains constant throughout the shot."` (evita que la luz fluctúe o parpadee).
* **Partículas:** Llovizna constante, humo sutil en suspensión, viento suave en la ropa.
* **Etiqueta `Audio:` obligatoria:** Veo 3.1 solo genera sonido ambiental si se incluye la etiqueta explícita:
  * `Audio: ambient sound of [viento, lluvia, motor, taller], subtle room tone, zero music, no voices.`

---

## 3. Lista Negra de Video ("Poison Words" de I2V)

Términos prohibidos que activan los defectos de renderizado y cámara falsa:
* `cinematic, smooth stabilized, hyperrealistic, ultra realistic, 8k, 4k, masterpiece, octane render, cgi, stunning, beautiful, perfect motion, fast zoom, drone shot`.

---

## 4. Rango de Longitud Óptima
* **Mínimo:** 50 palabras.
* **Máximo:** 180 palabras.
*(Los prompts de más de 200 palabras saturan la memoria de atención de Veo 3.1 y hacen que ignore las instrucciones de cámara).*
