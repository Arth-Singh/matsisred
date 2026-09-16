# Item file format

One markdown file per item, `questions/batchN/<id>.md`.

```
---
id: b1-01
type: reply-coverage | verbal-dispute | redundancy
title: short title
domain: alignment-eval | training-dynamics | game-theory
status: draft | smoke | tested | verified | rejected
---

## Prompt
Verbatim text sent to the model. Ends at the next H2.

## Rubric
Planted answer and the grading rule.

## Justification
Why the rubric answer is right and the typical model answer is wrong.

## Construction
Hidden structure: mechanisms, which objection is which, hard negatives.

## Test log
Appended by hand after runs.
```

The harness reads only the `## Prompt` section.
