"""Historical XP excerpts, including limitations discussed in the retrospective.
These functions are not a validated measure of capability. No file or network I/O.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

XP_GROWTH_RATE = 1.063


XP_BASE_PER_POINT = 10


_XP_TABLE = [round(XP_BASE_PER_POINT * (XP_GROWTH_RATE ** n - 1) / (XP_GROWTH_RATE - 1)) for n in range(101)]


COMPLEXITY_XP = {
    "trivial": 2,
    "low": 4,
    "medium": 6,
    "high": 9,
    "exceptional": 13,
}


QUALITY_MULTIPLIER = {
    "poor": 0.1,
    "acceptable": 0.5,
    "good": 1.0,
    "excellent": 1.3,
    "exceptional": 1.6,
}


SOURCE_MULTIPLIER = {
    "task": 1.0,       # Real work — full credit
    "chat": 0.75,      # Hands-on chat work — slightly reduced
    "quest": 0.5,      # Training quests — half credit
    "breeding": 0.25,  # Synthetic benchmarks — lowest signal
}


HELP_PENALTY = {
    "none": 1.0,
    "minor_clarification": 0.85,
    "paired": 0.7,
    "partial_escalation": 0.5,
    "full_escalation": 0.0,
}


TIER_THRESHOLDS = {0: "novice", 25: "competent", 50: "proficient", 75: "expert"}


@dataclass
class XPResult:
    """Result of an XP calculation with full breakdown."""
    xp_gained: int
    base_xp: int
    quality_mult: float
    help_mult: float
    source_mult: float
    is_failure: bool
    breakdown: str


def xp_for_score(score: int) -> int:
    """Cumulative XP required to reach a given score (0-100).

    Uses pre-computed table for O(1) lookup.
    """
    if score <= 0:
        return 0
    if score > 100:
        score = 100
    return _XP_TABLE[score]


def score_from_xp(total_xp: int) -> int:
    """Derive score (0-100) from cumulative XP total.

    Binary search on the threshold table.
    """
    if total_xp <= 0:
        return 0
    # Binary search: find highest score where xp_for_score(score) <= total_xp
    lo, hi = 0, 100
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if _XP_TABLE[mid] <= total_xp:
            lo = mid
        else:
            hi = mid - 1
    return lo


def get_tier(score: int) -> str:
    """Get the tier name for a given score."""
    tier = "novice"
    for threshold, name in sorted(TIER_THRESHOLDS.items()):
        if score >= threshold:
            tier = name
    return tier


def get_quest_tier(score: int) -> int:
    """Get the quest difficulty tier for a given score (1-10).

    Tier 1 = L0-9, Tier 2 = L10-19, ..., Tier 10 = L90-99.
    """
    return min(10, (score // 10) + 1)


def xp_to_next_tier(score: int) -> int:
    """Calculate score points needed to reach the next tier."""
    thresholds = sorted(TIER_THRESHOLDS.keys())
    for t in thresholds:
        if score < t:
            return t - score
    return 0  # already at max tier


def calculate_xp(
    base_xp: int,
    quality: str,
    help_level: str,
    current_score: int = 0,
    is_failure: bool = False,
    source: str = "task",
) -> XPResult:
    """Calculate raw XP gained from a task.

    Returns raw XP to add to total_xp pool. The exponential threshold curve
    handles diminishing returns — no diminishing factor in the formula itself.

    Args:
        base_xp: Base XP from complexity (use COMPLEXITY_XP values)
        quality: Quality rating key
        help_level: Help level key
        current_score: Agent's current score (unused in v3, kept for API compat)
        is_failure: Whether the task failed
        source: XP source for multiplier ("task", "chat", "quest", "breeding", "raid")

    Returns:
        XPResult with calculated raw XP and breakdown
    """
    s_mult = SOURCE_MULTIPLIER.get(source, 1.0)

    if is_failure:
        xp = max(1, round(base_xp * 0.15 * s_mult))
        return XPResult(
            xp_gained=xp,
            base_xp=base_xp,
            quality_mult=0.15,
            help_mult=1.0,
            source_mult=s_mult,
            is_failure=True,
            breakdown=f"Failure: max(1, {base_xp} * 0.15 * {s_mult}) = {xp}",
        )

    q_mult = QUALITY_MULTIPLIER.get(quality, 1.0)
    h_mult = HELP_PENALTY.get(help_level, 1.0)

    raw = base_xp * q_mult * h_mult * s_mult
    xp = max(1, round(raw))

    return XPResult(
        xp_gained=xp,
        base_xp=base_xp,
        quality_mult=q_mult,
        help_mult=h_mult,
        source_mult=s_mult,
        is_failure=False,
        breakdown=f"{base_xp} * {q_mult} (quality) * {h_mult} (help) * {s_mult} ({source}) = {xp}",
    )


def apply_xp(skill: dict, xp_gained: int) -> tuple[int, int, int]:
    """Apply raw XP to a skill entry, updating total_xp and derived score.

    Handles the total_xp → score derivation and tier/xp_to_next updates.
    Returns (old_score, new_score, new_total_xp).

    Args:
        skill: Mutable skill dict (modified in-place)
        xp_gained: Raw XP to add to total_xp pool
    """
    old_total = skill.get("total_xp", 0)
    old_score = skill.get("score", 0)

    # Migrate: if total_xp is missing/zero but score > 0, estimate from old system
    if old_total == 0 and old_score > 0:
        old_total = xp_for_score(old_score)
        skill["total_xp"] = old_total

    new_total = old_total + xp_gained
    new_score = score_from_xp(new_total)

    # Cap at 100
    if new_score > 100:
        new_score = 100
        new_total = _XP_TABLE[100]

    skill["total_xp"] = new_total
    skill["score"] = new_score
    skill["tier"] = get_tier(new_score)
    skill["xp_to_next_tier"] = xp_to_next_tier(new_score)

    return old_score, new_score, new_total


def compute_agent_level(skills: dict) -> int:
    """Compute composite agent level as the floored average of all skill scores.

    Args:
        skills: Dict of skill_key -> skill entry (each with 'score' field)

    Returns:
        Integer level 0-100 (average of all skill scores, floored)
    """
    if not skills:
        return 0
    scores = [s.get("score", 0) for s in skills.values()]
    return int(sum(scores) / len(scores))


def apply_decay(total_xp: int, last_xp_event: Optional[str], now: Optional[datetime] = None) -> int:
    """Apply time-based decay to cumulative XP.

    Decay operates on total_xp (not score). The exponential threshold curve
    means the same XP loss has less score impact at higher levels.

    Rules:
        - 30-day grace period after last XP event
        - After grace: lose XP equivalent to ~1 score point per 30 idle days
          (at the agent's current level)
        - Floor: XP for previous tier threshold - 10 (minimum 0)

    Args:
        total_xp: Current cumulative XP
        last_xp_event: ISO timestamp of last XP event, or None
        now: Current time (defaults to UTC now)

    Returns:
        New total_xp after decay
    """
    if not last_xp_event or total_xp <= 0:
        return total_xp

    if now is None:
        now = datetime.now(timezone.utc)

    try:
        last_dt = datetime.fromisoformat(last_xp_event.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return total_xp

    idle_days = (now - last_dt).days
    if idle_days <= 30:
        return total_xp

    # Calculate decay: lose XP for ~1 score point per 30 days past grace
    decay_periods = (idle_days - 30) // 30
    if decay_periods <= 0:
        return total_xp

    current_score = score_from_xp(total_xp)
    # XP cost of one point at current level
    if current_score > 0:
        xp_per_point = _XP_TABLE[current_score] - _XP_TABLE[current_score - 1]
    else:
        xp_per_point = XP_BASE_PER_POINT

    xp_loss = decay_periods * xp_per_point

    # Find floor: XP for previous tier threshold - 10
    thresholds = sorted(TIER_THRESHOLDS.keys(), reverse=True)
    floor_score = 0
    for t in thresholds:
        if current_score >= t and t > 0:
            floor_score = max(0, t - 10)
            break

    floor_xp = xp_for_score(floor_score)
    new_total = max(floor_xp, total_xp - xp_loss)
    return new_total
