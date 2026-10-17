"""
servidor_gui.py
Interfaz Gráfica de Producción y Chat para el Estudio Multi-Agente de Directores IA.
Conecta con los modelos entrenados (Podcast, Maestro 5 Formatos, Nano Banana Pro),
el Router Inteligente, y el motor de conversación Gemini 3.8 Flash.
"""

import os
import sys
import json
import subprocess
import webbrowser
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from typing import Dict, Any

# Asegurar codificacion UTF-8 en consola de Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from equipo_directores_ia import DirectorGeneralRouter
except ImportError:
    try:
        from brain.directores.equipo_directores_ia import DirectorGeneralRouter
    except ImportError:
        sys.path.insert(0, r"c:\Users\Gabo\Documents\entrenamiento de ai")
        from equipo_directores_ia import DirectorGeneralRouter

# Cargar API Key si existe en .env
GEMINI_KEY = ""
env_paths = [".env", os.path.join(r"c:\Users\Gabo\Documents\entrenamiento de ai", ".env"), os.path.join(r"C:\Users\Gabo\Documents\cerebro-hibrido-v2", ".env")]
for ep in env_paths:
    if os.path.exists(ep):
        with open(ep, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    GEMINI_KEY = line.strip().split("=", 1)[1].strip()
                    break
        if GEMINI_KEY:
            break

# Inicializar Router de Directores
router = DirectorGeneralRouter()

def llamar_gemini(system_prompt: str, user_message: str) -> str:
    """Llama a Gemini 3.8 Flash para el modo Chat y refinamiento de prompts."""
    if not GEMINI_KEY:
        return "⚠️ Clave GEMINI_API_KEY no encontrada en .env."
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_KEY)
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=f"System Prompt: {system_prompt}\n\nUser Message: {user_message}"
        )
        return response.text.strip()
    except Exception as e:
        return f"Error al consultar Gemini: {str(e)}"

def copiar_a_portapapeles(texto: str) -> bool:
    """Copia texto al portapapeles de Windows de forma segura."""
    try:
        cmd = f'Set-Clipboard -Value @\'\n{texto}\n\'@'
        subprocess.run(['powershell', '-NoProfile', '-Command', cmd], check=True)
        return True
    except Exception:
        try:
            p = subprocess.Popen(['clip'], stdin=subprocess.PIPE, shell=True)
            p.communicate(input=texto.encode('utf-8'))
            return True
        except Exception:
            return False

def obtener_estado_modelos() -> Dict[str, Any]:
    """Escanea la carpeta modelo_entrenado/ para reportar los LoRAs listos."""
    base_dir = os.path.join(os.path.dirname(__file__), "modelo_entrenado")
    if not os.path.exists(base_dir):
        base_dir = r"c:\Users\Gabo\Documents\entrenamiento de ai\modelo_entrenado"
    modelos = []
    if os.path.exists(base_dir):
        for entry in os.listdir(base_dir):
            full_path = os.path.join(base_dir, entry)
            if os.path.isdir(full_path):
                safetensors = os.path.join(full_path, "adapter_model.safetensors")
                has_weights = os.path.exists(safetensors)
                size_mb = round(os.path.getsize(safetensors) / (1024 * 1024), 1) if has_weights else 0
                modelos.append({
                    "nombre": entry,
                    "activo": has_weights,
                    "tamano_mb": size_mb,
                    "ruta": full_path
                })
    return {
        "modelos": modelos,
        "hardware": "AMD Radeon RX 580 | 32 GB RAM",
        "gemini_disponible": bool(GEMINI_KEY)
    }

if os.path.exists(os.path.join(os.path.dirname(__file__), "proyecto_activo.txt")):
    CEREBRO_V2_DIR = os.path.dirname(__file__)
else:
    CEREBRO_V2_DIR = r"C:\Users\Gabo\Documents\cerebro-hibrido-v2"

