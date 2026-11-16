"""Historical Gemma routing excerpts. Use explicit disposable paths in examples."""
from __future__ import annotations
import json
from pathlib import Path
from capability_registry import load_registry, get_capable_agents, get_online_agents

def pick_best_agent(
    needs: list[str],
    registry: dict | None = None,
    skills_dir: str | Path = "/ipc/skills",
    heartbeat_dir: str | Path = "/ipc/heartbeat",
    active_dir: str | Path = "/ipc/active",
    ipc_dir: str | Path = "/ipc",
    exclude: list[str] | None = None,
) -> str | None:
    """Pick the best agent for a task based on capabilities, skills, and availability.

    1. Filter to agents whose capabilities >= needs
    2. Filter out offline agents (heartbeat > 120s stale)
    3. Filter out agents in exclude list
    4. Score: average skill score across needs, penalize agents with active tasks (-20)
    5. Return highest scorer, or None

    Args:
        needs: list of capability keys the task requires
        registry: pre-loaded registry dict (loads from disk if None)
        skills_dir: path to /ipc/skills/ directory
        heartbeat_dir: path to /ipc/heartbeat/ directory
        active_dir: path to /ipc/active/ directory
        ipc_dir: path to /ipc/ directory
        exclude: agent names to exclude

    Returns:
        Agent name string, or None if no suitable agent found.
    """
    if registry is None:
        registry = load_registry(ipc_dir)

    exclude = set(exclude or [])

    # Load skills data for scoring
    skills_dir = Path(skills_dir)
    skills_data = {}
    if skills_dir.exists():
        for f in skills_dir.glob("*.json"):
            agent_name = f.stem
            try:
                skills_data[agent_name] = json.loads(f.read_text())
            except (json.JSONDecodeError, OSError):
                continue

    # Get capable agents with scores
    capable = get_capable_agents(registry, needs, skills_data)
    if not capable:
        return None

    # Filter online
    online = get_online_agents(registry, heartbeat_dir)

    # Filter and score
    active_dir = Path(active_dir)
    scored = []

    for agent_name, avg_score in capable:
        if agent_name in exclude:
            continue
        if agent_name not in online:
            continue
        # Director never receives tasks
        if registry.get("agents", {}).get(agent_name, {}).get("role") == "director":
            continue

        # Penalize agents with active tasks
        penalty = 0
        active_file = active_dir / f"{agent_name}.json"
        if active_file.exists():
            try:
                active = json.loads(active_file.read_text())
                if active.get("task_id"):
                    penalty = 20
            except (json.JSONDecodeError, OSError):
                pass

        scored.append((agent_name, avg_score - penalty))

    if not scored:
        return None

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0][0]


def build_retry_task(original_task: dict, failed_agent: str) -> dict:
    """Build a retry task excluding the failed agent.

    Copies the original task, adds the failed agent to exclude_agents,
    increments retry_count, and generates a new task_id.
    """
    retry = dict(original_task)
    retry["task_id"] = f"{original_task.get('task_id', 'task')}-retry-{retry.get('retry_count', 0) + 1}"

    # Track excluded agents
    excluded = list(retry.get("exclude_agents", []))
    if failed_agent not in excluded:
        excluded.append(failed_agent)
    retry["exclude_agents"] = excluded

    # Increment retry count
    retry["retry_count"] = retry.get("retry_count", 0) + 1

    # Clear routing metadata for re-routing
    retry.pop("routed_by", None)
    retry.pop("routing_score", None)
    retry.pop("to", None)

    return retry
