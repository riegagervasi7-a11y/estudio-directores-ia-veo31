"""
crear_notebook_kaggle.py
Genera el cuaderno de Kaggle optimizado para GPU T4 x2 para entrenar los
modelos especialistas en los 5 Formatos de Video Corto (Meta-Llama-3.1-8B).
"""

import json

notebook = {
    "nbformat": 4,
    "nbformat_minor": 0,
    "metadata": {
        "kernelspec": {
            "name": "python3",
            "display_name": "Python 3"
        },
        "language_info": {
            "name": "python"
        },
        "accelerator": "GPU"
    },
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 🔥 MODO BESTIA EN KAGGLE: Suite de 5 Formatos de Video Corto para Veo 3.1\n",
                "### Plataforma: Kaggle Dual GPU (T4 x2) | Modelo: Meta-Llama-3.1-8B-Instruct | LoRA r=32\n",
                "\n",
                "Este cuaderno entrena una IA especialista en los 5 formatos más virales de video corto:\n",
                "1. **Talking Head Comercial** (Anuncio B2B/B2C, mirada al lente, cejas activas, 50mm f/2.8).\n",
                "2. **Podcast / Masterclass 3/4** (Ángulo 3/4, Shure SM7B, mirada al entrevistador, 85mm f/1.8).\n",
                "3. **Testimonial UGC** (Cámara en mano selfie 24mm, mirada pantalla/lente, jitter orgánico).\n",
                "4. **Entrevista Callejera (Vox Pop)** (Cámara 28mm f/5.6, micrófono de mano, turnos limpios).\n",
                "5. **Demostración de Producto Macro** (100mm macro f/4, slider, hook de impacto físico en s0-2).\n",
                "\n",
                "> **Importante:** Asegúrate de tener **Internet ON** y el acelerador en **GPU T4 x2** en el panel derecho."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Paso 1: Instalación de Unsloth en Kaggle"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "%%capture\n",
                "!pip install \"unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git\"\n",
                "!pip install --no-deps trl peft accelerate bitsandbytes datasets"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Paso 2: Cargar Meta-Llama-3.1-8B-Instruct en 4-Bit\n",
                "Aprovechamos la memoria HBM de la T4 con cuantización 4-bit de alta velocidad."
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "from unsloth import FastLanguageModel\n",
                "import torch\n",
                "\n",
                "max_seq_length = 2048\n",
                "dtype = None\n",
                "load_in_4bit = True\n",
                "\n",
                "model, tokenizer = FastLanguageModel.from_pretrained(\n",
                "    model_name=\"unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit\",\n",
                "    max_seq_length=max_seq_length,\n",
                "    dtype=dtype,\n",
                "    load_in_4bit=load_in_4bit,\n",
                ")\n",
                "\n",
                "print(\"✅ Meta-Llama-3.1-8B cargado exitosamente en Kaggle.\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Paso 3: Configurar Adaptadores LoRA de Alta Capacidad (Modo Bestia: r = 32, alpha = 64)"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "model = FastLanguageModel.get_peft_model(\n",
                "    model,\n",
                "    r=32,\n",
                "    lora_alpha=64,\n",
                "    target_modules=[\"q_proj\", \"k_proj\", \"v_proj\", \"o_proj\", \"gate_proj\", \"up_proj\", \"down_proj\"],\n",
                "    lora_dropout=0,\n",
                "    bias=\"none\",\n",
                "    use_gradient_checkpointing=\"unsloth\",\n",
                "    random_state=3407,\n",
                ")\n",
                "\n",
                "print(\"✅ LoRA r=32 configurado para entrenamiento de video corto.\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Paso 4: Selección del Formato y Carga del Dataset\n",
                "Puedes entrenar el **Dataset Maestro (los 5 formatos unificados)** o un especialista individual.\n",
                "Elige la opción que prefieras:"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "# Elige qué quieres entrenar:\n",
                "# Opciones: 'maestro_5_formatos', 'talkinghead', 'podcast', 'ugc', 'street', 'product'\n",
                "SELECCION_FORMATO = 'maestro_5_formatos'\n",
                "\n",
                "import os\n",
                "import json\n",
                "from datasets import Dataset\n",
                "\n",
                "nombre_archivo = f\"dataset_video_{SELECCION_FORMATO}_dpo.jsonl\" if SELECCION_FORMATO == 'maestro_5_formatos' else f\"dataset_dpo_{SELECCION_FORMATO}.jsonl\"\n",
                "\n",
                "if not os.path.exists(nombre_archivo):\n",
                "    print(f\"⚠️ No se encontró {nombre_archivo} en la raíz. Por favor sube el archivo a /kaggle/working/ o al panel de datos.\")\n",
                "else:\n",
                "    data_list = []\n",
                "    with open(nombre_archivo, \"r\", encoding=\"utf-8\") as f:\n",
                "        for line in f:\n",
                "            item = json.loads(line)\n",
                "            data_list.append({\n",
                "                \"prompt\": item[\"prompt\"],\n",
                "                \"chosen\": item[\"chosen\"],\n",
                "                \"rejected\": item[\"rejected\"]\n",
                "            })\n",
                "    dataset = Dataset.from_list(data_list)\n",
                "    print(f\"✅ Dataset cargado: {len(dataset)} pares DPO para formato '{SELECCION_FORMATO}'.\")\n",
                "    print(\"\\nEjemplo Chosen:\", dataset[0]['chosen'][:200], \"...\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Paso 5: Entrenamiento DPO en Kaggle\n",
                "Configuración optimizada para exprimir la GPU T4 de Kaggle con estabilidad de 30 horas."
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "from trl import DPOTrainer, DPOConfig\n",
                "from unsloth import is_bfloat16_supported\n",
                "\n",
                "dpo_config = DPOConfig(\n",
                "    output_dir=\"./resultados_kaggle_video\",\n",
                "    beta=0.1,\n",
                "    learning_rate=5e-5,\n",
                "    lr_scheduler_type=\"cosine\",\n",
                "    per_device_train_batch_size=2,\n",
                "    gradient_accumulation_steps=4,\n",
                "    num_train_epochs=3,\n",
                "    warmup_ratio=0.1,\n",
                "    fp16=not is_bfloat16_supported(),\n",
                "    bf16=is_bfloat16_supported(),\n",
                "    logging_steps=5,\n",
                "    save_strategy=\"no\",\n",
                "    seed=3407,\n",
                ")\n",
                "\n",
                "dpo_trainer = DPOTrainer(\n",
                "    model=model,\n",
                "    ref_model=None,\n",
                "    args=dpo_config,\n",
                "    train_dataset=dataset,\n",
                "    tokenizer=tokenizer,\n",
                "    max_length=max_seq_length,\n",
                "    max_prompt_length=512,\n",
                ")\n",
                "\n",
                "gpu_mem_used = torch.cuda.memory_allocated() / 1024**3\n",
                "print(f\"📊 VRAM Inicial: {gpu_mem_used:.2f} GB\")\n",
                "print(\"🔥 Iniciando entrenamiento DPO en Kaggle... (Duración aprox: 15-18 minutos)\")\n",
                "stats = dpo_trainer.train()\n",
                "print(\"🎉 ¡Entrenamiento completado con éxito en Kaggle!\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Paso 6: Guardar y Empaquetar el Modelo en `/kaggle/working/`\n",
                "El modelo comprimido aparecerá en el panel lateral derecho de Kaggle (*Output*), listo para descargar con 1 clic."
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "import shutil\n",
                "\n",
                "output_dir = f\"lora_video_{SELECCION_FORMATO}_8b\"\n",
                "model.save_pretrained(output_dir)\n",
                "tokenizer.save_pretrained(output_dir)\n",
                "\n",
                "shutil.make_archive(output_dir, 'zip', output_dir)\n",
                "print(f\"📦 Modelo empaquetado como '{output_dir}.zip' en /kaggle/working/.\")\n",
                "print(\"👉 Ya puedes descargarlo desde la pestaña 'Output' a la derecha de Kaggle.\")"
            ]
        }
    ]
}

with open("entrenamiento_kaggle_5_formatos_modo_bestia.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("[OK] Cuaderno 'entrenamiento_kaggle_5_formatos_modo_bestia.ipynb' creado exitosamente.")
