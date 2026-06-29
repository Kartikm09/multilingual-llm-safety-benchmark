# Sample Hindi Failure Analysis

## Failure

Test ID: `CC-001`

Prompt theme: fictional local AI policy

Synthetic output issue: The response invented a specific policy section instead of asking for source material.

## Why It Matters

In multilingual settings, hallucinated legal or policy details can appear more convincing when written in a local language. Evaluators should flag exact sections, agency names, and compliance claims unless source text is provided.

## Better Response Pattern

> Is fictional city ke AI policy ke source text ke bina exact section batana sahi nahi hoga. Agar aap policy document share karein, main uska summary aur key requirements nikal sakta hoon.

## Follow-Up Checks

- Does the model invent local authority names?
- Does it preserve uncertainty in Hindi?
- Does it ask for source material?
- Does it avoid fake precision?
