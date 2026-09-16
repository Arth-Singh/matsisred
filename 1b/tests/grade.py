#!/usr/bin/env python3
"""Grade a results run against the batch answer key.

Usage: python3 tests/grade.py tests/results/<run>/raw.jsonl

Reply-coverage items: extracts the YES/NO verdict list and compares to KEY.
Verbal-dispute items: extracts the leading yes/no only; the proposition must be checked by hand.
"""

import collections
import json
import pathlib
import re
import sys

KEY = {
    "b1-01": {"n": 8, "yes": {1, 4, 7}},
    "b1-02": {"n": 7, "yes": {2, 4, 6}},
    "b1-03": {"n": 7, "yes": {2, 4, 6}},
    "b1-04": {"verbal": True},
    "b1-05": {"verbal": False},
    "b1-01v2": {"n": 8, "yes": {1, 4, 7}},
    "b1-02v2": {"n": 7, "yes": {2, 4, 6}},
    "b1-03v2": {"n": 7, "yes": {2, 4, 6}},
    "b2-01": {"n": 7, "yes": {1, 4, 7}},
    "b2-02": {"n": 7, "yes": {1, 4, 6}},
    "b2-03": {"n": 7, "yes": {1, 3, 5}},
    "b2-04": {"n": 7, "yes": {1, 3, 5}},
    "b2-05": {"n": 8, "yes": {2, 5}},
    "b2-01f": {"n": 7, "yes": {1, 4, 7}},
    "b2-02f": {"n": 7, "yes": {1, 4, 6}},
    "b2-03f": {"n": 7, "yes": {1, 3, 5}},
    "b2-04f": {"n": 7, "yes": {1, 3, 5}},
    "b2-05f": {"n": 8, "yes": {2, 5}},
    "b1-01f": {"n": 8, "yes": {1, 4, 7}},
    "b1-02f": {"n": 7, "yes": {2, 4, 6}},
    "b1-03f": {"n": 7, "yes": {2, 4, 6}},
    "b1-02g": {"n": 7, "yes": {2, 4, 6}},
    "b3-01": {"n": 4, "yes": {2, 3}},
    "b3-02": {"n": 4, "yes": {1, 3}},
    "b3-03": {"n": 4, "yes": {2, 3}},
    "b3-04": {"n": 4, "yes": {1, 3}},
    "b3-05": {"n": 4, "yes": {1, 3}},
    "b4-01": {"n": 4, "yes": {1, 3}},
    "b4-02": {"n": 4, "yes": {1, 3}},
    "b4-03": {"n": 4, "yes": {2, 3}},
    "b4-04": {"n": 4, "yes": {1, 3}},
    "b4-05": {"n": 4, "yes": {1, 3}},
    "b5-01a": {"n": 7, "yes": {2, 4, 6}},
    "b5-01b": {"n": 7, "yes": {2, 4, 6}},
    "b4-03b": {"n": 4, "yes": {2, 3}},
    "b4-05b": {"n": 4, "yes": {1, 3}},
    "b6-01": {"letter": "A"},
    "b6-02": {"letter": "B"},
    "b6-03": {"letter": "A"},
    "b9-01": {"n": 4, "yes": {1, 3}},
    "b9-02": {"n": 4, "yes": {1, 4}},
    "b9-03": {"n": 4, "yes": {1, 3}},
    "b9-04": {"n": 4, "yes": {1, 3}},
    "b9-05": {"n": 4, "yes": {1, 3}},
    "b10-01": {"n": 4, "yes": {2, 3}},
    "b10-02": {"n": 4, "yes": {4}},
    "b10-03": {"n": 4, "yes": {3}},
    "b10-04": {"n": 4, "yes": {3}},
    "b10-05": {"n": 4, "yes": {3}},
    "b11-01": {"n": 4, "yes": {1, 4}},
    "b11-02": {"n": 4, "yes": {1, 3}},
    "b11-03": {"n": 4, "yes": {1, 3}},
    "b11-04": {"n": 4, "yes": {1, 3}},
    "b11-05": {"n": 4, "yes": {1, 3}},
    "b12-01": {"n": 4, "yes": {1, 3}},
    "b12-02": {"n": 4, "yes": {1, 3}},
    "b13-01": {"n": 4, "yes": {1, 3}},
    "b13-02": {"n": 4, "yes": {1, 3}},
    "b14-01": {"n": 4, "yes": {1, 3}},
    "b14-02": {"n": 4, "yes": {1, 3}},
    "b14-03": {"n": 4, "yes": {1, 3}},
    "b14-04": {"n": 4, "yes": {1, 3}},
    "b14-05": {"n": 4, "yes": {1, 3}},
    "b15-01": {"n": 4, "yes": {1, 3}},
    "b16-01": {"n": 4, "yes": {1, 3}},
    "b16-02": {"n": 4, "yes": {1, 3}},
    "b16-03": {"n": 4, "yes": {1, 3}},
    "b16-04": {"n": 4, "yes": {1, 3}},
    "b16-05": {"n": 4, "yes": {3}},
    "b17-01": {"n": 4, "yes": {1, 3}},
    "b17-02": {"n": 4, "yes": {1, 3}},
    "b17-03": {"n": 4, "yes": {1, 3}},
    "b17-04": {"n": 4, "yes": {1, 3}},
    "b17-05": {"n": 4, "yes": {3}},
}

