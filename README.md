# Auditing explanations and proposed repairs

Task 1b research materials: a repeatable way to test whether a model's explanation or proposed repair supports its conclusion. Models often get the main verdict right; the examples here separately assess what they say next.

Start with the [submission](1b/submission/1b_submission.md), then the [results and exact sample references](1b/submission/1b_results.md). The submission contains three questions, their rubrics, short counterexamples and limitations.

## What the evidence supports

| Selected example | Confirmation finding |
| --- | --- |
| Archive support, b25-01 | DeepSeek accepted an invalid guarantee in 1 of 3 repeats. |
| Additive repair, b25-04 | Fable proposed a clearly insufficient repair in 1 of 3 repeats. One underspecified answer and one boundary case are excluded from clear failure counts. |
| Decoder explanation, b26-05 | False converse/equivalence claims in Fable 2/3 and Opus 1/3 answers, despite correct main verdicts. |

GPT-6 Astra and Astra Pro passed the tested examples. These selected, small samples do not establish stable failure rates, a reliable generator yield or unique priority. All grading was performed by the authoring agent, without independent human raters. The repository retains passing answers, controls, borderline cases and exclusions alongside failures.

Each group of three repeats consists of separate API calls; no explicit random seeds were set. API runs requested high reasoning effort. Codex checks used a different interface and are reported separately.

## Repository map

| Path | Contents |
| --- | --- |
| [1b/submission](1b/submission) | Polished Markdown, document composition JSON and evidence summary. |
| [templates](templates) | Reusable item and prospective audit templates. |
| [docs/methodology.md](docs/methodology.md) | Construction, controls, grading and selection process. |
| [1b/questions](1b/questions) | Exact candidate and control items from batches 24–28. Inclusion does not mean an item is hard or submission-ready. |
| [1b/tests/sets](1b/tests/sets) | Frozen confirmation sets and original prospective audit criteria. |
| [1b/tests](1b/tests) | API and Codex runners, offline evidence verifier and earlier grading utilities. |
| [1b/tests/results](1b/tests/results) | Fourteen selected runs: original screens, confirmations, stronger-model checks and controls. |

This is a focused public package from a larger search. Earlier unsuccessful batches are not included; the submission discloses that selection. See [publication scope](docs/publication_scope.md) for export details.

## Verify without model calls

Python 3.10 or later is sufficient; verification uses only the standard library and makes no network requests.

```sh
python3 1b/tests/verify_evidence.py
python3 -m unittest discover -s 1b/tests -p 'test_*.py'
```

The [verified evidence report](docs/evidence_report.md) covers 14 runs and 178 answer records. The verifier checks prompt hashes, expected sample tuples, final-answer agreement between records and audits, and published file checksums. Its tables summarize existing author-agent judgments; they do not independently validate the rubrics.

## Run new evaluations

Follow [evaluation instructions](1b/tests/README.md). New API calls require your own OpenRouter credentials and can incur charges. The recorded model identifiers are historical run settings; availability depends on the provider.

```sh
cd 1b
python3 -m venv .venv
.venv/bin/python -m pip install -r tests/requirements.txt
# Set OPENROUTER_API_KEY in your shell or credential manager first.
.venv/bin/python tests/run_openrouter.py \
  --items tests/sets/explanation_confirm \
  --models anthropic/claude-fable-5.1,anthropic/claude-opus-5,openai/gpt-6-astra \
  --n 3 --reasoning-effort high --max-tokens 16000 \
  --concurrency 3 --run my_explanation_confirmation
```

Prompts are extracted only from `## Prompt`; rubrics and construction notes are not sent. Use a fresh run name. New results and credentials are ignored by Git by default.
