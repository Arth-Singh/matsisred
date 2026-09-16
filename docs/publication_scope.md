# Publication scope and evidence provenance

This repository packages Task 1b's final submission, reusable construction templates, evaluation scripts and selected supporting evidence. It includes batches 24–28 and fourteen related API/Codex runs. These are a selected portion of a broader search, not a random sample of generated items. Earlier batches were largely solved; they are not represented as hard-item successes.

## Published evidence

API run directories contain the original request manifest, author-agent audit and summary. `raw.jsonl` is a public export: the `reasoning` field is removed from every record. Final answers and all other record fields are preserved, including errors, finish reasons, prompt hashes, model/provider identifiers, usage, latency and attempt counts. No samples were dropped. Each `public_export.json` records the transformation and the original private raw-file hash. That original hash records provenance; the original file is not part of this package.

Codex runs contain the original final-answer files and author-agent audits with exact question text and hashes. Local stderr logs, local paths and authentication files are not included. The recorded model/effort fields in those audits reflect the headers checked during the original work. Codex used an answer-only, no-tools prefix; it is a distinct interface from the direct API calls.

The root `evidence_checksums.json` covers published evidence, prompts, frozen sets and submission files. `verify_evidence.py` checks those files and internal record consistency without making model calls. It does not independently assess the scientific grading judgments. Hashes detect changes relative to this snapshot; they are not third-party timestamps or proof of novelty.

Private handovers, personal process notes, credentials, provider reasoning traces, the supplied work-test source and unrelated Task 2 materials are outside this package. No credentials are needed to read or verify the included evidence.

## Grading history

The explanation confirmation plan was written before that run. The zero-boundary additive exception was identified during audit and handled conservatively: that answer is excluded from decisive-error counts. The original plan, complete answers and final audit are retained so readers can inspect this change.

`grade.py`, `audit.py` and `table.py` are earlier utilities for keyed coverage questions. Their stored keys do not grade the three final examples and some historical keys were withdrawn. They are included as pipeline history only. Use the manual audits and offline verifier for this submission, not the legacy pass tables.