def obtener_datos_cerebro() -> Dict[str, Any]:
    if not os.path.exists(CEREBRO_V2_DIR):
        return {"disponible": False}
    
    prj_file = os.path.join(CEREBRO_V2_DIR, "proyecto_activo.txt")
    proyecto_activo = "desconocido"
    if os.path.exists(prj_file):
        with open(prj_file, "r", encoding="utf-8") as f:
            proyecto_activo = f.read().strip()
    
    shotlist_path = os.path.join(CEREBRO_V2_DIR, "proyectos", proyecto_activo, "shotlist.json")
    shots = []
    if os.path.exists(shotlist_path):
        try:
            with open(shotlist_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                shots = data.get("shots", [])
        except Exception:
            pass
            
    return {
        "disponible": True,
        "ruta": CEREBRO_V2_DIR,
        "proyecto_activo": proyecto_activo,
        "total_shots": len(shots),
        "shots": shots
    }

def actualizar_shot_cerebro(shot_id: str, ancla: str, video: str, formato: str = None) -> bool:
    datos = obtener_datos_cerebro()
    if not datos.get("disponible"):
        return False
    prj = datos.get("proyecto_activo")
    shotlist_path = os.path.join(CEREBRO_V2_DIR, "proyectos", prj, "shotlist.json")
    if not os.path.exists(shotlist_path):
        return False
    try:
        with open(shotlist_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for s in data.get("shots", []):
            if s.get("id") == shot_id:
                if ancla:
                    s["anchor_prompt"] = ancla
                if video:
                    s["video_prompt_completo"] = video
                if formato:
                    s["formato"] = formato
                break
        with open(shotlist_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="es" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Estudio de Directores IA • Video Corto & Nano Banana</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace'],
          },
          colors: {
            brand: {
              50: '#eef2ff',
              500: '#6366f1',
              600: '#4f46e5',
              700: '#4338ca',
            },
            dark: {
              950: '#090d16',
              900: '#0f172a',
              850: '#141e33',
              800: '#1e293b',
              700: '#334155',
            }
          }
        }
      }
    }
  </script>
  <style>
    body { background-color: #090d16; color: #f1f5f9; }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #475569; }
    .glass { background: rgba(15, 23, 42, 0.75); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }
    .glow-purple { box-shadow: 0 0 25px -5px rgba(99, 102, 241, 0.25); }
    .agent-active { border-color: #6366f1 !important; background: rgba(99, 102, 241, 0.12) !important; }
  </style>
</head>
<body class="min-h-screen flex flex-col font-sans antialiased text-slate-100">

  <!-- HEADER -->
  <header class="glass sticky top-0 z-50 border-b border-slate-800/80 px-6 py-3.5 flex items-center justify-between">
    <div class="flex items-center space-x-4">
      <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 via-indigo-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-indigo-500/20 font-extrabold text-xl">
        🎬
      </div>
      <div>
        <div class="flex items-center space-x-2.5">
          <h1 class="text-lg font-bold tracking-tight text-white">Estudio de Directores IA</h1>
          <span class="px-2 py-0.5 text-[11px] font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 rounded-full">Modo Bestia v2.0</span>
        </div>
        <p class="text-xs text-slate-400">Pipeline Nano Banana Pro (Ancla) + Google Veo 3.1 / Flow (I2V)</p>
      </div>
    </div>

    <!-- Live System Badges -->
    <div class="flex items-center space-x-3 text-xs">
      <div id="badge-cerebro" class="hidden sm:flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-indigo-500/40 text-indigo-300">
        <span class="w-2 h-2 rounded-full bg-indigo-400 animate-pulse"></span>
        <span id="txt-cerebro">Cerebro: Conectando...</span>
      </div>
      <div id="badge-modelos" class="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span id="txt-modelos">Detectando modelos...</span>
      </div>
      <div class="hidden md:flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-400">
        <span>💻 AMD RX 580 (Local)</span>
      </div>
      <button onclick="cambiarTab('modelos')" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition font-medium flex items-center space-x-1.5">
        <span>📦 Ver Modelos</span>
      </button>
    </div>
  </header>

  <!-- MAIN WRAPPER -->
  <div class="flex-1 flex overflow-hidden">

    <!-- SIDEBAR: SELECTOR DE AGENTES DIRECTORES -->
    <aside class="w-80 border-r border-slate-800/80 bg-dark-950 p-4 flex flex-col space-y-4 overflow-y-auto">
      <div>
        <span class="text-[11px] font-bold uppercase tracking-wider text-slate-500 px-2">Subagentes Entrenados</span>
      </div>

      <nav class="space-y-1.5 flex-1" id="lista-agentes">
        <!-- Director General -->
        <button onclick="seleccionarAgente('auto')" id="btn-agente-auto" class="w-full text-left p-3 rounded-xl border border-slate-800/80 hover:border-slate-700 bg-dark-900 transition flex items-start space-x-3 agent-active">
          <span class="text-2xl mt-0.5">🧠</span>
          <div>
            <div class="text-sm font-semibold text-white flex items-center justify-between">
              <span>Director General</span>
              <span class="text-[10px] bg-indigo-500/20 text-indigo-300 px-1.5 py-0.5 rounded">Router</span>
            </div>
            <p class="text-xs text-slate-400 mt-0.5">Auto-enruta la idea al especialista óptico ideal.</p>
          </div>
        </button>

        <!-- Podcast 3/4 -->
        <button onclick="seleccionarAgente('podcast')" id="btn-agente-podcast" class="w-full text-left p-3 rounded-xl border border-slate-800/80 hover:border-slate-700 bg-dark-900 transition flex items-start space-x-3">
          <span class="text-2xl mt-0.5">🎙️</span>
          <div>
            <div class="text-sm font-semibold text-white flex items-center justify-between">
              <span>Podcast & Storytelling</span>
              <span class="text-[10px] bg-emerald-500/20 text-emerald-300 px-1.5 py-0.5 rounded">LoRA Listo</span>
            </div>
            <p class="text-xs text-slate-400 mt-0.5">85mm f/1.8, Shure SM7B, mirada 35° al entrevistador.</p>
          </div>
        </button>

        <!-- Talking Head -->
        <button onclick="seleccionarAgente('talkinghead')" id="btn-agente-talkinghead" class="w-full text-left p-3 rounded-xl border border-slate-800/80 hover:border-slate-700 bg-dark-900 transition flex items-start space-x-3">
          <span class="text-2xl mt-0.5">🎬</span>
          <div>
            <div class="text-sm font-semibold text-white">Talking Head Comercial</div>
            <p class="text-xs text-slate-400 mt-0.5">50mm f/2.8, mirada al lente, cejas activas, sin congelar.</p>
          </div>
        </button>

        <!-- UGC Creadores -->
        <button onclick="seleccionarAgente('ugc')" id="btn-agente-ugc" class="w-full text-left p-3 rounded-xl border border-slate-800/80 hover:border-slate-700 bg-dark-900 transition flex items-start space-x-3">
          <span class="text-2xl mt-0.5">📱</span>
          <div>
            <div class="text-sm font-semibold text-white flex items-center justify-between">
              <span>UGC & TikTok Shop</span>
              <span class="text-[10px] bg-emerald-500/20 text-emerald-300 px-1.5 py-0.5 rounded">LoRA Listo</span>
            </div>
            <p class="text-xs text-slate-400 mt-0.5">24mm selfie, micro-jitter, vicio de pantalla, 5 dedos.</p>
          </div>
        </button>

        <!-- Entrevista Callejera -->
        <button onclick="seleccionarAgente('street')" id="btn-agente-street" class="w-full text-left p-3 rounded-xl border border-slate-800/80 hover:border-slate-700 bg-dark-900 transition flex items-start space-x-3">
          <span class="text-2xl mt-0.5">🎤</span>
          <div>
            <div class="text-sm font-semibold text-white">Entrevista Callejera (Vox Pop)</div>
            <p class="text-xs text-slate-400 mt-0.5">28mm f/5.6, mic de mano, turnos de habla sin solapar.</p>
          </div>
        </button>

        <!-- Producto Macro -->
        <button onclick="seleccionarAgente('product')" id="btn-agente-product" class="w-full text-left p-3 rounded-xl border border-slate-800/80 hover:border-slate-700 bg-dark-900 transition flex items-start space-x-3">
          <span class="text-2xl mt-0.5">💎</span>
          <div>
            <div class="text-sm font-semibold text-white">Demostración Macro</div>
            <p class="text-xs text-slate-400 mt-0.5">100mm macro f/4, slider, splash hook físico en s0-2.</p>
          </div>
        </button>
      </nav>

      <!-- Quick Action Buttons -->
      <div class="pt-3 border-t border-slate-800/80 space-y-2">
        <button onclick="abrirCarpetaModelos()" class="w-full py-2 px-3 rounded-lg bg-dark-900 hover:bg-slate-800 text-slate-300 text-xs font-medium border border-slate-800 flex items-center justify-center space-x-2 transition">
          <span>📁 Abrir Carpeta de Modelos</span>
        </button>
      </div>
    </aside>

    <!-- CONTENT AREA -->
    <main class="flex-1 flex flex-col bg-dark-900 overflow-y-auto">

      <!-- NAVIGATION TABS -->
      <div class="border-b border-slate-800/80 px-8 flex space-x-8 bg-dark-950/60 text-sm font-medium">
        <button onclick="cambiarTab('estudio')" id="tab-btn-estudio" class="py-3.5 border-b-2 border-brand-500 text-white font-semibold flex items-center space-x-2">
          <span>⚡ Generador de Prompts (Studio)</span>
        </button>
        <button onclick="cambiarTab('cerebro')" id="tab-btn-cerebro" class="py-3.5 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center space-x-2 transition">
          <span>🎬 Cerebro Híbrido (Shotlist)</span>
        </button>
        <button onclick="cambiarTab('chat')" id="tab-btn-chat" class="py-3.5 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center space-x-2 transition">
          <span>💬 Conversar con el Director</span>
        </button>
        <button onclick="cambiarTab('modelos')" id="tab-btn-modelos" class="py-3.5 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center space-x-2 transition">
          <span>📦 Modelos & Checkpoints</span>
        </button>
      </div>

      <!-- TAB 1: ESTUDIO DE PRODUCCION -->
      <section id="tab-estudio" class="p-8 max-w-6xl w-full mx-auto space-y-6">
        
        <!-- Input Card -->
        <div class="glass rounded-2xl p-6 shadow-xl border border-slate-800 space-y-5">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-base font-bold text-white flex items-center space-x-2">
                <span id="label-director-actual">🧠 Director General (Auto-Enrutamiento)</span>
              </h2>
              <p class="text-xs text-slate-400 mt-0.5">Ingresa tu idea o producto. El sistema aplicará la calibración óptica y anatómica entrenada.</p>
            </div>
            
            <!-- Quick preset buttons -->
            <div class="flex items-center space-x-2">
              <span class="text-xs text-slate-500 mr-1 hidden sm:inline">Ejemplos rápidos:</span>
              <button onclick="cargarPreset('podcast')" class="px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition">🎙️ Podcast</button>
              <button onclick="cargarPreset('ugc')" class="px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition">📱 UGC Serum</button>
              <button onclick="cargarPreset('talkinghead')" class="px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition">🎬 SaaS B2B</button>
              <button onclick="cargarPreset('product')" class="px-2.5 py-1 text-xs rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition">💎 Macro Reloj</button>
            </div>
          </div>

          <div class="space-y-4">
            <div>
              <label class="block text-xs font-semibold text-slate-300 mb-1.5 uppercase tracking-wide">1. Concepto / Idea del Video o Producto</label>
              <textarea id="input-idea" rows="3" class="w-full bg-dark-950 border border-slate-800 rounded-xl p-3.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 font-sans" placeholder="Ej: Fundador de startup de inteligencia artificial recordando el día más difícil antes de conseguir su primer cliente..."></textarea>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-300 mb-1.5 uppercase tracking-wide">2. Diálogo o Frase Clave (Punchline / Gancho)</label>
              <input type="text" id="input-speech" class="w-full bg-dark-950 border border-slate-800 rounded-xl p-3.5 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 font-sans" placeholder="Opcional: Si lo dejas vacío, el Director asignará el guión de oro más potente...">
            </div>

            <div class="flex items-center justify-between pt-2">
              <div class="text-xs text-slate-400 flex items-center space-x-3">
                <span class="flex items-center space-x-1"><span class="text-emerald-400">✓</span> <span>9:16 Vertical</span></span>
                <span class="flex items-center space-x-1"><span class="text-emerald-400">✓</span> <span>Anti-Alucinación Activo</span></span>
                <span class="flex items-center space-x-1"><span class="text-emerald-400">✓</span> <span>Cero EXIF/Marcas</span></span>
              </div>

              <button onclick="generarPrompts()" id="btn-generar" class="px-6 py-3 rounded-xl bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 text-white font-semibold text-sm shadow-lg shadow-indigo-500/25 transition flex items-center space-x-2">
                <span>🚀 Generar Prompts de Producción</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Output Cards (2 Columns) -->
        <div id="contenedor-resultados" class="grid grid-cols-1 md:grid-cols-2 gap-6 hidden">
          
          <!-- Card 1: Nano Banana Pro (Anchor) -->
          <div class="glass rounded-2xl p-6 border border-slate-800 flex flex-col justify-between space-y-4">
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <span class="w-7 h-7 rounded-lg bg-amber-500/20 text-amber-300 flex items-center justify-center font-bold text-sm">🍌</span>
                  <h3 class="text-sm font-bold text-white">Ancla Fotográfica (Nano Banana Pro)</h3>
                </div>
                <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">Primer Frame</span>
              </div>

              <div class="flex flex-wrap gap-1.5 text-[11px]">
                <span class="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">Boca relajada</span>
                <span class="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">Sin trípodes</span>
                <span class="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">Piel realista</span>
              </div>

              <div class="relative">
                <pre id="output-ancla" class="w-full bg-dark-950 p-4 rounded-xl border border-slate-800 text-xs font-mono text-slate-200 whitespace-pre-wrap leading-relaxed max-h-80 overflow-y-auto select-all"></pre>
              </div>
            </div>

            <button onclick="copiarAlPortapapeles('ancla')" id="btn-copiar-ancla" class="w-full py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold transition flex items-center justify-center space-x-2">
              <span>📋 Copiar Prompt Ancla al Portapapeles</span>
            </button>
          </div>

          <!-- Card 2: Veo 3.1 / Flow (I2V) -->
          <div class="glass rounded-2xl p-6 border border-slate-800 flex flex-col justify-between space-y-4">
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <span class="w-7 h-7 rounded-lg bg-indigo-500/20 text-indigo-300 flex items-center justify-center font-bold text-sm">🎥</span>
                  <h3 class="text-sm font-bold text-white">Prompt Video I2V (Google Veo 3.1 / Flow)</h3>
                </div>
                <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">Movimiento 8s</span>
              </div>

              <div class="flex flex-wrap gap-1.5 text-[11px]">
                <span class="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">Cejas activas</span>
                <span class="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">Audio directo</span>
                <span class="px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">Cero deformación</span>
              </div>

              <div class="relative">
                <pre id="output-video" class="w-full bg-dark-950 p-4 rounded-xl border border-slate-800 text-xs font-mono text-slate-200 whitespace-pre-wrap leading-relaxed max-h-80 overflow-y-auto select-all"></pre>
              </div>
            </div>

            <button onclick="copiarAlPortapapeles('video')" id="btn-copiar-video" class="w-full py-2.5 px-4 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold transition flex items-center justify-center space-x-2 shadow-lg shadow-indigo-500/20">
              <span>📋 Copiar Prompt de Video al Portapapeles</span>
            </button>
          </div>

        </div>

        <!-- Inyección directa a Cerebro Híbrido -->
        <div id="contenedor-inyeccion" class="glass rounded-2xl p-4 border border-indigo-500/30 flex items-center justify-between space-x-4 hidden">
          <div class="flex items-center space-x-3">
            <span class="text-xl">🧠</span>
            <div>
              <div class="text-xs font-bold text-white">Inyectar en Cerebro Híbrido</div>
              <p class="text-[11px] text-slate-400">Guarda estos prompts generados directamente en una toma del <span id="label-inyeccion-prj" class="text-indigo-300 font-mono">shotlist.json</span></p>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <select id="select-toma-cerebro" class="bg-dark-950 border border-slate-800 text-xs text-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:border-indigo-500">
              <!-- Cargado dinámicamente -->
            </select>
            <button onclick="inyectarPromptEnToma()" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg shadow-lg shadow-indigo-500/20 transition flex items-center space-x-1.5">
              <span>💾 Guardar en Toma</span>
            </button>
          </div>
        </div>

      </section>

      <!-- TAB 2: CHAT CON EL DIRECTOR -->
      <section id="tab-chat" class="p-8 max-w-4xl w-full mx-auto space-y-4 hidden flex-1 flex flex-col">
        <div class="glass rounded-2xl p-4 border border-slate-800 flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <span id="chat-avatar" class="text-2xl">🎙️</span>
            <div>
              <h3 id="chat-titulo" class="text-sm font-bold text-white">Director de Podcast & Storytelling (3/4 Profile)</h3>
              <p class="text-xs text-slate-400">Pídele cambios específicos al guión, tono o atmósfera cinematográfica.</p>
            </div>
          </div>
          <button onclick="limpiarChat()" class="text-xs text-slate-400 hover:text-slate-200 px-2 py-1 rounded bg-slate-800">Limpiar</button>
        </div>

        <!-- Chat history -->
        <div id="chat-mensajes" class="flex-1 min-h-[400px] glass rounded-2xl p-6 border border-slate-800 overflow-y-auto space-y-4">
          <div class="flex items-start space-x-3">
            <div class="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-sm font-bold">🎬</div>
            <div class="bg-slate-800/90 rounded-2xl rounded-tl-none p-4 max-w-xl text-sm leading-relaxed text-slate-200 border border-slate-700/60">
              ¡Hola! Soy tu Director asignado. ¿Qué video o spot publicitario quieres planificar hoy? Puedo estructurarte el ancla de imagen para Nano Banana Pro y la coreografía de movimiento para Veo 3.1.
            </div>
          </div>
        </div>

        <!-- Chat Input -->
        <div class="flex space-x-3">
          <input type="text" id="chat-input" onkeypress="handleChatKey(event)" class="flex-1 bg-dark-950 border border-slate-800 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500" placeholder="Escribe al Director (ej: 'Haz el tono más dramático y cambia el suéter a negro')...">
          <button onclick="enviarMensajeChat()" id="btn-enviar-chat" class="px-5 py-3 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-semibold text-sm transition">
            Enviar
          </button>
        </div>
      </section>

      <!-- TAB 3: MODELOS Y CHECKPOINTS -->
      <section id="tab-modelos" class="p-8 max-w-5xl w-full mx-auto space-y-6 hidden">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-lg font-bold text-white">Modelos LoRA y Checkpoints Instalados</h2>
            <p class="text-xs text-slate-400 mt-1">Ubicación local en tu PC: <code class="font-mono text-indigo-400">c:\\Users\\Gabo\\Documents\\entrenamiento de ai\\modelo_entrenado</code></p>
          </div>
          <button onclick="abrirCarpetaModelos()" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold shadow-lg shadow-indigo-500/20 transition">
            📂 Abrir en Explorador
          </button>
        </div>

        <div id="grid-modelos" class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Loaded dynamically -->
        </div>

        <!-- Kaggle Training Next Steps -->
        <div class="glass rounded-2xl p-6 border border-slate-800 space-y-4">
          <h3 class="text-sm font-bold text-white flex items-center space-x-2">
            <span>🚀 Siguiente Agente a Entrenar: Subagente 4 - Entrevistas Callejeras (Vox Pop)</span>
          </h3>
          <p class="text-xs text-slate-300 leading-relaxed">
            Ya tienes el archivo <code class="text-indigo-300 bg-slate-900 px-2 py-0.5 rounded font-mono">entrenamiento_kaggle_subagente_street.ipynb</code> listo en tu disco local.
            Súbelo a Kaggle con GPU T4 x2 para entrenar los adaptadores de óptica 28mm f/5.6 con micrófono de mano y turnos limpios sin solapar voces.
          </p>
          <div class="flex items-center space-x-3 pt-2">
            <a href="https://www.kaggle.com" target="_blank" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold transition">
              Abrir Kaggle en el navegador ↗
            </a>
          </div>
        </div>
      </section>

      <!-- TAB 4: CEREBRO HIBRIDO (PIPELINE & SHOTLIST) -->
      <section id="tab-cerebro" class="p-8 max-w-6xl w-full mx-auto space-y-6 hidden">
        <div class="flex items-center justify-between">
          <div>
            <div class="flex items-center space-x-3">
              <h2 class="text-lg font-bold text-white flex items-center space-x-2">
                <span>🧠 Cerebro Híbrido: Pipeline & Shotlist</span>
              </h2>
              <span id="label-proyecto-activo" class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                Cargando...
              </span>
            </div>
            <p class="text-xs text-slate-400 mt-1">Conexión con <code class="font-mono text-indigo-400">C:/Users/Gabo/Documents/cerebro-hibrido-v2</code></p>
          </div>
          <div class="flex items-center space-x-3">
            <button onclick="cargarCerebro()" class="px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold transition flex items-center space-x-1.5">
              <span>🔄 Recargar Tomas</span>
            </button>
            <button onclick="abrirCarpetaCerebro()" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold shadow-lg shadow-indigo-500/20 transition flex items-center space-x-1.5">
              <span>📂 Abrir Cerebro Híbrido</span>
            </button>
          </div>
        </div>

        <!-- Tomas del Shotlist -->
        <div class="space-y-4">
          <div class="flex items-center justify-between text-xs text-slate-400 px-1">
            <span id="resumen-tomas">Cargando tomas del proyecto activo...</span>
            <span class="text-[11px] text-slate-500">Haz clic en 'Cargar en Estudio' para calibrar el prompt con nuestros 5 Directores</span>
          </div>
          <div id="grid-shots-cerebro" class="grid grid-cols-1 gap-3.5">
            <!-- Cargado dinámicamente -->
          </div>
        </div>
      </section>

    </main>
  </div>

  <!-- TOAST NOTIFICATION -->
  <div id="toast" class="fixed bottom-6 right-6 z-50 glass px-4 py-3 rounded-xl border border-indigo-500/40 text-xs font-medium text-white shadow-2xl flex items-center space-x-2 transform translate-y-20 opacity-0 transition-all duration-300">
    <span class="text-emerald-400 font-bold">✓</span>
    <span id="toast-msg">Copiado al portapapeles de Windows</span>
  </div>

  <script>
    let agenteActual = 'auto';
    let ultimoResultado = null;

    // Presets rápidos
    const PRESETS = {
      podcast: {
        agente: 'podcast',
        idea: "Fundador de startup tecnológica recordando sus inicios y el miedo a fracasar en público",
        speech: "Tardé diez años en entender que el problema nunca fue el dinero. Era el miedo a fracasar en público."
      },
      ugc: {
        agente: 'ugc',
        idea: "Creadora de contenido recomendando un serum facial de ácido hialurónico mostrando textura de piel",
        speech: "Ok, llevo dos semanas usando esto y mira mi piel… o sea, ¿qué? No lo puedo creer."
      },
      talkinghead: {
        agente: 'talkinghead',
        idea: "Directora de software B2B en oficina de cristal moderna explicando optimización de procesos comerciales",
        speech: "Tu equipo comercial pierde el treinta por ciento de los leads por responder tarde. Nosotros lo resolvemos en segundos."
      },
      product: {
        agente: 'product',
        idea: "Smartwatch de titanio negro mate sobre grava volcánica con iluminación de acento dramática",
        speech: "un splash de agua en cámara lenta seguido de la iluminación de la pantalla OLED"
      }
    };

    function seleccionarAgente(agente) {
      agenteActual = agente;
      document.querySelectorAll('#lista-agentes button').forEach(b => b.classList.remove('agent-active'));
      const btn = document.getElementById('btn-agente-' + agente);
      if (btn) btn.classList.add('agent-active');

      const titulos = {
        auto: '🧠 Director General (Auto-Enrutamiento)',
        podcast: '🎙️ Director de Podcast & Storytelling (3/4 Profile)',
        talkinghead: '🎬 Director Talking Head Comercial (50mm f/2.8)',
        ugc: '📱 Director UGC & Creadores (24mm Selfie Handheld)',
        street: '🎤 Director Entrevista Callejera (Vox Pop 28mm)',
        product: '💎 Director Demostración Producto Macro (100mm f/4)'
      };
      document.getElementById('label-director-actual').innerText = titulos[agente] || '🧠 Director General';
      document.getElementById('chat-titulo').innerText = titulos[agente] || '🧠 Director General';
    }

    function cargarPreset(tipo) {
      const p = PRESETS[tipo];
      if (p) {
        seleccionarAgente(p.agente);
        document.getElementById('input-idea').value = p.idea;
        document.getElementById('input-speech').value = p.speech;
      }
    }

    async function generarPrompts() {
      const idea = document.getElementById('input-idea').value.trim();
      const speech = document.getElementById('input-speech').value.trim();
      if (!idea) {
        mostrarToast("Por favor describe una idea primero.");
        return;
      }

      const btn = document.getElementById('btn-generar');
      btn.disabled = true;
      btn.innerText = "⏳ Directores procesando...";

      try {
        const resp = await fetch('/api/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            idea: idea,
            speech: speech,
            formato: agenteActual === 'auto' ? null : agenteActual
          })
        });
        const data = await resp.json();
        ultimoResultado = data;

        document.getElementById('output-ancla').innerText = data.prompt_ancla;
        document.getElementById('output-video').innerText = data.prompt_video;
        document.getElementById('contenedor-resultados').classList.remove('hidden');

        if (datosCerebro && datosCerebro.disponible) {
          const iny = document.getElementById('contenedor-inyeccion');
          if (iny) iny.classList.remove('hidden');
        }

        // Scroll suave hacia los resultados
        document.getElementById('contenedor-resultados').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        mostrarToast("✅ Prompts generados y calibrados con éxito");
      } catch (err) {
        mostrarToast("Error al generar: " + err);
      } finally {
        btn.disabled = false;
        btn.innerText = "🚀 Generar Prompts de Producción";
      }
    }

    async function copiarAlPortapapeles(tipo) {
      if (!ultimoResultado) return;
      const texto = tipo === 'ancla' ? ultimoResultado.prompt_ancla : ultimoResultado.prompt_video;

      // Usar API local de Windows clipboard en backend
      await fetch('/api/copy', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ texto: texto })
      });

      // Fallback navegador
      navigator.clipboard.writeText(texto);
      mostrarToast(`📋 Prompt ${tipo.toUpperCase()} copiado al portapapeles de Windows`);
    }

    function cambiarTab(tab) {
      ['estudio', 'cerebro', 'chat', 'modelos'].forEach(t => {
        const el = document.getElementById('tab-' + t);
        const btn = document.getElementById('tab-btn-' + t);
        if (el) el.classList.add('hidden');
        if (btn) btn.className = "py-3.5 border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center space-x-2 transition";
      });

      const activeEl = document.getElementById('tab-' + tab);
      const activeBtn = document.getElementById('tab-btn-' + tab);
      if (activeEl) activeEl.classList.remove('hidden');
      if (activeBtn) activeBtn.className = "py-3.5 border-b-2 border-brand-500 text-white font-semibold flex items-center space-x-2";

      if (tab === 'modelos') cargarModelos();
      if (tab === 'cerebro') cargarCerebro();
    }

    async function cargarModelos() {
      try {
        const resp = await fetch('/api/status');
        const data = await resp.json();
        
        document.getElementById('txt-modelos').innerText = `${data.modelos.filter(m => m.activo).length} Modelos Listos`;
        
        const grid = document.getElementById('grid-modelos');
        grid.innerHTML = data.modelos.map(m => `
          <div class="glass p-5 rounded-2xl border border-slate-800 space-y-3">
            <div class="flex items-center justify-between">
              <span class="font-bold text-sm text-white">${m.nombre}</span>
              <span class="px-2 py-0.5 text-[10px] rounded font-semibold ${m.activo ? 'bg-emerald-500/20 text-emerald-300' : 'bg-slate-800 text-slate-400'}">
                ${m.activo ? 'Activo' : 'Pendiente'}
              </span>
            </div>
            <div class="text-xs text-slate-400 flex items-center justify-between">
              <span>Peso LoRA: <strong class="text-slate-200">${m.tamano_mb} MB</strong></span>
              <span>Formato: <strong class="text-slate-200">Safetensors</strong></span>
            </div>
            <p class="text-[11px] font-mono text-slate-500 truncate">${m.ruta}</p>
          </div>
        `).join('');
      } catch (e) {
        console.error(e);
      }
    }

    async function abrirCarpetaModelos() {
      await fetch('/api/open_folder', { method: 'POST' });
      mostrarToast("📂 Carpeta abierta en el Explorador de Windows");
    }

    async function enviarMensajeChat() {
      const input = document.getElementById('chat-input');
      const msg = input.value.trim();
      if (!msg) return;

      const chatCont = document.getElementById('chat-mensajes');
      chatCont.innerHTML += `
        <div class="flex items-start space-x-3 justify-end">
          <div class="bg-brand-600 rounded-2xl rounded-tr-none p-3.5 max-w-xl text-sm leading-relaxed text-white">
            ${msg}
          </div>
          <div class="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-xs font-bold">Tú</div>
        </div>
      `;
      input.value = '';
      chatCont.scrollTop = chatCont.scrollHeight;

      const btn = document.getElementById('btn-enviar-chat');
      btn.disabled = true;

      try {
        const resp = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            mensaje: msg,
            director: agenteActual
          })
        });
        const data = await resp.json();

        chatCont.innerHTML += `
          <div class="flex items-start space-x-3">
            <div class="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-sm font-bold">🎬</div>
            <div class="bg-slate-800/90 rounded-2xl rounded-tl-none p-4 max-w-xl text-sm leading-relaxed text-slate-200 border border-slate-700/60 whitespace-pre-wrap">
              ${data.respuesta}
            </div>
          </div>
        `;
        chatCont.scrollTop = chatCont.scrollHeight;
      } catch (err) {
        mostrarToast("Error en chat: " + err);
      } finally {
        btn.disabled = false;
      }
    }

    function handleChatKey(e) {
      if (e.key === 'Enter') enviarMensajeChat();
    }

    function limpiarChat() {
      document.getElementById('chat-mensajes').innerHTML = `
        <div class="flex items-start space-x-3">
          <div class="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-sm font-bold">🎬</div>
          <div class="bg-slate-800/90 rounded-2xl rounded-tl-none p-4 max-w-xl text-sm leading-relaxed text-slate-200 border border-slate-700/60">
            Chat reiniciado. ¿En qué video o concepto deseas trabajar?
          </div>
        </div>
      `;
    }

    function mostrarToast(msg) {
      const t = document.getElementById('toast');
      document.getElementById('toast-msg').innerText = msg;
      t.classList.remove('translate-y-20', 'opacity-0');
      setTimeout(() => {
        t.classList.add('translate-y-20', 'opacity-0');
      }, 3000);
    }

    let datosCerebro = null;

    async function cargarCerebro() {
      try {
        const resp = await fetch('/api/cerebro');
        const data = await resp.json();
        datosCerebro = data;
        
        if (data.disponible) {
          const badgeTxt = document.getElementById('txt-cerebro');
          if (badgeTxt) badgeTxt.innerText = `Cerebro: ${data.proyecto_activo}`;
          const prjLbl = document.getElementById('label-proyecto-activo');
          if (prjLbl) prjLbl.innerText = data.proyecto_activo;
          const resTxt = document.getElementById('resumen-tomas');
          if (resTxt) resTxt.innerText = `${data.total_shots} tomas en el proyecto activo (${data.proyecto_activo})`;
          const inyPrj = document.getElementById('label-inyeccion-prj');
          if (inyPrj) inyPrj.innerText = data.proyecto_activo;
          
          // Poblar select de inyeccion
          const select = document.getElementById('select-toma-cerebro');
          if (select) {
            select.innerHTML = data.shots.filter(s => s.kind !== 'ui_insert').map(s => `
              <option value="${s.id}">${s.id}: ${s.vo_text ? s.vo_text.substring(0, 45) + '...' : s.id}</option>
            `).join('');
          }
          
          // Poblar lista de tomas en tab-cerebro
          const grid = document.getElementById('grid-shots-cerebro');
          if (grid) {
            grid.innerHTML = data.shots.map(s => {
              const isInsert = s.kind === 'ui_insert';
              const formatBadge = s.formato ? `<span class="px-2 py-0.5 rounded text-[10px] bg-purple-500/20 text-purple-300 font-mono">${s.formato}</span>` : '';
              return `
                <div class="glass p-4 rounded-xl border border-slate-800 hover:border-slate-700 transition flex items-start justify-between space-x-4">
                  <div class="space-y-1.5 flex-1">
                    <div class="flex items-center space-x-2">
                      <span class="font-mono font-bold text-xs ${isInsert ? 'text-amber-400' : 'text-indigo-400'}">${s.id}</span>
                      <span class="text-[10px] px-1.5 py-0.2 rounded ${isInsert ? 'bg-amber-500/20 text-amber-300' : 'bg-slate-800 text-slate-300'}">${s.kind || 'shot'}</span>
                      ${formatBadge}
                      <span class="text-[10px] text-slate-500">${s.framing || ''} ${s.camera ? (s.camera.lens || '') : ''}</span>
                    </div>
                    <p class="text-xs text-slate-200">${s.vo_text || s.description || (s.subject ? s.subject.action : 'Sin texto')}</p>
                    ${s.anchor_prompt ? `<div class="text-[11px] font-mono text-slate-400 truncate">🍌 Ancla: ${s.anchor_prompt.substring(0, 80)}...</div>` : ''}
                  </div>
                  <div class="flex items-center space-x-2">
                    ${!isInsert ? `
                      <button onclick='cargarTomaEnEstudio(${JSON.stringify(s).replace(/'/g, "&#39;")})' class="px-3 py-1.5 rounded-lg bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 text-xs font-semibold border border-indigo-500/30 transition">
                        ⚡ Cargar en Estudio
                      </button>
                    ` : '<span class="text-[11px] text-slate-500">Remotion UI</span>'}
                  </div>
                </div>
              `;
            }).join('');
          }
        } else {
          const badgeTxt = document.getElementById('txt-cerebro');
          if (badgeTxt) badgeTxt.innerText = 'Cerebro: No detectado';
        }
      } catch (e) {
        console.error(e);
      }
    }

    function cargarTomaEnEstudio(s) {
      seleccionarAgente(s.formato || 'auto');
      document.getElementById('input-idea').value = s.description || (s.subject ? s.subject.action : '') || s.vo_text || '';
      document.getElementById('input-speech').value = s.vo_text || '';
      cambiarTab('estudio');
      mostrarToast(`Toma ${s.id} cargada en el Estudio`);
    }

    async function inyectarPromptEnToma() {
      if (!ultimoResultado) {
        mostrarToast("Primero genera los prompts.");
        return;
      }
      const select = document.getElementById('select-toma-cerebro');
      const shotId = select.value;
      if (!shotId) return;

      try {
        const resp = await fetch('/api/cerebro/update_shot', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            shot_id: shotId,
            ancla: ultimoResultado.prompt_ancla,
            video: ultimoResultado.prompt_video,
            formato: ultimoResultado.formato_elegido
          })
        });
        const data = await resp.json();
        if (data.status === 'ok') {
          mostrarToast(`✅ Prompts inyectados con éxito en la toma ${shotId} de shotlist.json`);
          cargarCerebro();
        } else {
          mostrarToast("Error al inyectar en shotlist.json");
        }
      } catch (e) {
        mostrarToast("Error: " + e);
      }
    }

    async function abrirCarpetaCerebro() {
      await fetch('/api/cerebro/open', { method: 'POST' });
      mostrarToast("📂 Carpeta de Cerebro Híbrido abierta");
    }

    // Inicializar estado al cargar
    cargarModelos();
    cargarCerebro();
  </script>
