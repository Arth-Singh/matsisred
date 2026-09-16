"""Usage: python3 tests/audit.py <run_name> <objection_number>
Prints, per item and model, each sample's verdict on that objection and the sentence justifying it."""
import json, re, sys, collections
from grade import KEY, coverage_verdicts, invalid_reason
run, target = sys.argv[1], int(sys.argv[2])
import pathlib
rows = [json.loads(l) for l in open(pathlib.Path(__file__).resolve().parent / "results" / run / "raw.jsonl")]
rows.sort(key=lambda r: (r["item"], r["model"]))
by = collections.defaultdict(list)
for r in rows:
    by[(r["item"], r["model"].split("/")[-1])].append(r)
for (item, model), rs in by.items():
    print(f"\n##### {item}  {model}")
    for r in sorted(rs, key=lambda r: r["sample"]):
        k = r["sample"]
        text = r.get("content") or ""
        if not text.strip():
            print(f"  [{k}] EMPTY finish={r.get('finish_reason')}")
            continue
        # verdict line
        verdicts = coverage_verdicts(text, KEY[item]["n"])
        v = verdicts[target - 1] if verdicts else "?"
        # justification: the sentence/line mentioning the target objection number after verdict list
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        just = ""
        for l in lines:
            if re.match(rf"^\W*(objection\s*)?{target}\b", l, re.I) and len(l) > 40:
                just = l
        if not just:
            for l in lines:
                if re.match(rf"^\W*(objection\s*)?{target}\b", l, re.I):
                    just = l
        print(f"  [{k}] {v}: {just[:420]}")
