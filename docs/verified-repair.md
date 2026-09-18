# Verified repair scope

The starting source was `79510e5c8d1764fd80453b29463eda6a47cdc38c`. The bundled example commands completed,
but there was no automated assertion suite. Bounded synthetic input probes
exposed the defect addressed here.

Validate1–5 scores in both scoring commands and reject empty combined summary clearly.

New regression tests failed before the repair. After the change, `make verify`
passed 3 test methods, including independent result oracles and negative
command-line cases. Every original documented sample command was rerun. Test
counts are methods; parameterized inputs are not inflated into separate tests.

The tests use the standard library and synthetic fixtures. They do not claim
comprehensive schema validation, real model quality, external evidence quality,
or production readiness. CI repeats the discoverable verification command.
