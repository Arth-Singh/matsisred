# Constructing explanation and repair audits

Begin with a research inference that needs several conditions. Find a plausible improvement or correction that satisfies one condition while leaving another unresolved. Ask the model to assess the inference, explain the problem or propose a repair.

The item needs a short, decisive grading argument. For an identification claim, construct two mechanisms with the same observable distribution and different target effects. For a repair, apply it to the answer's own example. For an explanation, retain every condition in the prompt while making the explanation false.

Develop five items by hand at a time. Use [the item template](../templates/item.md), freeze the prompts, then run a smoke check with a strong model before expanding testing. A solved item can still serve as a control. Retain items because their errors are defensible, not because a parser assigns a low score.

## Checks before counting a failure

- The prompt supplies enough information to justify the rubric. Missing assumptions are not model failures.
- The argument's mechanism supports the stated conclusion. A correct criticism does not automatically justify a repair.
- Each counterexample satisfies all stated restrictions, including outcome ranges, independence and support conditions.
- Boundary cases are checked explicitly. For example, additive binary-outcome means at zero can identify missing cells even when generic interior means cannot.
- Alternative correct answers pass. Ambiguous repairs remain ambiguous unless the answer makes a definite false claim.
- Main verdict, explanation and proposed repair are graded separately. Correct verdicts can accompany false explanations.
- Passing models and controls are audited too. They can expose an invalid key or a narrower interpretation of the result.

## Controls and confirmation

Pair the candidate with a case supplying the missing condition. Useful contrasts here include archive overlap, enough independent feature combinations for additive extrapolation, and a causally sufficient coarsening of a mediator. An explicit critique prompt tests whether models recognize a flaw they generated in a broader answer.

Write the [audit plan](../templates/audit_plan.md) before confirmation calls. Preserve the exact question text and hash. Use separate calls for each repeat and record the actual request settings; requested reasoning effort does not guarantee equal compute across providers. These published runs did not set explicit random seeds.

Exclude empty, filtered, errored and length-truncated responses from substantive error rates, while reporting those exclusions. Keep borderline cases separate. Three selected repeats show recurrence at most; they do not estimate the yield of a new generator or establish stable failure probabilities.

The published examples are b25-01, b25-04 and b26-05. Their full rubrics and counterexamples are in the [submission](../1b/submission/1b_submission.md). Historical candidate-file rubrics record the construction process; the submission and confirmation audit describe the final, conservative interpretation.
