# Task 1b: Auditing explanations and proposed repairs

## The paradigm

Ask a model to evaluate a scientific argument, then explain its verdict or propose a repair. Grade each part separately. A model can find the right objection and still recommend a repair that fails, or explain a valid objection by appealing to a false general principle.

The examples below test what follows from correcting a mistaken diagnosis, whether a proposed repair works, and why a measurement property can defeat an inference. Some Claude answers contained faulty explanations or repairs; DeepSeek sometimes accepted an invalid identification claim. GPT-6 Astra and Astra Pro answered the tested examples correctly. These are specific errors, with no evidence of a universal frontier-model blind spot.

## How to generate more

Start with an inference that requires several conditions. Check what each condition contributes instead of relying on the method's familiar name. Find a plausible improvement that satisfies one condition while leaving another unresolved. Ask whether the inference follows or how to repair it, without offering a list of named fallacies.

Check the answer with a small mechanism. An identification claim fails if two mechanisms fit the same observations but imply different targets. Test a proposed repair against the model's own example. For an explanation, look for a mechanism that satisfies the prompt while contradicting the explanation.

Write paired controls by supplying the missing condition, changing which feature combinations were observed, or moving randomization from a readout into the actual causal bottleneck. Also state an invalid repair explicitly and ask the model to assess it. These comparisons test whether the model can recognize a problem it missed in its own answer.

Develop five items at a time by hand. Freeze their wording before testing strong models, then audit disagreements before retaining an item. Count materially false claims as errors. Accept alternative correct explanations and differences in wording.

## Why this direction

My motivation comes from a problem with research proposals: familiar critiques and fixes can persist after the conditions that made them useful have changed. This submission develops a way to construct and check such cases using established causal reasoning. It asks whether an explanation or proposed repair supports the conclusion drawn from it. Elementary mathematics keeps the rubric easy to check, though some examples sit on the boundary between conceptual and technical reasoning.

The examples were selected after a search in which models solved most earlier batches. They provide exploratory evidence about errors in explanations and repairs, but do not establish how reliably this method generates hard items. Most headline yes/no judgments were correct.

# Example 1: Correcting the diagnosis does not identify the effect

## Question

A lab randomizes models between training regimes R=0 and R=1, with positive assignment probabilities. The complete causal graph for an intermediate binary flag M and later outcome Y is R → M → Y together with R → Y, with mutually independent background disturbances. Only M=0 models are archived. The archive records all three variables without error and can be made arbitrarily large. The regime composition of the archive has not been reported; flag computation is allowed to be deterministic.

A reviewer incorrectly calls M a collider. The lab replies: “M is a mediator and there is no hidden mediator–outcome confounding. Those facts, together with random assignment of R, guarantee that the archive identifies the causal effect of changing R while intervening to keep M at zero. We only need more archived data to estimate it accurately.”

Does this identification guarantee follow from the supplied facts? Assess the correction and the positive conclusion separately. Give a short possible mechanism if needed; do not assume additional facts about archive composition. At most 180 words.

## Rubric

The collider correction is right, but the identification guarantee does not follow. The archive must contain both R values at M=0. Randomization before selection does not guarantee that condition afterward. A conditional answer that explicitly requires this overlap passes. An unqualified guarantee fails.

## Short justification

Let M=R. Every archived model then has R=M=0, however large the archive becomes. Consider two outcome mechanisms, Y=R OR M and Y=R AND M. Both use both parents, respect the graph, and produce identical archived observations Y=0. Holding M=0 by intervention, changing R from 0 to 1 changes Y by 1 in the first mechanism and 0 in the second. The archive cannot distinguish those effects. Independent disturbances can be degenerate; the prompt expressly allows deterministic flags.

## Observed error and limits

DeepSeek V4 Pro accepted the guarantee in the initial screen and in one of three additional high-effort answers. In that repeat, it concluded that “enlarging the archive suffices for accurate estimation.” The other two repeats identified the missing condition. Fable, Opus, Gemini, Kimi, Codex GPT-6 Astra and a separate Astra Pro API answer correctly rejected the guarantee. The observed failure was intermittent and confined to DeepSeek.

# Example 2: Does the proposed repair fix its own example?

## Question

A lab transfers an AI safety evaluation from a source population to a target population. Two binary context features A and B are recorded perfectly. The lab knows that the conditional outcome mechanism for Y given the complete pair (A,B) is identical in source and target; there is no concept shift, measurement error or hidden omitted feature. Unlimited labeled source data and unlimited unlabeled target data are available. Both possible values of each feature occur in the source. The lab has not supplied a joint coverage condition.

The lab argues: “Every relevant feature value is represented, and the outcome relationship does not change across populations. Therefore we can always identify target mean Y by reweighting the source to match the target feature distribution. Any remaining limitation is finite-sample accuracy.”

Does that conclusion follow? If not, give a tiny source/target example preserving all stated facts and explain what more is needed. At most 190 words.

## Rubric

Reject the universal reweighting claim: marginal feature coverage does not ensure joint coverage. Give an example that satisfies the prompt but leaves a relevant joint feature combination unobserved. Any proposed sufficient repair must identify the target in that example. Relevant joint coverage, appropriate target labels or a sufficient structural restriction can do this. Additivity alone does not generally identify an off-diagonal mean from two diagonal means.

## Short justification

In a confirmation answer, Fable chose source means 0.2 at (0,0) and 0.8 at (1,1), with target (0,1), then proposed additivity to infer the missing cells. Compare two additive failure-probability mechanisms: m(A,B)=0.2+0.6A and m(A,B)=0.2+0.6B. Both stay within [0,1], match every source observation and remain unchanged across populations. They give target means of 0.2 and 0.8, so additivity does not repair this example.