</body>
</html>
"""

class ManejadorEstudio(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/" or url.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
        elif url.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            data = obtener_estado_modelos()
            self.wfile.write(json.dumps(data).encode("utf-8"))
        elif url.path == "/api/cerebro":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            data = obtener_datos_cerebro()
            self.wfile.write(json.dumps(data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        url = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        payload = json.loads(body) if body else {}

        if url.path == "/api/generate":
            idea = payload.get("idea", "")
            speech = payload.get("speech", "")
            formato = payload.get("formato", None)

            resultado = router.procesar(idea, speech, formato)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resultado).encode("utf-8"))

        elif url.path == "/api/copy":
            texto = payload.get("texto", "")
            ok = copiar_a_portapapeles(texto)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok" if ok else "error"}).encode("utf-8"))

        elif url.path == "/api/open_folder":
            base_dir = os.path.join(os.path.dirname(__file__), "modelo_entrenado")
            os.makedirs(base_dir, exist_ok=True)
            subprocess.Popen(['explorer', base_dir])
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "opened"}).encode("utf-8"))

        elif url.path == "/api/chat":
            mensaje = payload.get("mensaje", "")
            director_slug = payload.get("director", "auto")

            prompts_directores = {
                "podcast": "Eres el Subagente Director de Podcast & Masterclass (3/4 Profile). Responde con autoridad cinematográfica. Reglas: lente 85mm f/1.8, short lighting 5:1, Shure SM7B rígido a 10cm de la boca, mirada 35° al entrevistador off-camera, nunca al lente.",
                "ugc": "Eres el Subagente Director de UGC & Creadores (TikTok Shop / Reels). Tu tono es enérgico, informal y directo. Reglas: cámara selfie 24mm con micro-jitter humano en la mano, vicio de pantalla, mirada que alterna al lente en el punchline, piel real sin filtros.",
                "talkinghead": "Eres el Subagente Director de Talking Head Comercial B2B/B2C. Reglas: 50mm f/2.8, mirada frontal directa al lente, cejas activas y expresivas modulando el habla, cero congelamiento facial, boca cerrada y relajada en el frame inicial.",
                "street": "Eres el Subagente Director de Entrevista Callejera (Vox Pop). Reglas: 28mm f/5.6, micrófono de mano con flag sólida, turnos limpios de habla sin solapamiento de voces, reacción de sorpresa->pensamiento->respuesta.",
                "product": "Eres el Subagente Director de Demostración de Producto Macro. Reglas: 100mm macro f/4, slider motorizado, hook físico de agua/splash en s0-2, mano de 5 dedos anatómicamente perfecta, cero morphing.",
                "auto": "Eres el Director General del Estudio Multi-Agente de Video Corto para Veo 3.1 y Nano Banana Pro. Asesoras al usuario sobre qué formato le conviene para su objetivo y cómo perfeccionar sus prompts."
            }

            system_prompt = prompts_directores.get(director_slug, prompts_directores["auto"])
            respuesta = llamar_gemini(system_prompt, mensaje)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"respuesta": respuesta}).encode("utf-8"))

        elif url.path == "/api/cerebro/update_shot":
            shot_id = payload.get("shot_id", "")
            ancla = payload.get("ancla", "")
            video = payload.get("video", "")
            formato = payload.get("formato", "")
            ok = actualizar_shot_cerebro(shot_id, ancla, video, formato)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok" if ok else "error"}).encode("utf-8"))

        elif url.path == "/api/cerebro/open":
            if os.path.exists(CEREBRO_V2_DIR):
                subprocess.Popen(['explorer', CEREBRO_V2_DIR])
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "opened"}).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

def iniciar_servidor(puerto: int = 7860):
    servidor = HTTPServer(("localhost", puerto), ManejadorEstudio)
    url = f"http://localhost:{puerto}"
    print("=" * 70)
    print("  [OK] ESTUDIO DE DIRECTORES IA - INTERFAZ GRAFICA ACTIVA")
    print("=" * 70)
    print(f"  * Interfaz web disponible en: {url}")
    print("  * Modelos activos: Podcast, Maestro 5 Formatos, Nano Banana")
    print("  * Presiona Ctrl+C en esta terminal para detener el servidor.")
    print("=" * 70)

    # Abrir navegador automáticamente
    threading.Timer(1.2, lambda: webbrowser.open(url)).start()

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
        servidor.server_close()

if __name__ == "__main__":
    puerto = 7860
    if len(sys.argv) > 1:
        try:
            puerto = int(sys.argv[1])
        except ValueError:
            pass
    iniciar_servidor(puerto)
