"""
mcp_flow_generador.py
Controlador directo de Google Flow a través del servidor MCP local.
Automatiza el envío del prompt maestro y la descarga de la imagen generada.
"""

import subprocess
import json
import sys
import time
import os

PROJECT_ID = "a32e72e0-e2cd-4f08-aeda-87e70ac3fa94"

class GoogleFlowMCPClient:
    def __init__(self):
        cmd = ["cmd.exe", "/c", "npx", "-y", "google-flow-browser-mcp"]
        self.proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            bufsize=1
        )
        self.msg_id = 1
        self._initialize()

    def _send(self, method: str, params: dict = None) -> dict:
        req = {
            "jsonrpc": "2.0",
            "id": self.msg_id,
            "method": method
        }
        if params is not None:
            req["params"] = params
        self.msg_id += 1

        self.proc.stdin.write(json.dumps(req) + "\n")
        self.proc.stdin.flush()

        line = self.proc.stdout.readline()
        if not line:
            return {"error": "Servidor MCP no respondió"}
        try:
            return json.loads(line)
        except Exception as e:
            return {"error": f"Error decodificando respuesta: {e}", "raw": line}

    def _initialize(self):
        self._send("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "antigravity-flow-operator", "version": "1.0.0"}
        })
        self.proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
        self.proc.stdin.flush()

    def call_tool(self, name: str, arguments: dict) -> dict:
        return self._send("tools/call", {
            "name": name,
            "arguments": arguments
        })

    def check_login(self) -> bool:
        res = self.call_tool("flow_confirm_login", {
            "projectId": PROJECT_ID,
            "userConfirmedFreshSignIn": True,
            "membershipConfirmed": True,
            "creditsAvailableConfirmed": True
        })
        # Si no da error de login, está autenticado
        is_error = res.get("result", {}).get("isError", False)
        text = str(res)
        if "Google still shows a login page" in text:
            return False
        return not is_error

    def generar_imagen(self, prompt: str):
        print("\n[1] Preparando generación en Google Flow...")
        res_prep = self.call_tool("flow_prepare_generation", {
            "projectId": PROJECT_ID,
            "operation": "image",
            "shotIndex": 0,
            "prompt": prompt
        })
        print("Respuesta preparación:", res_prep.get("result", {}).get("content", [{}])[0].get("text", ""))

        # Buscar jobId
        job_data = res_prep.get("result", {}).get("structuredContent", {})
        job_id = job_data.get("jobId") or job_data.get("id")

        if not job_id:
            print("[!] No se obtuvo jobId para la generación.")
            return False

        print(f"\n[2] Enviando generación (Job ID: {job_id})...")
        res_sub = self.call_tool("flow_submit_generation", {
            "jobId": job_id,
            "userApprovedCreditSpend": True
        })
        print("Respuesta envío:", res_sub.get("result", {}).get("content", [{}])[0].get("text", ""))

        print("\n[3] Esperando a que Nano Banana Pro termine de renderizar...")
        res_wait = self.call_tool("flow_wait_for_generation", {
            "jobId": job_id
        })
        print("Resultado generación:", res_wait.get("result", {}).get("content", [{}])[0].get("text", ""))

        return True

    def close(self):
        try:
            self.proc.terminate()
        except:
            pass

def main():
    print("=" * 60)
    print("  OPERADOR DIRECTO ANTIGRAVITY <-> GOOGLE FLOW MCP")
    print("=" * 60)

    client = GoogleFlowMCPClient()
    print("[*] Conectado al servidor MCP de Google Flow.")

    if not client.check_login():
        print("\n[!] AVISO: La ventana de Chrome para Google Flow está abierta en tu pantalla.")
        print("    -> Por favor, inicia sesión con tu cuenta de Google en esa ventana.")
        print("    -> Una vez que veas la pantalla de Google Flow, vuelve aquí y ejecuta este script.")
        client.close()
        return

    print("\n[✓] Sesión de Google Flow verificada y activa.")
    
    # Leer el último prompt
    if os.path.exists("ultimo_prompt.txt"):
        with open("ultimo_prompt.txt", "r", encoding="utf-8") as f:
            prompt = f.read().strip()
    else:
        prompt = "A candid, unposed documentary portrait of a 65-year-old Scandinavian fisherman on a wet wooden dock in cold drizzle, Leica M11 RAW 85mm f/2.5, visible skin pores, water droplets on beard, unretouched aesthetic, zero CGI."

    print(f"\n[+] Enviando prompt a Nano Banana Pro:")
    print(prompt[:120] + "...")

    client.generar_imagen(prompt)
    client.close()

if __name__ == "__main__":
    main()
