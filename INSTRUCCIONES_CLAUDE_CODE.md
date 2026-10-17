# Instrucciones para tu Sesión de Claude Code

Para ejecutar este ciclo completo desde tu terminal con **Claude Code**:

### 1. Abre tu terminal en esta carpeta:
```powershell
cd "c:\Users\Gabo\Documents\entrenamiento de ai"
claude
```

### 2. Escribe esta orden exacta a Claude Code:

> *"Actúa como orquestador de pruebas para nuestro generador de prompts de Google Nano Banana Pro. Realiza el siguiente flujo:*
> *1. Piensa en una idea humana compleja que suela delatar a las IA (ej. un anciano artesano con arrugas y manos con textura, o un retrato con flash directo nocturno).*
> *2. Ejecuta `python pipeline_claude_google.py --idea "<tu idea>"` para obtener el prompt maestro.*
> *3. Revisa el archivo `ultimo_prompt.txt` generado.*
> *4. Si tienes acceso a Google Flow o una imagen generada en `ultima_imagen.png`, inspecciónala con tu visión y emite una crítica forense: ¿Tiene piel de cera? ¿Reflejos oculares creíbles? ¿Puntuación del 1 al 10 en realismo fotográfico?"*

---

### ¿Cómo opera Claude Code durante la sesión?
* Claude Code llamará a `pipeline_claude_google.py`.
* Nuestro modelo le devolverá el prompt fotográfico de 7 capas en `ultimo_prompt.txt`.
* Cuando la imagen esté generada en Google (o si tienes configurado `GEMINI_API_KEY` en tu entorno), Claude Code abrirá la imagen, la mirará con su propia visión multimodal y te escribirá en la terminal el reporte forense completo.
