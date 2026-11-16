# Analyst model integration and deployment constraints

Product design notes supplementing the [Analyst Assistant PRD](prd.md). These are proposed integration requirements, not an implemented model connection.


The assistant connects to an approved model endpoint through a backend service; model credentials are never exposed to the browser. Before the pilot, engineering and security must confirm whether investigation data may leave the deployment boundary, which hosting environments are permitted, and the applicable retention and logging requirements. Only the authorized evidence needed for the task is sent to the model. Model outputs propose structured operations that application services validate before execution; the model receives no direct database credentials or independent authority to run queries or share findings.

Select the model against representative analyst tasks using correctness, evidence grounding, latency, cost, and deployment compatibility. A frontier model is an evaluation candidate, not an assumed requirement. If the endpoint is unavailable or times out, preserve the investigation and draft, show a clear failure state, and keep manual workflows available.

Pilot gate: Engineering and security approve the data boundary and endpoint; representative task tests verify grounded responses, validated tool calls, and outage fallback before analyst access.
