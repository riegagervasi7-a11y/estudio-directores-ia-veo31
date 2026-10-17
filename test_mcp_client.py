"""
test_mcp_client.py
Cliente ligero JSON-RPC para comunicarse con el servidor MCP de Google Flow
y descubrir sus herramientas disponibles.
"""

import subprocess
import json
import sys
import time

def main():
    print("[*] Iniciando servidor MCP google-flow-browser-mcp...")
    cmd = ["cmd.exe", "/c", "npx", "-y", "google-flow-browser-mcp"]
    
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # 1. Enviar mensaje de Initialize
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "antigravity-flow-client",
                "version": "1.0.0"
            }
        }
    }

    req_str = json.dumps(init_request) + "\n"
    proc.stdin.write(req_str)
    proc.stdin.flush()

    # Leer respuesta de initialize
    line = proc.stdout.readline()
    print("[+] Respuesta initialize:", line.strip()[:160] + "...")

    # Enviar initialized notification
    notif = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    proc.stdin.write(json.dumps(notif) + "\n")
    proc.stdin.flush()

    # 2. Listar herramientas (tools/list)
    tools_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    proc.stdin.write(json.dumps(tools_request) + "\n")
    proc.stdin.flush()

    line = proc.stdout.readline()
    res = json.loads(line)
    tools = res.get("result", {}).get("tools", [])
    print(f"\n[+] ¡Herramientas descubiertas ({len(tools)} tools)!:")
    for t in tools:
        print(f" - {t['name']}: {t.get('description', '')[:70]}...")

    # Terminar proceso
    proc.terminate()

if __name__ == "__main__":
    main()
