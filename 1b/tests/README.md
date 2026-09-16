# Evaluation pipeline

Run evaluation commands from `1b/`. Python 3.10 or later is required by the API runner. Offline evidence verification needs no third-party packages and makes no network requests.

```sh
python3 tests/verify_evidence.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

## API runner

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r tests/requirements.txt
```

Set `OPENROUTER_API_KEY` through your shell or credential manager. The runner also supports `~/.config/basins/openrouter.key`. Keep the value out of this repository. These commands make new, potentially paid API requests; offline verification does not.

Example reproduction of the two-item explanation confirmation:

```sh
.venv/bin/python tests/run_openrouter.py \
  --items tests/sets/explanation_confirm \
  --models anthropic/claude-fable-5.1,anthropic/claude-opus-5,openai/gpt-6-astra \
  --n 3 --reasoning-effort high --max-tokens 16000 \
  --concurrency 3 --run my_explanation_confirmation
```

For the support target and control:

```sh
.venv/bin/python tests/run_openrouter.py \
  --items tests/sets/support_confirm \
  --models deepseek/deepseek-v4-pro \
  --n 3 --reasoning-effort high --max-tokens 16000 \
  --concurrency 3 --run my_support_confirmation
```

Use `tests/sets/explanation_candidates` and `tests/sets/decoder_pro` for the stronger-model checks, with the historical `openai/gpt-6-astra-pro` identifier, `--n 1` and `--max-tokens 32000`. Model identifiers reflect the recorded experiments; provider availability can change.

The runner reads only `## Prompt`, writes exact prompts and SHA-256 hashes to `manifest.json`, and saves each response as it completes. It refuses an existing run name. Repeats are separate calls without a seed parameter. New run output is ignored by Git to allow review before publication.

## Codex smoke runner

An installed, authenticated Codex CLI is required:

```sh
bash tests/run_codex.sh questions/batch25 1
```

The script uses the local Codex model and effort configuration, adds an answer-only/no-tools prefix and requests a read-only sandbox. It does not pin a model. Published runs were checked as GPT-6 Astra at xhigh. Inspect each new `.stderr` header before labeling the run. A failed call leaves an error log and must not be counted as a completed answer. Never publish authentication files or unreviewed local logs.

## Grading and exclusions

Grade the main verdict and explanation/repair separately using the submission's rubrics and a prospective audit plan. Inspect all answers, including passing models. Keep underspecified, boundary and secondary-error cases separate from decisive failures.

Empty, filtered, errored and length-truncated responses are exclusions, not incorrect conceptual answers. Opus sometimes returned `content_filter` on benign earlier items. Long waits and out-of-order completion do not imply that an earlier request failed. The runner may retry transient errors; `attempts` records that distinction.

`grade.py`, `audit.py` and `table.py` apply to earlier coverage-style items. **They do not grade the final b25/b26 examples.** Some stored historical keys were withdrawn. For this package, `verify_evidence.py` verifies the included records and summarizes the manual audits; it does not independently judge answer correctness.