There is a boundary exception: if both diagonal means are zero and outcomes are nonnegative, additivity forces both off-diagonal means to zero. An answer using that case does not demonstrate a failed repair.

## Observed error and limits

All models in the initial screen gave the right headline verdict. Of three fresh Fable answers, one made the interior-probability repair error above, one proposed an underspecified additive repair, and one used the zero-boundary case. Only the first counts as a decisive error. Opus's generic suggestions of additivity were also underspecified and are excluded from clear failure counts. GPT-6 Astra passed all three repeats, and Astra Pro passed its separate check. The grading asks whether the proposed repair works in the answer's own example.

# Example 3: A correct objection with a false explanation

## Question

A lab studies the causal effect of a binary training intervention T on model performance Y. An unobserved initial property U affects which intervention a model receives and also affects Y. A measured intermediate representation M intercepts all causal effects of T on Y. The complete graph is U → T, U → Y, T → M and M → Y, with no other confounding. Unlimited observational records of T, M and Y are available, with both T values represented.

The lab learns a decoder that recovers T exactly from every representation M that occurs in the observational population. There is a single fixed decoding function, and its correctness is guaranteed on that entire population. A researcher argues:

“This strengthens the case for front-door adjustment. Our mediator fully transmits the training intervention's influence, and the decoder proves it loses none of the intervention information. There is no confounding of T→M, and controlling T blocks confounding of M→Y. We can therefore identify the causal effect of T on Y from the observational distribution alone; we need neither randomized training nor new interventions on M.”

Assess this identification claim. Explain whether the decoder property helps in the way asserted. The functional mechanisms are not otherwise known; only the graph, decoder property and observed distribution are supplied. At most 220 words.

## Rubric

Reject the general identification guarantee. An exact decoder T=d(M) means that no observed mediator value appears under both treatments. The usual front-door formula therefore requires conditional outcomes outside the observed support. Grade this verdict separately from the explanation. Exact decoding does not imply that M is merely a relabeling of T, that T determines M, or that M has no variation within treatment.

## Short justification

For the main verdict, let U be a fair bit, T=U and M=T. Outcome mechanisms Y=M+2U and Y=2M+U generate identical observations but have treatment effects 1 and 2. Both retain the stipulated graph.

To check the explanation, instead let M=(T,Z), with a fresh fair bit Z independent of U. T is still exactly decodable, but M varies within each treatment. Let Y=T+Z+U, with T read from M's first coordinate; every treatment effect still passes through M. At fixed T, observing M reveals Z and changes the conditional outcome distribution. Conditioning on M is therefore not equivalent to conditioning on T. This counterexample leaves the overlap objection intact.

## Observed error and limits

Every screened model rejected the main guarantee. In fresh high-effort confirmations, Fable explicitly confused decoding with the converse or with equivalent conditioning in two of three answers; Opus did so in one of three. Fable's remaining answer made a less precise information overclaim, excluded from these counts. GPT-6 Astra passed all three repeats. Gemini, Kimi and DeepSeek got the main inference right in their initial answers; Astra Pro passed its separate check. The counted errors concern the explanations accompanying correct verdicts.

# Testing, controls and interpretation

## How to reproduce

Paste each Question section alone into a fresh conversation, without the rubric, model quotations or neighboring examples. The API tests used the exact question text with requested reasoning effort high and max_tokens 16000; Astra Pro checks requested 32000. Each set of three repeats consisted of separate API calls, with no explicit random seed set. Codex smoke checks used GPT-6 Astra xhigh with an answer-only, no-tools prefix and are reported separately.

Requested API identifiers were anthropic/claude-fable-5.1, anthropic/claude-opus-5, google/gemini-3.1-pro-preview, moonshotai/kimi-k3, deepseek/deepseek-v4-pro, openai/gpt-6-astra and openai/gpt-6-astra-pro. These settings do not guarantee equal compute across providers. Empty, filtered, errored and length-truncated responses are excluded from error rates. All responses in the targeted confirmation runs completed substantively.

## What the controls show

DeepSeek accepted an explicit-support version of Example 1 in all three additional samples. Codex and all five other families correctly answered a version of Example 2 that explicitly asks whether two diagonal observations identify separate effects, counting completed answers. A separate three-cell additive design permits extrapolation. Models also recognized that a causally sufficient coarsening of a representation can support adjustment even when the full representation lacks overlap.

In a follow-up with fixed interior source rates, asking why the proposed repair suffices elicited a sufficient repair from Codex and all five API families. All six also recognized the zero-boundary additive exception.

These controls narrow the finding: a model can reject an invalid repair when asked about it directly, yet propose the same kind of repair in a broader answer. The task tests whether the model's own explanation or next step holds up.

## Selection and grading limits

The examples were selected after a broad search. Three repeats can show that an error recurs on a selected prompt, but cannot establish a stable failure rate. Main verdicts and explanations were graded separately. The stricter explanation criteria were written before the fresh two-item confirmation run; earlier observations were used to discover candidates. Boundary cases and underspecified suggestions are reported separately from clear errors.

The authoring agent performed all audits; there were no independent human raters. A human reviewer should check the short counterexamples and quoted failure claims. Many candidates were discarded because missing assumptions or ambiguous grading made their apparent difficulty unreliable. This work establishes neither novelty of the broad topic nor priority for the examples. The strongest tested model passed them.

## What this could measure

A benchmark that grades only the verdict would mark most of these responses correct while missing the unsupported advice. Asking models to recognize a stated flaw also misses errors they make when producing their own repairs. This construction tests both tasks, with small counterexamples and matched controls that make the errors easy to check. A held-out batch covering other inference methods, with grading criteria fixed in advance for both conclusions and repairs, would provide stronger validation.
