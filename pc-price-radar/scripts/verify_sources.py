#!/usr/bin/env python3
"""Single HEAD HTTP domain check. DOES NOT validate merchants, offers or delivery."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]

def check(s):
    req = urllib.request.Request("https://" + s["domain"] + "/", method="HEAD", headers={"User-Agent": "PCPriceRadar/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=7) as r:
            status = r.status
    except urllib.error.HTTPError as e:
        status = e.code
    except Exception:
        status = None
    state = "responded" if status is not None and 200 <= status < 400 else (
        "restricted_or_head_unsupported" if status in (401, 403, 405, 406, 429) else
        "error_response" if status is not None else "unconfirmed"
    )
    return {"domain": s["domain"], "status_code": status, "reachability": state}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=400)
    ap.add_argument("--workers", type=int, default=8)
    args=ap.parse_args()
    catalog=json.loads((ROOT/"catalog.json").read_text(encoding="utf-8"))["sources"][:max(args.limit,1)]
    with ThreadPoolExecutor(max_workers=max(1,min(12,args.workers))) as pool:
        results=list(pool.map(check,catalog))
    counts={k: sum(x["reachability"]==k for x in results) for k in ("responded","restricted_or_head_unsupported","error_response","unconfirmed")}
    data={"checked_at":datetime.now(timezone.utc).isoformat(),
          "method":"Single HTTPS HEAD to homepage, no scraping of retailer pages.",
          "disclaimer":"HTTP response is NOT seller legitimacy, a product search, a shipping check, or a stock verification.",
          "counts":counts,"results":results}
    (ROOT/"sources-status.json").write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("HTTP checks:",len(results),counts)

if __name__=="__main__":main()
