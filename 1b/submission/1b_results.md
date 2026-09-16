# Evidence accompanying the delivered Task 1b document

Final document: [Task 1b submission](1b_submission.md).

The submitted examples are b25-01, b25-04 and b26-05. These counts are **targeted errors in selected confirmation samples**, not a universal accuracy score. Verdict errors and explanation/repair errors are different outcomes. Prompts are unchanged from original screens.

| Example | Model / interface | Confirmation evidence |
|---|---|---|
| 1: archive support | DeepSeek V4 Pro API | 1/3 unqualified invalid guarantees; 2/3 correct. Initial screen also failed. |
| 1: support supplied | DeepSeek V4 Pro API control | 3/3 accept the valid CDE inference. Two answers have secondary explanatory mistakes; main control verdict is correct. |
| 1 | Fable, Opus, Gemini, Kimi API; Codex Astra; Astra Pro API | All available single-sample target checks correct. |
| 2: adequate repair | Fable 5.1 API | 1/3 unambiguous interior-probability repair failure; 1 underspecified repair; 1 boundary case excluded from decisive-error count. All primary verdicts correct. |
| 2 | Opus 5 API | 3/3 list underspecified repairs; no unambiguous targeted failure counted. |
| 2 | GPT-6 Astra API | 3/3 correct; Astra Pro single check correct. Initial other-family verdicts correct. |
| 3: decoder explanation | Fable 5.1 API | 2/3 explicit false converse/equivalence claims; third broader overclaim excluded from strict count. All verdicts correct. |
| 3 | Opus 5 API | 1/3 explicit false converse/equivalence claims. All verdicts correct. |
| 3 | GPT-6 Astra API | 3/3 correct; Astra Pro single check correct. Other-family initial verdicts correct. |

## Exact confirmation records

- `tests/results/support_confirm_deepseek_high_20260917/`: six responses; Example1 target and support control, three each. Target failing sample1. Audited prompt hashes, tuples and model settings.
- `tests/results/explanation_confirm_high_20260917/`:18 responses; Examples2/3, Fable/Opus/GPT-6 Astra, three each. Example2 decisive failure: Fable sample2. Example3 strict failures: Fable samples0,2 and Opus sample0.
- `tests/sets/explanation_confirm/AUDIT_PLAN.txt`: separate prospective explanation/repair criteria written before that confirmation run. The zero-boundary caveat emerged during audit and was handled conservatively.
- `tests/results/explanation_candidates_astra_pro_high_20260917/`: Pro checks Examples1/2 and b27-02, all correct.
- `tests/results/decoder_astra_pro_high_20260917/`: Pro check of Example3, correct.
- Original screens and follow-up controls: batch25, batch26, batch27 and batch28 run directories. Every completed run has an author-agent manual audit and summary.

## Controls and counterevidence

Batch27:24 substantive API target passes, one DeepSeek b27-03 length exclusion; Codex5/5. Batch28:25 substantive API target passes; Codex5/5. Explicitly asking why a repair suffices elicits sufficient repairs from every tested family. The exact-zero additive boundary is also solved by all. These are evidence of task-form sensitivity, not hard-item wins. Subsidiary errors are preserved separately.

No samples were silently replaced. The three examples were selected after a broad search, so neither original nor confirmation counts estimate fresh-generator yield. Audits are author-agent judgments, not independent human ratings. GPT passes and borderline conceptual/technical scope are disclosed in the delivered document.
