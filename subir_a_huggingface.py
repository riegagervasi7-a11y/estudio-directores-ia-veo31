"""
subir_a_huggingface.py
Herramienta automatizada para subir todos los adaptadores LoRA entrenados a Hugging Face Hub.
Permite subir repositorios privados o públicos con metadatos y Model Cards automáticas.
"""

import os
import sys
from huggingface_hub import HfApi, login, create_repo

MODELOS_DISPONIBLES = [
    {
        "dir": "lora_video_maestro_5_formatos_8b",
        "repo_name": "llama3.1-8b-lora-video-maestro-5formatos",
        "descripcion": "Adaptador LoRA Maestro entrenado con DPO en Llama-3.1-8B para generar prompts de video de alta fidelidad en los 5 formatos virales (Talking Head, Podcast 3/4, UGC Selfie, Street Interview, Macro Producto) para Google Veo 3.1 y Nano Banana Pro."
    },
    {
        "dir": "lora_video_podcast_8b",
        "repo_name": "llama3.1-8b-lora-video-podcast-3-4",
        "descripcion": "Especialista LoRA en formato Podcast / Masterclass en ángulo 3/4 con Shure SM7B, óptica 85mm f/1.8 y mirada a 35° al entrevistador."
    },
    {
        "dir": "lora_video_ugc_8b",
        "repo_name": "llama3.1-8b-lora-video-ugc-creadores",
        "descripcion": "Especialista LoRA en formato UGC Testimonial / TikTok Shop con cámara selfie 24mm, micro-jitter humano y vicio de pantalla."
    },
    {
        "dir": "lora_dpo_nano_banana",
        "repo_name": "qwen2.5-3b-lora-dpo-nano-banana-pro",
        "descripcion": "Adaptador LoRA DPO para anclas fotográficas fotorrealistas sin artefactos de estudio ni alucinaciones en Google Nano Banana Pro."
    }
]

def main():
    print("=" * 75)
    print("   🚀 SUBIDA DE MODELOS LORA A HUGGING FACE HUB")
    print("=" * 75)
    print("Esta herramienta subirá tus modelos de 'modelo_entrenado/' a tu cuenta de Hugging Face.")
    print("Requisitos: Un token de Hugging Face con permisos de ESCRITURA ('Write').")
    print("Lo obtienes en: https://huggingface.co/settings/tokens\n")

    token = os.environ.get("HF_TOKEN", "").strip()
    if not token:
        token = input("Pega tu Hugging Face Write Token (hf_...): ").strip()

    if not token:
        print("❌ Error: Se requiere un token para autenticarse.")
        sys.exit(1)

    try:
        login(token=token, add_to_git_credential=True)
        api = HfApi(token=token)
        user_info = api.whoami()
        username = user_info["name"]
        print(f"\n✅ Autenticado exitosamente como: {username}")
    except Exception as e:
        print(f"❌ Error al autenticar en Hugging Face: {e}")
        sys.exit(1)

    es_privado = input("\n¿Deseas que los repositorios sean PRIVADOS? (s/n) [Default: s]: ").strip().lower() != 'n'

    base_dir = os.path.join(os.path.dirname(__file__), "modelo_entrenado")

    print("\n" + "=" * 75)
    print("Iniciando subida de adaptadores...")
    print("=" * 75)

    for item in MODELOS_DISPONIBLES:
        local_path = os.path.join(base_dir, item["dir"])
        if not os.path.exists(local_path):
            print(f"⚠️ Saltando {item['dir']} (no encontrado en disco local).")
            continue

        repo_id = f"{username}/{item['repo_name']}"
        print(f"\n📦 Subiendo [{item['dir']}] -> {repo_id}...")

        try:
            create_repo(repo_id=repo_id, repo_type="model", private=es_privado, exist_ok=True, token=token)

            # Generar README para el repo en Hugging Face
            readme_content = f"""---
license: llama3.1
tags:
- lora
- unsloth
- dpo
- text-generation
- video-generation
- google-veo
- nano-banana-pro
---

# {item['repo_name']}

{item['descripcion']}

## 🚀 Uso en Python / Kaggle / Colab
```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="{repo_id}",
    max_seq_length=2048,
    load_in_4bit=True
)
```
"""
            with open(os.path.join(local_path, "README.md"), "w", encoding="utf-8") as f:
                f.write(readme_content)

            api.upload_folder(
                folder_path=local_path,
                repo_id=repo_id,
                repo_type="model",
                commit_message="feat: Subida inicial de pesos LoRA entrenados con DPO"
            )
            print(f"🎉 ¡Subido con éxito! Ver en: https://huggingface.co/{repo_id}")

        except Exception as err:
            print(f"❌ Error al subir {item['dir']}: {err}")

    print("\n" + "=" * 75)
    print("✅ Proceso de subida a Hugging Face finalizado.")
    print("=" * 75)

if __name__ == "__main__":
    main()
