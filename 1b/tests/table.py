"""Usage: python3 tests/table.py b12-02:batch12_smoke b14-02:batch14_smoke ...
Markdown pass table (passes/valid samples) for chosen items across runs, using grade.py's KEY and parsers."""
import sys, json, pathlib, importlib.util
root = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("grade", root / "tests/grade.py"); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
models = ["anthropic/claude-fable-5.1","anthropic/claude-opus-5","openai/gpt-6-astra","google/gemini-3.1-pro-preview","moonshotai/kimi-k3","deepseek/deepseek-v4-pro"]
short = ["Fable 5.1","Opus 5","GPT-6","Gemini 3.1 Pro","Kimi K3","DeepSeek V4"]
pairs = [a.split(":") for a in sys.argv[1:]]   # item:run
print("| item | " + " | ".join(short) + " |"); print("|---|" + "---|"*len(short))
for item, run in pairs:
    rows = [json.loads(l) for l in (root/"tests/results"/run/"raw.jsonl").read_text().splitlines() if l.strip()]
    key = g.KEY[item]; cells = []
    for m in models:
        rs = [r for r in rows if r["item"] == item and r["model"] == m]
        valid = [r for r in rs if not g.invalid_reason(r) and g.coverage_verdicts(r["content"], key["n"]) is not None]
        ok = 0
        for r in valid:
            v = g.coverage_verdicts(r["content"], key["n"])
            if v is not None and {i + 1 for i, x in enumerate(v) if x == "YES"} == set(key["yes"]):
                ok += 1
        cells.append(f"{ok}/{len(valid)}" if valid else ("—" if not rs else "excluded"))
    print(f"| {item} | " + " | ".join(cells) + " |")
