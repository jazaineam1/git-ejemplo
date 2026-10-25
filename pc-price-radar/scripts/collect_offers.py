#!/usr/bin/env python3
"""Conector opt-in SerpApi Google Shopping (GL=CO).

No scrapea directamente tiendas, no esquiva protecciones y no genera precios
si falta la credencial. Credenciales solo en servidor/GitHub Actions.
"""
from __future__ import annotations
import datetime as dt
import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "offers.json"
DEFAULT_QUERIES = [
    "portatil RTX 4060 32GB RAM 1TB SSD Colombia",
    "portatil RTX 5060 32GB RAM 1TB Colombia",
    "ASUS Zenbook OLED Intel Core Ultra 32GB Colombia",
    "Lenovo Legion NVIDIA RTX 32GB Colombia",
]
USER_AGENT = "PCPriceRadar/0.1 (price research; authorized aggregator)"


def extract_specs(title: str) -> dict:
    s = str(title or "")
    ram = re.search(r"\bRAM\s*[:=-]?\s*(\d{1,3})\s*GB\b|\b(\d{1,3})\s*GB\s*(?:RAM|DDR[45]|LPDDR[45]X?)\b", s, re.I)
    drive = re.search(r"\bSSD\s*[:=-]?\s*(\d+(?:\.\d+)?)\s*(TB|GB)\b|\b(\d+(?:\.\d+)?)\s*(TB|GB)\s*(?:SSD|NVME)\b", s, re.I)
    gpu = ("nvidia" if re.search(r"\b(?:RTX|GEFORCE)\s*\d{4}\b", s, re.I)
           else "arc" if re.search(r"\bIntel\s+Arc\b", s, re.I)
           else "amd" if re.search(r"\bRadeon\b", s, re.I) else "")
    vram = re.search(r"RTX\s*\d{4}[^\d]{0,20}(\d{1,2})\s*GB\b", s, re.I)
    def nv(pattern):
        return int(next((v for v in pattern.groups() if v), 0)) if pattern else None
    ssd = None
    if drive:
        n = float(drive.group(1) or drive.group(3))
        unit = (drive.group(2) or drive.group(4)).upper()
        ssd = int(n * (1024 if unit == "TB" else 1))
    return {
        "ram": nv(ram), "ssd": ssd, "vram": nv(vram),
        "gpu": gpu, "screen": "OLED" if "OLED" in s.upper() else "",
        "battery": None,
    }


def safe_url(url: str) -> bool:
    try:
        u = urllib.parse.urlsplit(str(url or ""))
        return u.scheme == "https" and bool(u.hostname)
    except ValueError:
        return False


def as_offer(item: dict, checked_at: str) -> dict | None:
    title = str(item.get("title") or "").strip()
    url = item.get("link") or item.get("product_link") or ""
    val = item.get("extracted_price")
    # GL=CO + extracted_price no garantiza moneda; solo aceptar importe
    # compatible con COP para evitar confundir US$ 800 con COP 800.
    if not title or not safe_url(url) or not isinstance(val, (int, float)) or not 200_000 <= val <= 150_000_000:
        return None
    old = item.get("extracted_old_price")
    discount = round((1 - val / old) * 100, 2) if isinstance(old, (int, float)) and old > val > 0 else 0
    source_name = str(item.get("source") or "Google Shopping (comercio no especificado)")
    pid = str(item.get("product_id") or "")
    return {
        "id": "serpapi-" + re.sub(r"[^A-Za-z0-9]", "-", pid or (url + title))[:90],
        "title": title[:170], "seller": source_name[:90], "url": url,
        "currency": "COP", "price": old if discount else val, "discount": discount, "coupon": 0,
        "shipping": None, "taxes": None, "fx": 1,
        "condition": "new", "checked_at": checked_at,
        "verified": False, "source": "api",
        "notes": "Precio de agregador GL=CO, moneda COP inferida por magnitud; confirmar moneda, variante, stock, estado, cupón, garantías y envío.",
        "currency_confidence": "inferred_not_verified",
        **extract_specs(title),
    }


def fetch_shopping(query: str, key: str, max_price: int | None = None) -> dict:
    params = {
        "engine": "google_shopping", "q": query, "gl": "co", "hl": "es",
        "location": "Bogota, Colombia", "api_key": key,
    }
    if max_price:
        params["max_price"] = str(max_price)
    url = "https://serpapi.com/search.json?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=35) as r:
        payload = json.load(r)
    if payload.get("error"):
        raise RuntimeError("El proveedor de Shopping devolvió un error; comprueba tu cuenta y el límite de peticiones.")
    return payload


def collect(payloads: list[dict], at: str) -> list[dict]:
    results = []
    seen = set()
    for p in payloads:
        items = list(p.get("shopping_results") or [])
        for category in p.get("categorized_shopping_results") or []:
            items.extend(category.get("shopping_results") or [])
        for raw in items:
            offer = as_offer(raw, at)
            if not offer:
                continue
            key = (offer["url"], offer["price"])
            if key not in seen:
                seen.add(key)
                results.append(offer)
    return results


def main() -> int:
    key = os.getenv("SERPAPI_KEY", "").strip()
    if not key:
        print("Sin SERPAPI_KEY: omitiendo consulta externa; no se generan precios falsos.")
        return 0
    custom = os.getenv("PC_RADAR_QUERIES", "").strip()
    queries = [q.strip()[:180] for q in custom.split(";") if q.strip()] if custom else DEFAULT_QUERIES
    limit = max(1, min(int(os.getenv("PC_RADAR_MAX_QUERIES", "4")), 8))
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    all_payloads = []
    for q in queries[:limit]:
        try:
            all_payloads.append(fetch_shopping(q, key))
            print("Consulta completada:", q)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, RuntimeError) as exc:
            # Nunca mostrar URL, que contiene la clave.
            print("Consulta fallida para", repr(q), "tipo:", type(exc).__name__, file=sys.stderr)
    if not all_payloads:
        print("Proveedor sin datos: conservar offers.json previo y reportar error.", file=sys.stderr)
        return 1
    result = collect(all_payloads, now)
    if not result:
        print("Resultados sin precios COP plausibles: no sobreescribir datos previos.")
        return 1
    data = {"schema_version": 1, "provider": "SerpApi Google Shopping GL=CO", "collected_at": now,
            "disclaimer": "No comprueba precios finales, inventario, envíos ni impuestos. Moneda inferida.",
            "offers": result[:180]}
    tmp = OUTPUT.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(OUTPUT)
    print("Guardadas", len(data["offers"]), "fichas. No se certifican.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
