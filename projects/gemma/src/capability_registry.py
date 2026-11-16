"""Historical Gemma registry excerpts; no services or credentials required."""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

def load_registry(ipc_dir: str | Path = "/ipc") -> dict:
    """Load the capability registry from ipc_dir/registry.json."""
    path = Path(ipc_dir) / "registry.json"
    if path.exists():
        try:
            return json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {"version": 0, "agents": {}, "apis": {}, "infrastructure": {}}


def get_capable_agents(
    registry: dict,
    needs: list[str],
    skills_data: dict | None = None,
) -> list[tuple[str, float]]:
    """Return agents whose capabilities are a superset of `needs`, sorted by average skill score.

    Args:
        registry: loaded registry dict
        needs: list of capability keys required
        skills_data: {agent_name: {skills: {skill_key: {score: int}}}} from /ipc/skills/

    Returns:
        List of (agent_name, avg_score) sorted by score descending.
    """
    needs_set = set(needs)
    results = []

    for agent_name, agent_info in registry.get("agents", {}).items():
        caps = set(agent_info.get("capabilities", []))
        if not needs_set.issubset(caps):
            continue

        # Score from skills_data if available
        avg_score = 50.0  # default
        if skills_data and agent_name in skills_data:
            agent_skills = skills_data[agent_name].get("skills", {})
            scores = [agent_skills[s]["score"] for s in needs if s in agent_skills]
            if scores:
                avg_score = sum(scores) / len(scores)

        results.append((agent_name, avg_score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results


def get_online_agents(
    registry: dict,
    heartbeat_dir: str | Path = "/ipc/heartbeat",
    max_age: int = 120,
) -> set[str]:
    """Filter registry agents by heartbeat freshness.

    Returns set of agent names with heartbeats newer than max_age seconds.
    """
    hb_dir = Path(heartbeat_dir)
    online = set()
    now = datetime.now(timezone.utc)

    for agent_name in registry.get("agents", {}):
        hb_file = hb_dir / f"{agent_name}.json"
        if not hb_file.exists():
            # Director (gemma) doesn't write heartbeats via ipc_runner
            if registry["agents"][agent_name].get("role") == "director":
                online.add(agent_name)
            continue
        try:
            hb = json.loads(hb_file.read_text())
            ts = datetime.fromisoformat(hb["timestamp"].replace("Z", "+00:00"))
            age = (now - ts).total_seconds()
            if age <= max_age:
                online.add(agent_name)
        except (json.JSONDecodeError, OSError, KeyError, ValueError):
            continue

    return online
