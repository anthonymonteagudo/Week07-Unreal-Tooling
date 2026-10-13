---
updated: 2026-09-08
title: Validation and evidence
group: Topics
order: 38
status: Foundation
summary: A useful check compares observed data with an explicit requirement and explains the scope of its result.
---

## Start with an intended result

“Looks wrong” identifies a reason to investigate. A useful test adds the expected behavior, the observed difference, and the conditions under which the difference appears.

For a readable label, the viewing direction and coordinate orientation matter. For a bend, the required range of motion matters. For a texture setting, the intended data role matters. A rule is meaningful because it protects one of these requirements.

## Separate evidence from confidence

| Result | What it establishes |
|---|---|
| PASS | The available evidence satisfies this specific rule under the tested conditions. |
| FAIL | The observed state conflicts with the explicit rule. |
| REVIEW | The role, data, applicability, or evidence is insufficient for an automatic conclusion. |

These are suggested teaching/report labels. The real tool or exercise can define its own result vocabulary. Passing one rule does not prove complete artistic quality or correctness.

## Make the comparison useful

Reproduce the original symptom. State a hypothesis and an alternative. Keep relevant viewing conditions fixed, change a variable that tests the hypothesis, and repeat the original check. Record any additional changes required by the tool.

What observation would make you reject your explanation? If the answer is “nothing,” the proposed test probably cannot establish the cause.

## Design a small checker

Before writing code, prepare a known passing example, a known failure, and an incomplete-information example. Decide which data must be declared and which can be measured.

[Week 3's Python preview](week03.html) demonstrates this with in-memory texture records. A mature external example is the [Khronos glTF Validator](https://github.com/KhronosGroup/glTF-Validator): use it to study how validation produces specific findings, while recognizing that its format rules are not a course-wide UE asset policy.

## Leave a usable record

Capture the asset identity, rule, observed value, result, and reason. Link the relevant source and describe the verification limits. A precise unresolved diagnosis can save the next person substantial investigation time. See the [documentation guide](documentation.html).
