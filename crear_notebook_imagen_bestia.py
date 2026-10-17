"""
crear_notebook_imagen_bestia.py
Genera el cuaderno de Google Colab para entrenar la IA de Imagen (Nano Banana Pro)
en "Modo Bestia": Llama-3.1-8B + LoRA r=32 + DPO especializada en Spots Publicitarios,
Avatares de Presentadores a Cámara, y Supresión Total de Equipos y Marcas de Agua.
"""

import json

notebook = {
    "nbformat": 4,
    "nbformat_minor": 0,
    "metadata": {
        "colab": {
            "name": "Entrenamiento_Imagen_Comercial_Modo_Bestia_8B.ipynb",
            "provenance": [],
            "gpuType": "T4"
        },
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
                "# 🔥 MODO BESTIA: IA de Imagen Publicitaria para Google Nano Banana Pro\n",
                "### Especialización: Spots Publicitarios, Presentadores Comerciales y Avatares de Video\n",
                "### Modelo Base: Meta-Llama-3.1-8B-Instruct | LoRA Rank = 32 | Contexto = 2048 Tokens\n",
                "\n",
                "Este cuaderno entrena a **Llama 3.1 (8B)** mediante **DPO (Direct Preference Optimization)** para erradicar los 5 vicios del prompting comercial:\n",
                "1. **Cero Lámparas en el Cuadro:** Obliga a que la luz sea *off-camera* y prohíbe pintar softboxes o trípodes.\n",
                "2. **Cero Marcas de Agua:** Elimina el estampado de datos EXIF numéricos en la esquina.\n",
                "3. **Cero Envejecimiento Artificial:** Rostros de 30 años con piel sana, luminosa y poros reales sin arrugas profundas.\n",
                "4. **Boca Cerrada en Reposo (Lip-Sync Ready):** Postura neutra y confiada indispensable para animación en Veo 3.1.\n",
                "5. **Cero Plástico IA:** Ni piel de cera 3D ni clichés de 'photorealistic 8k'."
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Paso 1: Instalación de Unsloth y Dependencias de Alto Rendimiento\n",
                "Ejecuta esta celda para preparar el entorno optimizado en la GPU T4."
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
                "Cargamos los 8.000 millones de parámetros cuantizados para aprovechar el 85% de la GPU T4 (~12.5 GB)."
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
                "print(\"✅ Meta-Llama-3.1-8B cargado exitosamente en GPU.\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Paso 3: Configurar Adaptadores LoRA de Alta Capacidad (Modo Bestia: r = 32, alpha = 64)\n",
                "Entrenamos todas las proyecciones lineales (`q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`)."
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
                "print(\"✅ Adaptadores LoRA r=32 configurados en Modo Bestia.\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Paso 4: Cargar Dataset Comercial DPO (`dataset_comercial_dpo.jsonl`)\n",
                "Sube el archivo `dataset_comercial_dpo.jsonl` generado para entrenar las preferencias comerciales."
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "import os\n",
                "import json\n",
                "from google.colab import files\n",
                "from datasets import Dataset\n",
                "\n",
                "if not os.path.exists(\"dataset_comercial_dpo.jsonl\"):\n",
                "    print(\"Por favor, sube el archivo 'dataset_comercial_dpo.jsonl':\")\n",
                "    uploaded = files.upload()\n",
                "\n",
                "data_list = []\n",
                "with open(\"dataset_comercial_dpo.jsonl\", \"r\", encoding=\"utf-8\") as f:\n",
                "    for line in f:\n",
                "        item = json.loads(line)\n",
                "        data_list.append({\n",
                "            \"prompt\": item[\"prompt\"],\n",
                "            \"chosen\": item[\"chosen\"],\n",
                "            \"rejected\": item[\"rejected\"]\n",
                "        })\n",
                "\n",
                "dataset = Dataset.from_list(data_list)\n",
                "print(f\"✅ Dataset Comercial cargado: {len(dataset)} pares de entrenamiento DPO.\")\n",
                "print(\"Ejemplo Chosen:\\n\", dataset[0]['chosen'][:200], \"...\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Paso 5: Entrenamiento DPO en Modo Bestia\n",
                "Entrenamos con `DPOTrainer` castigando matemáticamente softboxes en el plano, marcas de agua y bocas abiertas."
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
                "    output_dir=\"./resultados_imagen_bestia\",\n",
                "    beta=0.1,  # Castigo de divergencia hacia vicios rechazados\n",
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
                "gpu_total = torch.cuda.get_device_properties(0).total_memory / 1024**3\n",
                "print(f\"📊 VRAM Inicial: {gpu_mem_used:.2f} GB / {gpu_total:.2f} GB\")\n",
                "\n",
                "print(\"🔥 Iniciando entrenamiento Modo Bestia para Imagen Comercial... Duración aprox: 18-20 minutos.\")\n",
                "stats = dpo_trainer.train()\n",
                "\n",
                "gpu_mem_peak = torch.cuda.max_memory_allocated() / 1024**3\n",
                "print(f\"🎉 ¡Entrenamiento completado! VRAM Máxima aprovechada: {gpu_mem_peak:.2f} GB / {gpu_total:.2f} GB\")"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Paso 6: Prueba en Vivo de Inferencia Comercial\n",
                "Probamos la IA entrenada para generar un prompt de ancla publicitaria a cámara."
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "FastLanguageModel.for_inference(model)\n",
                "\n",
                "def generar_prompt_ancla_comercial(idea_es):\n",
                "    prompt_in = f\"Generate a commercial advertising portrait prompt for an AI presenter: {idea_es}\"\n",
                "    messages = [\n",
                "        {\"role\": \"user\", \"content\": prompt_in}\n",
                "    ]\n",
                "    inputs = tokenizer.apply_chat_template(\n",
                "        messages,\n",
                "        tokenize=True,\n",
                "        add_generation_prompt=True,\n",
                "        return_tensors=\"pt\"\n",
                "    ).to(\"cuda\")\n",
                "\n",
                "    outputs = model.generate(\n",
                "        input_ids=inputs,\n",
                "        max_new_tokens=300,\n",
                "        temperature=0.6,\n",
                "        use_cache=True,\n",
                "        do_sample=True\n",
                "    )\n",
                "    respuesta = tokenizer.batch_decode(outputs[:, inputs.shape[1]:], skip_special_tokens=True)[0]\n",
                "    return respuesta.strip()\n",
                "\n",
                "idea_prueba = \"Presentadora financiera de 32 años en sede bancaria moderna con traje sastre azul marino\"\n",
                "print(\"PROMPT COMERCIAL GENERADO POR TU IA EN MODO BESTIA:\\n\")\n",
                "print(generar_prompt_ancla_comercial(idea_prueba))"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Paso 7: Guardar y Descargar los Pesos LoRA (`lora_imagen_comercial_8b.zip`)\n",
                "Empaquetamos el adaptador entrenado y lo descargamos automáticamente a tu computadora."
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "execution_count": None,
            "outputs": [],
            "source": [
                "import shutil\n",
                "from google.colab import files\n",
                "\n",
                "output_dir = \"lora_imagen_comercial_8b\"\n",
                "model.save_pretrained(output_dir)\n",
                "tokenizer.save_pretrained(output_dir)\n",
                "\n",
                "shutil.make_archive(output_dir, 'zip', output_dir)\n",
                "print(f\"📦 Modelo comprimido como '{output_dir}.zip'. Iniciando descarga automática...\")\n",
                "files.download(f\"{output_dir}.zip\")"
            ]
        }
    ]
}

with open("entrenamiento_imagen_comercial_modo_bestia_colab.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=2, ensure_ascii=False)

print("[OK] Cuaderno 'entrenamiento_imagen_comercial_modo_bestia_colab.ipynb' creado exitosamente.")
