"""
buscar_anuncios_meta.py
Buscador automatizado de la Biblioteca de Anuncios de Meta (Meta Ads Library) sin APIs de pago.
Permite buscar anuncios activos de cualquier marca SaaS o competidor en Instagram y Facebook,
extrayendo sus guiones, ganchos (hooks) y enlaces directos de video (.mp4).
"""

import sys
import os
import json
import subprocess
from typing import List, Dict, Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def buscar_meta_ads(query: str, country: str = "US", max_results: int = 5, solo_video: bool = True) -> List[Dict[str, Any]]:
    output_file = f"temp_ads_{country}_{query.replace(' ', '_')}.json"
    cmd = [
        sys.executable, "-m", "meta_ads_collector",
        "--query", query,
        "--country", country,
        "-n", str(max_results),
        "-o", output_file
    ]
    if solo_video:
        cmd.append("--has-video")

    print(f"[*] Conectando a Meta Ads Library para: '{query}' en país '{country}'...")
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"[-] Error al consultar Meta Ads: {e}")
        return []

    if not os.path.exists(output_file):
        return []

    try:
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        os.remove(output_file)
        return data.get("ads", [])
    except Exception as e:
        print(f"[-] Error al leer resultados: {e}")
        return []

def formatear_anuncios(ads: List[Dict[str, Any]]) -> str:
    if not ads:
        return "No se encontraron anuncios activos con esos criterios."

    lineas = []
    lineas.append("=" * 80)
    lineas.append(f"  ANUNCIOS ACTIVOS ENCONTRADOS EN META ADS LIBRARY ({len(ads)} resultados)")
    lineas.append("=" * 80)

    for i, ad in enumerate(ads, 1):
        page = ad.get("page", {})
        page_name = page.get("name", "Desconocido")
        creatives = ad.get("creatives", [])
        if not creatives:
            continue
        c = creatives[0]
        body = c.get("body", "Sin texto").strip()
        video_url = c.get("video_hd_url") or c.get("video_url") or "Sin URL de video"
        thumb_url = c.get("thumbnail_url", "Sin miniatura")
        cta = c.get("cta_text", "N/A")

        lineas.append(f"\n[ANUNCIO #{i}] - {page_name}")
        lineas.append(f"• Fecha inicio: {ad.get('delivery_start_time', 'N/A')}")
        lineas.append(f"• Plataformas: {', '.join(ad.get('publisher_platforms', []))}")
        lineas.append(f"• CTA: {cta}")
        lineas.append(f"• Video MP4: {video_url[:120]}...")
        lineas.append("-" * 80)
        lineas.append("GUION / TEXTO DEL ANUNCIO (HOOK & COPY):")
        # Mostrar las primeras 5 líneas del copy
        preview_body = "\n".join("  " + l for l in body.split("\n")[:8])
        lineas.append(preview_body)
        if len(body.split("\n")) > 8:
            lineas.append("  ...")
        lineas.append("-" * 80)

    return "\n".join(lineas)

if __name__ == "__main__":
    q = "Kommo"
    c = "US"
    n = 3
    if len(sys.argv) > 1:
        q = sys.argv[1]
    if len(sys.argv) > 2:
        c = sys.argv[2]
    if len(sys.argv) > 3:
        try:
            n = int(sys.argv[3])
        except ValueError:
            pass

    anuncios = buscar_meta_ads(q, c, n)
    reporte = formatear_anuncios(anuncios)
    print(reporte)
