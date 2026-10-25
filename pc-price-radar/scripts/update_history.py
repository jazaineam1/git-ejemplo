#!/usr/bin/env python3
"""Conserva precios observados de las mismas publicaciones y detecta caídas.

El descuento respecto a la mediana histórica NO es un cupón ni una garantía
del precio. Fuente (API) y momento siempre se conservan.
"""
from __future__ import annotations
from datetime import datetime, timedelta, timezone
from hashlib import sha256
import json
from pathlib import Path
from statistics import median
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "price-history.json"
DEALS = ROOT / "deals.json"
OFFERS = ROOT / "offers.json"
MAX_DAYS = 365
MIN_DAYS = 3
DROP_THRESHOLD = 10
MIN_SAVINGS_COP = 150000
TRACKING = {"gclid", "fbclid", "msclkid", "gad_source", "igshid", "mc_cid", "mc_eid"}


def to_dt(value):
    if not value:
        return None
    try:
        stamp = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return stamp.replace(tzinfo=timezone.utc) if stamp.tzinfo is None else stamp.astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def canonical_url(url):
    try:
        parts = urlsplit(url)
        if parts.scheme != "https" or not parts.hostname:
            return ""
        query = sorted((k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                       if not k.lower().startswith("utm_") and k.lower() not in TRACKING)
        return urlunsplit(("https", parts.netloc.lower(), parts.path.rstrip("/") or "/", urlencode(query), ""))
    except (ValueError, TypeError):
        return ""


def key_for(offer):
    address = canonical_url(offer.get("url", ""))
    if not address:
        return ""
    # Merchant ID+URL; variants differing by query or path do not merge.
    return sha256((str(offer.get("seller", "")) + "|" + address).encode("utf-8")).hexdigest()[:22]


def observed_price(offer):
    if offer.get("currency") != "COP":
        return None
    try:
        listed = float(offer["price"])
        discount = float(offer.get("discount") or 0)
        coupon = float(offer.get("coupon") or 0) if offer.get("coupon_status") == "checkout_verified" else 0
        price = max(0, listed * (1 - discount / 100) - coupon)
        return round(price) if 200000 <= price <= 150000000 else None
    except (TypeError, ValueError, KeyError, OverflowError):
        return None


def normalize_observation(offer, now):
    stamp = to_dt(offer.get("checked_at"))
    key = key_for(offer)
    amount = observed_price(offer)
    if not (stamp and key and amount):
        return None
    if stamp > now + timedelta(days=1) or stamp < now - timedelta(days=MAX_DAYS):
        return None
    return {"key": key, "url": canonical_url(offer["url"]), "seller": str(offer.get("seller", ""))[:100],
            "title": str(offer.get("title", ""))[:170], "price_cop": amount,
            "observed_at": stamp.isoformat(), "source": str(offer.get("source", "unknown")),
            "verified": bool(offer.get("verified", False))}


def merge_history(previous, additions, now):
    """Idempotent: one last observation per publication and UTC calendar day."""
    series = {}
    for o in list(previous) + list(additions):
        if not isinstance(o, dict) or not o.get("key"):
            continue
        stamp = to_dt(o.get("observed_at"))
        if not stamp or stamp < now - timedelta(days=MAX_DAYS) or stamp > now + timedelta(days=1):
            continue
        key = (o["key"], stamp.date().isoformat())
        if key not in series or stamp >= to_dt(series[key]["observed_at"]):
            series[key] = o
    return sorted(series.values(), key=lambda r: (r["key"], r["observed_at"]))


def detect_deals(observations, now):
    groups = {}
    for o in observations:
        groups.setdefault(o["key"], []).append(o)
    deals = []
    for key, values in groups.items():
        values.sort(key=lambda o: o["observed_at"])
        latest = values[-1]
        latest_at = to_dt(latest["observed_at"])
        if latest_at is None or latest_at < now - timedelta(hours=72):
            continue
        base = [v["price_cop"] for v in values[:-1]
                if to_dt(v["observed_at"]) >= latest_at - timedelta(days=90)]
        # Values are daily; require 3 earlier independent observation dates.
        if len(base) < MIN_DAYS:
            continue
        mid = median(base)
        drop = (mid - latest["price_cop"]) / mid * 100 if mid else 0
        savings = mid - latest["price_cop"]
        if drop < DROP_THRESHOLD or savings < MIN_SAVINGS_COP:
            continue
        deals.append({"key": key, "title": latest["title"], "seller": latest["seller"],
                      "url": latest["url"], "latest_price_cop": latest["price_cop"],
                      "baseline_median_cop": round(mid), "drop_pct": round(drop, 1),
                      "saving_cop": round(savings), "previous_days": len(base),
                      "observed_at": latest["observed_at"], "source": latest["source"],
                      "verified": False, "status": "candidato: precios de fuente no auditados"})
    return sorted(deals, key=lambda d: (-d["drop_pct"], -d["saving_cop"]))


def run(root=ROOT, now=None):
    root = Path(root)
    now = now or datetime.now(timezone.utc)
    feed = json.loads((root / "offers.json").read_text(encoding="utf-8"))
    old = json.loads((root / "price-history.json").read_text(encoding="utf-8"))
    incoming = [normalize_observation(o, now) for o in feed.get("offers", [])]
    incoming = [o for o in incoming if o]
    history = merge_history(old.get("observations", []), incoming, now)
    deals = detect_deals(history, now)
    (root / "price-history.json").write_text(json.dumps(
        {"schema_version": 1, "updated_at": now.isoformat(), "count": len(history),
         "disclaimer": "Observaciones de proveedor o vendedor; sin checkout verificado y sin flete/impuestos salvo que se indiquen.",
         "observations": history}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "deals.json").write_text(json.dumps(
        {"schema_version": 1, "updated_at": now.isoformat(),
         "min_historical_days": MIN_DAYS, "threshold_pct": DROP_THRESHOLD,
         "disclaimer": "Caídas de precio frente a la mediana histórica, no descuentos certificados ni cupones probados.",
         "deals": deals}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Historia:", len(history), "observaciones.", "Posibles oportunidades:", len(deals))
    return history, deals


if __name__ == "__main__":
    run()
