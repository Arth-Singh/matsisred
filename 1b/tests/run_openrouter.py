#!/usr/bin/env python3
"""Run item prompts against models on OpenRouter and save transcripts.

Usage:
  python3 tests/run_openrouter.py --items questions/batch1 --models anthropic/claude-fable-5.1,openai/gpt-6-astra --n 3

Outputs:
  tests/results/<run>/raw.jsonl                  one line per (item, model, sample)
  tests/results/<run>/<item>/<model_slug>.md     readable transcript with all samples
"""

import argparse
import concurrent.futures
import json
import hashlib
from datetime import datetime, timezone
import os
import pathlib
import re
import sys
import time

import requests

API_URL = "https://openrouter.ai/api/v1/chat/completions"
KEY_FILE = pathlib.Path.home() / ".config" / "basins" / "openrouter.key"


def load_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        return key.strip()
    if not KEY_FILE.exists():
        sys.exit(f"No OPENROUTER_API_KEY and no key file at {KEY_FILE}")
    return KEY_FILE.read_text().strip()


def parse_item(path: pathlib.Path) -> dict:
    text = path.read_text()
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not fm:
        sys.exit(f"{path}: missing frontmatter")
    meta = {}
    for line in fm.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    m = re.search(r"^## Prompt\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        sys.exit(f"{path}: missing '## Prompt' section")
    prompt = m.group(1).strip()
    if not prompt:
        sys.exit(f"{path}: empty prompt")
    return {"id": meta.get("id", path.stem), "type": meta.get("type", ""), "prompt": prompt, "path": str(path)}


def call(key: str, model: str, prompt: str, max_tokens: int, reasoning_effort: str | None, timeout: int) -> dict:
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }
    if reasoning_effort:
        body["reasoning"] = {"effort": reasoning_effort}
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://local.redwood-1b",
        "X-Title": "redwood-1b-smoke",
    }
    delay = 5
    last_err = None
    call_started = time.monotonic()
    for attempt in range(5):
        t0 = time.time()
        try:
            r = requests.post(API_URL, headers=headers, json=body, timeout=timeout)
        except requests.RequestException as e:
            last_err = f"request error: {e}"
            time.sleep(delay)
            delay *= 2
            continue
        latency = time.time() - t0
        if r.status_code == 200:
            data = r.json()
            if "error" in data:
                last_err = f"api error: {data['error']}"
                time.sleep(delay)
                delay *= 2
                continue
            choice = data["choices"][0]
            msg = choice.get("message", {})
            return {
                "content": msg.get("content") or "",
                "reasoning": msg.get("reasoning") or "",
                "finish_reason": choice.get("finish_reason"),
                "usage": data.get("usage", {}),
                "latency_s": round(latency, 1),
                "total_latency_s": round(time.monotonic() - call_started, 1),
                "attempts": attempt + 1,
                "response_model": data.get("model"),
                "response_id": data.get("id"),
                "provider": data.get("provider"),
                "error": None,
            }
        if r.status_code in (429, 500, 502, 503, 504):
            last_err = f"http {r.status_code}: {r.text[:300]}"
            time.sleep(delay)
            delay *= 2
            continue
        return {"content": "", "reasoning": "", "finish_reason": None, "usage": {}, "latency_s": round(latency, 1),
                "provider": None, "attempts": attempt + 1,
                "total_latency_s": round(time.monotonic() - call_started, 1),
                "error": f"http {r.status_code}: {r.text[:500]}"}
    return {"content": "", "reasoning": "", "finish_reason": None, "usage": {}, "latency_s": 0, "provider": None,
            "attempts": 5, "total_latency_s": round(time.monotonic() - call_started, 1), "error": last_err}


def slug(model: str) -> str:
    return re.sub(r"[^A-Za-z0-9.-]+", "_", model)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", required=True, help="directory or single .md file")
    ap.add_argument("--models", required=True, help="comma-separated OpenRouter model ids")
    ap.add_argument("--n", type=int, default=3, help="samples per (item, model)")
    ap.add_argument("--run", default=None, help="run name; default = items dir name + timestamp")
    ap.add_argument("--max-tokens", type=int, default=6000)
    ap.add_argument("--reasoning-effort", default=None, choices=["none", "minimal", "low", "medium", "high", "xhigh", "max"], help="omit for model default")
    ap.add_argument("--concurrency", type=int, default=6)
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args()
    if min(args.n, args.max_tokens, args.concurrency, args.timeout) < 1:
        ap.error("sample count, token limit, concurrency and timeout must be positive")

    items_path = pathlib.Path(args.items)
    files = sorted(items_path.glob("*.md")) if items_path.is_dir() else [items_path]
    files = [f for f in files if f.name not in ("FORMAT.md", "README.md")]
    if not files:
        sys.exit(f"no item files under {items_path}")
    items = [parse_item(f) for f in files]
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    key = load_key()

    run_name = args.run or f"{items_path.stem}_{time.strftime('%Y%m%d_%H%M%S')}"
    out_dir = pathlib.Path(__file__).resolve().parent / "results" / run_name
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / "raw.jsonl"
    if raw_path.exists() or (out_dir / "manifest.json").exists():
        sys.exit(f"run already exists: {out_dir}; choose a new --run name")
    manifest = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "arguments": vars(args),
        "items": [{**it, "prompt_sha256": hashlib.sha256(it["prompt"].encode()).hexdigest()} for it in items],
        "models": models,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")

    jobs = [(it, m, s) for it in items for m in models for s in range(args.n)]
    print(f"{len(items)} items x {len(models)} models x {args.n} samples = {len(jobs)} calls -> {out_dir}")

    results: list[dict] = []

    def work(job):
        it, model, s = job
        res = call(key, model, it["prompt"], args.max_tokens, args.reasoning_effort, args.timeout)
        rec = {"item": it["id"], "type": it["type"], "model": model, "sample": s,
               "requested_reasoning_effort": args.reasoning_effort, "max_tokens": args.max_tokens,
               "prompt_sha256": hashlib.sha256(it["prompt"].encode()).hexdigest(), **res}
        tag = "ERR" if res["error"] else f"{res['latency_s']}s"
        print(f"  [{tag}] {it['id']} {model} #{s}", flush=True)
        return rec

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futures = [ex.submit(work, job) for job in jobs]
        for future in concurrent.futures.as_completed(futures):
            rec = future.result()
            results.append(rec)
            with raw_path.open("a") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    for it in items:
        item_dir = out_dir / it["id"]
        item_dir.mkdir(exist_ok=True)
        for model in models:
            recs = sorted([r for r in results if r["item"] == it["id"] and r["model"] == model], key=lambda r: r["sample"])
            lines = [f"# {it['id']} / {model}", ""]
            for r in recs:
                lines.append(f"## sample {r['sample']}  (latency {r['latency_s']}s, finish={r['finish_reason']}, provider={r['provider']})")
                lines.append("")
                if r["error"]:
                    lines.append(f"ERROR: {r['error']}")
                else:
                    if r["reasoning"]:
                        lines.append("<details><summary>reasoning</summary>")
                        lines.append("")
                        lines.append(r["reasoning"])
                        lines.append("")
                        lines.append("</details>")
                        lines.append("")
                    lines.append(r["content"])
                lines.append("")
            (item_dir / f"{slug(model)}.md").write_text("\n".join(lines))

    errs = sum(1 for r in results if r["error"])
    cost_tokens = sum((r["usage"].get("prompt_tokens", 0) + r["usage"].get("completion_tokens", 0)) for r in results)
    print(f"done. errors={errs} total_tokens={cost_tokens} -> {out_dir}")


if __name__ == "__main__":
    main()
