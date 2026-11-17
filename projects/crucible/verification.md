# Crucible Verification

Checked November 16, 2026.

- The offline inspector verified all four prompt hashes, the baseline calibration identity, both nonempty diffs, and the unchanged crossover artifact.
- It checked baseline means against the extracted run values and summarized all 20 included candidate evaluation events across two benchmarks.
- Seven focused tests passed: artifact counts and identity, recorded means, tamper detection, section crossover, mutation validation, regression handling, and the historical zero-variance gate behavior.
- Historical function bodies were selected without algorithm changes; the inspector and tests are new portfolio utilities.

Commands from the repository root:

```sh
python3 -B projects/crucible/src/inspect_experiment.py
python3 -B -m unittest discover -s projects/crucible/tests -v
```

Python 3.9+ and the standard library are sufficient. No model calls, benchmark execution, or operational state changes occur.

These checks establish consistency of the included artifacts and summaries. They do not prove that the original experiments were controlled, that all attempts were logged, that observations are independent, or that the promotion method is statistically appropriate. The exact historical execution environment and cycle decision cannot be reconstructed from this package.

[Case study](README.md) · [Experiment limitations](experiment.md#limits-on-interpretation)
