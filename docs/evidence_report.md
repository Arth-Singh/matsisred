# Published evidence verification

Offline consistency checks only. Grades below are author-agent judgments, not independent regrading.

| Run | Records | Main passes | Main failures | Excluded | Other judgments |
| --- | ---: | ---: | ---: | ---: | --- |
| batch24_correction_high_20260917 | 25 | 19 | 0 | 1 | provisional_fail: 4, qualified: 1 |
| batch25_support_high_20260917 | 25 | 24 | 1 | 0 | none |
| batch26_properties_high_20260917 | 25 | 25 | 0 | 0 | none |
| batch27_repairs_high_20260917 | 25 | 24 | 0 | 1 | none |
| batch28_boundary_high_20260917 | 25 | 25 | 0 | 0 | none |
| codex_batch24_20260917_010842 | 5 | 5 | 0 | 0 | none |
| codex_batch25_20260917_011922 | 5 | 5 | 0 | 0 | none |
| codex_batch26_20260917_012524 | 5 | 5 | 0 | 0 | none |
| codex_batch27_20260917_013230 | 5 | 5 | 0 | 0 | none |
| codex_batch28_20260917_014118 | 5 | 5 | 0 | 0 | none |
| decoder_astra_pro_high_20260917 | 1 | 1 | 0 | 0 | none |
| explanation_candidates_astra_pro_high_20260917 | 3 | 3 | 0 | 0 | none |
| explanation_confirm_high_20260917 | 18 | 18 | 0 | 0 | none |
| support_confirm_deepseek_high_20260917 | 6 | 5 | 1 | 0 | none |

## Explanation grades in selected confirmations

These categories are separate from the main-verdict counts above. Borderline categories are not decisive errors.

| Item | Model | Explanation/repair grade | Count |
| --- | --- | --- | ---: |
| b24-02 | deepseek/deepseek-v4-pro | pass | 1 |
| b24-02 | deepseek/deepseek-v4-pro | secondary_error | 2 |
| b25-01 | deepseek/deepseek-v4-pro | fail | 1 |
| b25-01 | deepseek/deepseek-v4-pro | pass | 2 |
| b25-04 | anthropic/claude-fable-5.1 | boundary_caveat_not_counted | 1 |
| b25-04 | anthropic/claude-fable-5.1 | repair_fail | 1 |
| b25-04 | anthropic/claude-fable-5.1 | underspecified_repair | 1 |
| b25-04 | anthropic/claude-opus-5 | underspecified_repair | 3 |
| b25-04 | openai/gpt-6-astra | pass | 3 |
| b26-05 | anthropic/claude-fable-5.1 | explanation_fail | 2 |
| b26-05 | anthropic/claude-fable-5.1 | overclaim_not_primary_count | 1 |
| b26-05 | anthropic/claude-opus-5 | explanation_fail | 1 |
| b26-05 | anthropic/claude-opus-5 | pass | 2 |
| b26-05 | openai/gpt-6-astra | pass | 3 |

Verified 113 files, 14 runs and 178 answer records. All three submission questions match the tested prompts.
