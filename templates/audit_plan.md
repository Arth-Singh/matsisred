# Prospective audit plan

Complete this before the confirmation calls. The plan documents grading decisions; it is not sent to models.

## Scope

List the frozen item IDs and prompt hashes, model/interface settings, samples per item and stopping rule. Explain how these items were selected. Record whether a random seed is actually set.

## Main verdict

Define pass, fail and excluded outcomes for each item. Describe the evidence required to distinguish them.

## Explanation and repair

List materially false claims that count as errors. Require any proposed sufficient repair to work in the answer's own example. Describe alternative valid explanations and repairs. Keep underspecified suggestions, boundary exceptions and secondary errors separate from decisive failures.

## Controls

State which missing condition each control supplies. Include explicit flaw recognition when testing whether a model generates the same invalid repair. Keep correct controls in the report.

## Reporting

Report all planned sample tuples, completed answers, exclusions and missing responses. Keep main-verdict counts separate from explanation/repair counts. Describe post-run rubric changes and preserve the original plan. Identify who performed the grading and whether any independent review occurred.
