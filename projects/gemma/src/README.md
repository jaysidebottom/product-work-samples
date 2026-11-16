# Gemma Code Selection

[Case study](../README.md)

The Python modules are selected historical function bodies with reduced imports and new module headers. No operational configuration, model runner, credential handling, or memory data is included.

| File | Origin and purpose |
|---|---|
| [capability_registry.py](capability_registry.py) | Historical registry loading, capability matching, and heartbeat checks; write/mutation helpers omitted |
| [routing.py](routing.py) | Historical agent selection and retry-task construction |
| [progression.py](progression.py) | Historical XP constants and reward, threshold, tier, and decay functions; aliases and snapshot helpers omitted |
| [walkthrough.py](walkthrough.py) | New portfolio utility using fictional agents and disposable data |

The historical function bodies are preserved, including known limitations. In particular, the registry's missing-score default is 50, the reward minimum grants XP even for full escalation, and repeated decay is not idempotent. Tests document those behaviors rather than silently correcting the historical implementation.

Generic `/ipc` defaults reflect the original container convention. The walkthrough and tests supply explicit temporary paths and never use a live state directory. Run the commands in the [case study](../README.md) to inspect the sample without services or accounts.
