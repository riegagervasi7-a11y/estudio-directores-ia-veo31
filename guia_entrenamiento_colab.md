# Guía Práctica de Ejecución: Entrenamiento en Google Colab
## Modelo: Generador de Prompts Anti-IA para Google Nano Banana Pro

Esta guía detalla los pasos para ejecutar el entrenamiento en la nube utilizando **Google Colab** y la aceleración **Unsloth (GPU T4 Gratuita)**.

---

### Requisitos Previos
* Una cuenta de Google (Gmail).
* Navegador web (Chrome, Edge, Firefox, Safari).
* Los dos archivos generados en tu espacio de trabajo:
  1. [`entrenamiento_nano_banana_colab.ipynb`](file:///c:/Users/Gabo/Documents/entrenamiento%20de%20ai/entrenamiento_nano_banana_colab.ipynb)
  2. [`dataset_dpo_nano_banana.jsonl`](file:///c:/Users/Gabo/Documents/entrenamiento%20de%20ai/dataset_dpo_nano_banana.jsonl)

---

### Paso a Paso para Entrenar en la Web

#### 1. Abrir Google Colab
1. Entra en tu navegador a: **[colab.research.google.com](https://colab.research.google.com)**.
2. En la ventana emergente, selecciona la pestaña **Subir** (*Upload*).
3. Arrastra o selecciona el archivo: `entrenamiento_nano_banana_colab.ipynb`.

#### 2. Asegurar el Acelerador de GPU Gratuito
1. En el menú superior de Colab, ve a: **Entorno de ejecución** (*Runtime*) ➔ **Cambiar tipo de entorno de ejecución** (*Change runtime type*).
2. En **Acelerador de hardware** (*Hardware accelerator*), selecciona: **T4 GPU** (es gratuita).
3. Haz clic en **Guardar** (*Save*).

#### 3. Ejecutar las Celdas en Orden
Solo debes presionar el botón de **Play** ($\blacktriangleright$) en cada celda del cuaderno:

1. **Celda 1 (Instalación):** Instala `unsloth` y `trl`. Tarda aprox. **1 minuto**.
2. **Celda 2 (Cargar Modelo):** Descarga `Qwen2.5-3B-Instruct` cuantizado en 4-bit. Tarda aprox. **2 minutos**.
3. **Celda 3 (Configurar LoRA):** Prepara los adaptadores de bajo rango. Tarda **5 segundos**.
4. **Celda 4 (Cargar Dataset):** Te pedirá subir un archivo. Haz clic en *"Seleccionar archivos"* y sube `dataset_dpo_nano_banana.jsonl`.
5. **Celda 5 (Entrenamiento DPO):** Inicia el entrenamiento con `DPOTrainer`.
   * **Tiempo de ejecución:** Entre **10 y 15 minutos**.
   * Verás cómo el valor de `loss` desciende progresivamente a medida que el modelo aprende a descartar el aspecto de IA.
6. **Celda 6 (Prueba en Vivo):** Genera un prompt en tiempo real a partir de cualquier idea que escribas.
7. **Celda 7 (Descarga del Modelo):** Empaqueta los pesos LoRA entrenados (`lora_dpo_nano_banana.zip`) y los descarga a tu computadora para conservarlos de por vida.

---

### ¿Cómo Usar los Prompts en Google Nano Banana Pro?

1. Tomas el texto generado en la **Celda 6**.
2. Abres Google Nano Banana Pro (en Google AI Studio o en la interfaz de Gemini 3 Pro Image).
3. Pegas el prompt completo en inglés.
4. **Resultado esperado:**
   * Cero aspecto plástico.
   * Textura visible de poros y vello sutil (*peach fuzz*).
   * Reflejos corneales coherentes.
   * Grano óptico y física de lente real (85mm / 35mm / película analógica).
