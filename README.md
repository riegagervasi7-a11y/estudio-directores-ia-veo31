# 🎬 Estudio Multi-Agente de Directores IA (Nano Banana Pro & Veo 3.1)

Sistema integral de ingeniería de prompts, fine-tuning y orquestación multi-agente para generación publicitaria y clips virales con avatares fotorrealistas en **Google Nano Banana Pro** (Anclas fotográficas I2V) y **Google Veo 3.1 / Google Flow** (Video cinematográfico).

---

## 🏗️ Arquitectura del Sistema

El pipeline implementa una arquitectura modular con un **Director General (Router Inteligente)** y 5 Subagentes Especialistas entrenados con DPO (*Direct Preference Optimization*) sobre `Meta-Llama-3.1-8B-Instruct`:

1. **🎬 Subagente 1: Talking Head Comercial (B2B/B2C)**
   - Óptica: 50mm f/2.8 full-frame a nivel de ojos.
   - Dinámica: Cejas activas modulando la voz, micro-sacadas oculares, boca relajada en el frame inicial.
2. **🎙️ Subagente 2: Podcast / Masterclass 3/4**
   - Óptica: 85mm f/1.8 con bokeh cremoso y bombillas Edison a 2700K.
   - Dinámica: Shure SM7B rígido a 10 cm de la boca; mirada a 35° al entrevistador (nunca al lente).
3. **📱 Subagente 3: UGC & Creadores (TikTok Shop / Reels)**
   - Óptica: 24mm cámara frontal selfie a la distancia del brazo.
   - Dinámica: *Micro-jitter* de mano humana, vicio de pantalla (mira la pantalla y clava el lente en el punchline), manos anatómicas de 5 dedos.
4. **🎤 Subagente 4: Entrevista Callejera (Vox Pop)**
   - Óptica: 28mm f/5.6 con profundidad de calle y transeúntes consistentes.
   - Dinámica: Micrófono dinámico con cubo sólido; turnos de habla limpios sin solapar voces (sorpresa -> pensamiento -> respuesta).
5. **💎 Subagente 5: Demostración de Producto Macro**
   - Óptica: 100mm macro f/4 sobre slider motorizado con speed ramp.
   - Dinámica: Hook físico de impacto (agua/splash) en s0-2, integridad física sin morphing.

---

## 🖥️ Interfaz Gráfica Local (GUI)

El proyecto incluye un servidor de estudio local integrado:
- **Ejecutar:** Doble clic en `iniciar_estudio.bat` o `python servidor_gui.py`.
- **URL:** `http://localhost:7860`
- **Funcionalidades:**
  - Selector interactivo de directores y router inteligente.
  - Generador de doble tarjeta: Ancla Fotográfica + Video I2V con copiado al portapapeles de 1 clic.
  - Sala de chat en vivo con los directores potenciada por `gemini-3.8-flash`.
  - Monitor local de adaptadores LoRA instalados.

---

## 📦 Modelos y Checkpoints LoRA (Hugging Face)

Los adaptadores LoRA (r=32, alpha=64) entrenados con Unsloth en Kaggle Dual GPU (T4 x2) se alojan en Hugging Face Hub:
- `lora_video_maestro_5_formatos_8b`: Suite unificada de los 5 formatos de video corto.
- `lora_video_podcast_8b`: Especialista en podcast 3/4 y storytelling con SM7B.
- `lora_video_ugc_8b`: Especialista en video selfie y TikTok Shop.
- `lora_dpo_nano_banana`: Calibrador fotorrealista anti-alucinación para Nano Banana Pro.

---

## 🚀 Cuadernos de Entrenamiento (Kaggle)

Todos los cuadernos son 100% autónomos (auto-generan los datasets DPO en memoria):
- `entrenamiento_kaggle_5_formatos_modo_bestia.ipynb` (Modelo Maestro)
- `entrenamiento_kaggle_subagente_ugc.ipynb` (Subagente UGC)
- `entrenamiento_kaggle_subagente_street.ipynb` (Subagente Vox Pop)

---

## 🛠️ Requisitos e Instalación

```bash
git clone https://github.com/tu-usuario/estudio-directores-ia-veo31.git
cd estudio-directores-ia-veo31
pip install -r requirements.txt
python servidor_gui.py
```
