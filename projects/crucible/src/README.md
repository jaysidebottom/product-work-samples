# Crucible Code Selection

[Case study](../README.md)

[evolution.py](evolution.py) contains historical function bodies selected from the archived pure-logic module: prompt hashing, section crossover, mutation validation, statistical promotion, and a regression floor. Imports and module framing are reduced for independent inspection. No model runner or external dependency is required.

[inspect_experiment.py](inspect_experiment.py) is a new portfolio utility. It verifies the included prompt files and diffs, checks baseline summary consistency, and calculates means from recorded evaluation events. It does not execute generated code or call a model.

## Historical limitations retained

- Mutation validation checks structure, repetition, identity, and size. Its old docstring describes additional type-aware checks that the preserved body does not implement; `mutation_type` is not used there.
- Crossover selects section indices mechanically. Correct indices and meaningful final changes are the caller's responsibility.
- The statistical helper returns a non-promoting result for zero-variance samples, even when their means differ. Its numerical approximation is not independently certified here.
- The regression helper skips missing benchmark results; it does not enforce evaluation coverage.
- These archived function bodies may postdate the featured March experiment. They illustrate implementation mechanisms, not the exact executable version or decision path of that cycle.

The [tests](../tests/test_evidence.py) exercise artifact integrity and selected historical behaviors, including limitations. They do not validate the original statistical methodology or prove agent improvement.
