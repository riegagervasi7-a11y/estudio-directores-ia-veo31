# Rúbrica Maestra: Taxonomía Fotográfica e Hiperrealismo Anti-IA
## Especificación Técnica para Google Nano Banana Pro

Esta rúbrica es el núcleo fundacional de conocimiento para el entrenamiento del generador de prompts y define las reglas que los **Jueces de Evaluación (Texto y Visión)** usarán para clasificar ejemplos en **Chosen (Aceptados)** y **Rejected (Rechazados)** para DPO / SFT.

---

## 1. La Lista Negra de Términos Tóxicos ("The Poison List")

Cualquier prompt que contenga estas palabras será penalizado de inmediato por el Juez de Texto. En los modelos de difusión y autorregresivos visuales, estos términos están sobreindexados en bases de datos de arte digital (ArtStation, DeviantArt, renderizadores 3D) y activan los pesos de acabado plástico y pulido artificial.

| Términos Prohibidos | Razón del Rechazo | Reemplazo Fotográfico Obligatorio |
| :--- | :--- | :--- |
| `hyperrealistic`, `photorealistic`, `ultra-realistic` | Activa filtros de suavizado digital y CGI. | Especificar cámara, sensor y lente (`shot on Sony A7IV, 85mm f/1.8`). |
| `8k`, `4k`, `UHD`, `high resolution` | Ruido semántico que produce artefactos de nitidez forzada (*over-sharpening*). | Mencionar profundidad de campo real y nitidez focal natural (`tack-sharp focus on the iris`). |
| `masterpiece`, `award-winning`, `trending on artstation` | Sesga hacia pintura digital e ilustración estilizada. | Especificar estilo documental o editorial (`candid editorial photography, raw unretouched documentary photo`). |
| `perfect skin`, `smooth skin`, `flawless` | Genera rostros de maniquí de plástico o cera. | Detallar microtextura epidérmica (`visible pores, natural skin micro-texture, fine peach fuzz, subtle blemishes`). |
| `cinematic lighting`, `dramatic rim light` (genérico) | Provoca la típica iluminación artificial de IA (luces de neón simétricas o brillo excesivo). | Describir fuentes de luz físicas reales (`diffused north-facing window light`, `harsh direct on-camera flash`). |

---

## 2. Taxonomía de las 7 Capas de Realismo Fotográfico

Para que un prompt sea aprobado con calificación **10/10**, debe construir la escena siguiendo estrictamente esta pila modular:

### Capa 1: Identidad y Micro-Expresiones
* **Evitar poses estáticas simétricas:** No solicitar "mirando a cámara sonriendo perfecto".
* **Humanidad dinámica:** Expresiones en movimiento (hablando, riendo a mitad de frase, ceño relajado, mirada ligeramente desviada a $15^\circ$ del lente, parpadeo sutil, sonrisa asimétrica natural).
* **Diversidad real:** Especificar edad exacta, ascendencia genética y constitución física sin generalizaciones.

### Capa 2: Micro-Imperfecciones Anatómicas (El factor #1 anti-cera)
* **Textura dérmica:** Poros visibles en mejillas y nariz, vello facial ultra sutil (*vellus hair / peach fuzz*), brillo natural por sebo en la zona T (frente y puente nasal).
* **Líneas gestuales:** Patas de gallo finas al sonreír, pliegues nasolabiales naturales, textura real en labios con ligeras grietas dérmicas.
* **Cabello orgánico:** Cabellos sueltos (*flyaway hairs* desordenados por la estática o viento), raíces con variación de tono, mechones individuales en lugar de un bloque de pelo sólido.

### Capa 3: Vestuario y Física de Materiales
* **Especificar textiles auténticos:** Lino con arrugas naturales, algodón pesado con tramado visible, lana con pequeñas motas de pelusa (*lint*), costuras visibles en cuello y botones.
* **Física del tejido:** La ropa debe reaccionar a la gravedad y postura (pliegues en las axilas, tensión en los hombros).

### Capa 4: Óptica y Geometría de Cámara
Nano Banana Pro responde con extrema precisión a parámetros ópticos. Se debe definir:
* **Distancia Focal:**
  * `85mm` o `105mm`: Para retrato con compresión de fondo natural y proporciones faciales exactas (sin distorsión de nariz).
  * `50mm`: Perspectiva del ojo humano para situaciones cotidianas.
  * `28mm` o `35mm`: Para fotos tipo reportaje o callejeras espontáneas.
* **Apertura de Diafragma:**
  * `f/1.8` - `f/2.8`: Bokeh óptico creíble (desenfoque progresivo, no recorte digital de software móvil).
  * `f/5.6` - `f/8.0`: Para escenas grupales o tomas de calle donde el entorno tiene contexto nítido.
* **Obturación e ISO:** `1/250s, ISO 400` para reducir sensación de renderizado sintético.