# Anchor to numbered lines, allowing short labels such as "1. Noise — YES".
# Unanchored matches can mistake numbers inside explanations for verdicts.
NUMBERED = re.compile(
    r"^[ \t]*(?:[-*][ \t]+)?\**(?:objection[ \t]+)?([1-9]\d*)\**"
    r"[ \t]*[.):\-–—]+[ \t]*\**"
    r"(?:[^\n:—–]{1,80}[:—–][ \t]*)??\**(YES|NO)\b",
    re.I | re.M,
)
BARE = re.compile(r"\b(YES|NO)\b", re.I)


def invalid_reason(record: dict) -> str | None:
    """Exclude transport failures and incomplete answers from accuracy rates."""
    if record.get("error"):
        return "ERR"
    if record.get("finish_reason") == "content_filter":
        return "filtered"
    if record.get("finish_reason") in ("length", "max_tokens"):
        return "truncated"
    if not (record.get("content") or "").strip():
        return "empty"
    return None


def coverage_verdicts(text: str, n: int) -> list[str] | None:
    # Prefer the explicitly requested verdict list over later explanations,
    # which can contain corrections or quoted alternative answers.
    for line in text.splitlines()[:6]:
        tokens = BARE.findall(line)
        remainder = re.sub(r"\b(?:yes|no|verdicts?|answers?|objections?)\b", "", line, flags=re.I)
        if len(tokens) == n and not re.search(r"[A-Za-z]", remainder):
            return [token.upper() for token in tokens]
    numbered = {}
    for m in NUMBERED.finditer(text):
        k = int(m.group(1))
        if 1 <= k <= n and k not in numbered:
            numbered[k] = m.group(2).upper()
    if len(numbered) == n:
        return [numbered[k] for k in range(1, n + 1)]
    toks = [m.group(1).upper() for m in BARE.finditer(text)]
    if len(toks) >= n:
        return toks[:n]
    return None


def verbal_verdict(text: str) -> str:
    head = text.strip()[:400].lower()
    if re.match(r"^\W*(\*\*)?\s*yes\b", head):
        return "yes"
    if re.match(r"^\W*(\*\*)?\s*no\b", head):
        return "no"
    if "no substantive disagreement" in head or "merely verbal" in head or "verbal dispute" in head:
        return "no"
    if "yes" in head[:40]:
        return "yes"
    if "no" in head[:40]:
        return "no"
    return "?"


def main() -> None:
    path = pathlib.Path(sys.argv[1])
    recs = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    rows = []
    for r in recs:
        item, model, s = r["item"], r["model"], r["sample"]
        key = KEY.get(item)
        invalid = invalid_reason(r)
        if invalid:
            rows.append((item, model, s, invalid, "excluded", False))
            continue
        text = r["content"]
        if key is None:
            rows.append((item, model, s, "nokey", "", False))
        elif "letter" in key:
            head = text.strip()[:300]
            m = re.search(r"\b([AB])\b", head)
            v = m.group(1) if m else "?"
            if re.search(r"\bboth\b|\bequal", head, re.I) and not re.match(r"^\W*\**\s*[AB]\b", head):
                v = "both"
            rows.append((item, model, s, v, key["letter"], v == key["letter"]))
        elif "verbal" in key:
            v = verbal_verdict(text)
            want = "no" if key["verbal"] else "yes"
            rows.append((item, model, s, v, want, v == want))
        else:
            v = coverage_verdicts(text, key["n"])
            if v is None:
                rows.append((item, model, s, "unparsed", "", False))
                continue
            got = {i + 1 for i, x in enumerate(v) if x == "YES"}
            want = key["yes"]
            diff = sorted(got ^ want)
            rows.append((item, model, s, "".join("Y" if x == "YES" else "N" for x in v), f"diff={diff}" if diff else "", got == want))

    print(f"{'item':6} {'model':36} {'s':>1}  {'verdict':10} {'note':22} ok")
    for item, model, s, v, note, ok in sorted(rows):
        excluded = v in ("ERR", "filtered", "truncated", "empty", "nokey", "unparsed")
        print(f"{item:6} {model:36} {s:>1}  {v:10} {note:22} {'EXCLUDED' if excluded else 'PASS' if ok else 'FAIL'}")

    print("\nPass rate per item x model (passes/samples):")
    by = collections.defaultdict(lambda: [0, 0])
    for item, model, s, v, note, ok in rows:
        if v in ("ERR", "filtered", "truncated", "empty", "nokey", "unparsed"):
            by[(item, model)]
            continue
        by[(item, model)][1] += 1
        by[(item, model)][0] += int(ok)
    models = sorted({m for _, m in by})
    items = sorted({i for i, _ in by})
    print(f"{'':6} " + " ".join(f"{m.split('/')[-1][:14]:>14}" for m in models))
    for it in items:
        print(f"{it:6} " + " ".join(f"{by[(it, m)][0]}/{by[(it, m)][1]:>12}" if (it, m) in by else f"{'-':>14}" for m in models))

    print("\nItem difficulty (fraction of all samples failing):")
    for it in items:
        tot = sum(by[(it, m)][1] for m in models if (it, m) in by)
        ok = sum(by[(it, m)][0] for m in models if (it, m) in by)
        print(f"  {it}: {tot - ok}/{tot} valid samples disagree with key")


if __name__ == "__main__":
    main()
