---
id: example-01
type: explanation-repair-audit
title: Replace with a descriptive title
domain: alignment-eval
status: draft
---

## Prompt
Replace this paragraph with the complete question. State all relevant assumptions, ask for the main judgment and an explanation or repair, and specify a word limit if useful. Keep the question within one page. Only this section is sent to the model.

## Rubric
State the correct main verdict. Grade explanation and repair validity separately. Identify a concrete claim that would count as an error and describe acceptable alternative answers. Specify how ambiguous or incomplete suggestions will be recorded.

## Justification
Give a small counterexample or pair of mechanisms. Show that each satisfies the prompt and that the proposed inference, explanation or repair fails. Check boundary cases before calling an answer wrong.

## Construction
Record the condition the argument satisfies and the condition it still lacks. Explain the plausible but invalid next step. Design a matched valid control and, where useful, an explicit critique version of the same flaw.

## Test log
Record run name, model/interface, sample count, requested reasoning effort, token limit, prompt hash, main verdict, explanation/repair grade, exclusions and exact answer references. Distinguish discovery runs from confirmations. Do not overwrite earlier prompts after testing.