### Capa 5: Emulsión / Formato de Captura
* **Opción A (Analógica):** Película de 35mm con grano químico natural:
  * `Shot on Kodak Portra 400 (warm skin tones, fine organic grain)`.
  * `Shot on Cinestill 800T (cool tungsten shadows, subtle halation around bright practical lights)`.
* **Opción B (Digital Raw):**
  * `Unprocessed RAW file captured on Leica M11, natural dynamic range, unsharpened sensor noise`.

### Capa 6: Iluminación Física Coherente
* **El "Truco del Flash Directo":** Es el método más infalible contra el aspecto de IA. Usar frases como:
  * `Point-and-shoot direct flash photography, harsh direct flash casting a sharp dark shadow on the wall behind, candid party snapshot aesthetic`.
* **Luz Natural:**
  * `Overcast afternoon daylight, 5600K color temperature, soft natural shadow roll-off beneath the chin`.
  * `Direct harsh midday sunlight casting authentic hard-edged shadows, squinting slightly against the sun`.

### Capa 7: Composición y Entorno Orgánico
* **Imperfección en el encuadre:** Composición fuera de centro, corte intencional a la altura del hombro, ligera inclinación de cámara accidental.
* **Fondo con vida real:** No fondos vacíos o con desenfoque de ensueño infinito; incluir elementos mundanos fuera de foco (un vaso con condensación, cables de luz lejanos, una pared con textura de estuco desgastado).

---

## 3. Rúbrica de Puntuación para los Jueces

### Juez 1 (Texto - LLM Critic): Rango 0 a 10
* **Penalización (-3 pts por palabra):** Aparición de términos de la *Poison List*.
* **Penalización (-2 pts):** Falta de especificaciones ópticas (lente/apertura).
* **Penalización (-2 pts):** Falta de micro-imperfecciones explícitas de la piel o cabello.
* **Bonificación (+2 pts):** Especificación de emulsión analógica o sensor RAW con grano real.
* **Bonificación (+2 pts):** Iluminación realista documentada (flash directo o luz difusa natural).
* **Corte de aprobación:** $\ge 9.0$ puntos pasa a *Chosen*. Menor a $7.0$ se categoriza como *Rejected* para entrenamiento DPO.

### Juez 2 (Visión - VLM Critic): Auditoría Visual Forense
El modelo de visión evalúa la imagen generada por Nano Banana Pro con estas preguntas binarias:
1. ¿La piel parece porcelana/cera o muestra microporos y vello fino?
2. ¿Los ojos tienen reflejos de luz lógicamente alineados con las fuentes de la escena o tienen el "brillo vidrioso de IA"?
3. ¿Las manos, uñas y lóbulos de las orejas tienen volumen y textura consistentes?
4. ¿El bokeh del fondo parece un desenfoque Gaussiano digital o una aberración esférica de lente real?

---

## 4. Ejemplos de Entrenamiento (Pares DPO)

### Ejemplo 1: Retrato Femenino Casual

* **Prompt Rechazado (Rejected - Aspecto Típico de IA):**
  > *"Hyperrealistic beautiful 25 year old woman smiling at the camera in a coffee shop, 8k resolution, photorealistic, masterpiece, perfect lighting, ultra detailed skin, bokeh background, octane render, trending on artstation."*
  > *Fallo:* Plástico garantizado, ojos de muñeca, iluminación artificial irreal.

* **Prompt Elegido (Chosen - 100% Fotográfico):**
  > *"A candid 35mm film photograph of a 26-year-old woman looking away while taking a sip of iced coffee at an outdoor café table. Unposed, relaxed natural smile with slight squint. Visible skin micro-texture, natural pores on cheeks, fine flyaway strands of hair caught in a gentle breeze, peach fuzz along the jawline. Wearing a relaxed oversized beige linen shirt with authentic fabric weave and loose collar buttons. Shot on an 85mm lens at f/2.2, ISO 400 on Kodak Portra 400 film stock. Soft overcast ambient lighting with gentle shadow roll-off. Authentic subtle optical depth of field with blurred street background, slight film grain texture, unretouched aesthetic."*
  > *Resultado:* Foto orgánica con imperfecciones reales y física óptica.

---

### Ejemplo 2: Retrato Masculino con Flash Directo (Snapshot Realista)

* **Prompt Rechazado (Rejected):**
  > *"Handsome 30 year old man at a night party, photorealistic portrait, cinematic neon lighting, ultra detailed, 8k resolution, perfect handsome face."*

* **Prompt Elegido (Chosen):**
  > *"Point-and-shoot direct on-camera flash photograph of a 32-year-old man laughing mid-conversation in a dim hallway. Direct harsh flash creates realistic specular highlights on his forehead and nose, casting a sharp dark shadow on the off-white textured wall behind him. Natural skin sheen, light five o'clock shadow with individual stubble hairs, slightly crooked teeth visible during genuine laughter. Wearing a worn vintage denim jacket with frayed collar seams. Shot on a 35mm compact camera, f/4 aperture, slight motion softness at the edge of his raised hand, authentic 90s disposable camera snapshot aesthetic, fine color noise."*
