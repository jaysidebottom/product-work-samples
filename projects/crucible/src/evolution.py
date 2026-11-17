"""Historical Crucible pure-logic excerpts. No model execution.
The statistical gate is preserved for inspection, not endorsed as a valid
experimental design or used to reconstruct the historical cycle decision.
"""
from __future__ import annotations
import hashlib
import math
import re
import statistics
from dataclasses import dataclass, field

@dataclass
class SkillSection:
    heading: str          # "## Working Style"
    level: int            # 2
    content: str          # full text including heading
    skill_tags: list[str] = field(default_factory=list)  # inferred from content keywords
    section_type: str = "procedural"  # "declarative" or "procedural"


def compute_prompt_hash(content: str) -> str:
    """SHA-256 hash of prompt content, first 12 chars."""
    return hashlib.sha256(content.encode()).hexdigest()[:12]


def crossover(
    sections_a: list[SkillSection],
    sections_b: list[SkillSection],
    swap_indices: list[int],
) -> list[SkillSection]:
    """Take sections at swap_indices from A, rest from B.

    Both section lists must have the same length. Indices out of range are ignored.
    """
    result = []
    for i in range(len(sections_b)):
        if i in swap_indices and i < len(sections_a):
            result.append(sections_a[i])
        else:
            result.append(sections_b[i])
    return result


def validate_mutation(original: str, mutated: str, mutation_type: str = None) -> tuple[bool, str]:
    """Check mutation quality before accepting it (Nemotron-inspired repetition detection).

    Type-aware validation: reorder checks line-sequence change (not word overlap),
    rephrase uses a lenient 90% threshold, others use 95%.

    Returns (is_valid, reason). Invalid mutations should be resampled.
    """
    if not mutated or not mutated.strip():
        return False, "empty"

    # 0. Section integrity: must preserve original heading and not add extra headings.
    # Extract the original heading (first line starting with ##)
    original_lines = original.strip().split("\n")
    mutated_lines = mutated.strip().split("\n")
    original_heading = None
    for line in original_lines:
        if re.match(r'^#{2,6}\s+', line):
            original_heading = line.strip()
            break

    if original_heading:
        # Check mutated text starts with the original heading
        mutated_first_heading = None
        for line in mutated_lines:
            if re.match(r'^#{2,6}\s+', line):
                mutated_first_heading = line.strip()
                break
        if mutated_first_heading != original_heading:
            return False, "heading_changed"

        # Check no extra ## headings were introduced (would corrupt SKILL.md structure)
        heading_count = sum(1 for line in mutated_lines if re.match(r'^#{2,6}\s+', line))
        original_heading_count = sum(1 for line in original_lines if re.match(r'^#{2,6}\s+', line))
        if heading_count > original_heading_count:
            return False, "extra_headings"

    # 1. Repetition check: any 4-gram appearing 3+ times
    words = mutated.lower().split()
    if len(words) >= 4:
        ngrams = [tuple(words[i:i+4]) for i in range(len(words) - 3)]
        counts: dict[tuple, int] = {}
        for ng in ngrams:
            counts[ng] = counts.get(ng, 0) + 1
        if any(c >= 3 for c in counts.values()):
            return False, "repetitive_ngrams"

    # 2. Identity check: mutation must differ from original
    # (pattern_deletion should be shorter, others should have new content)
    if mutated.strip() == original.strip():
        return False, "unchanged"

    # 3. Length check: mutation shouldn't 8x the original
    # Length sanity check — only reject extreme bloat (15x+).
    # Functional mutations (pattern_injection, benchmark_directed) legitimately
    # add substantial content to short sections. The fitness function's token
    # efficiency metric penalizes bloat naturally during evaluation.
    if len(mutated) > len(original) * 15:
        return False, "too_long"

    return True, "valid"


def _student_t_cdf_upper(t: float, df: float) -> float:
    """Upper-tail CDF of Student's t-distribution (pure Python).

    P(T > t) for T ~ t(df). Uses regularized incomplete beta function.
    Accurate to ~5 decimal places for df >= 2.
    """
    if df <= 0:
        return 1.0

    x = df / (df + t * t)

    # Regularized incomplete beta function I_x(a, b) via continued fraction
    a = df / 2.0
    b = 0.5

    # Use the log-beta for normalization
    log_beta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)

    if x <= 0.0:
        ibeta = 0.0
    elif x >= 1.0:
        ibeta = 1.0
    else:
        # Lentz's continued fraction for I_x(a, b)
        front = math.exp(a * math.log(x) + b * math.log(1.0 - x) - log_beta) / a
        # Use series expansion for small x, CF otherwise
        if x < (a + 1.0) / (a + b + 2.0):
            ibeta = front * _betacf(x, a, b)
        else:
            ibeta = 1.0 - math.exp(
                b * math.log(1.0 - x) + a * math.log(x) - log_beta
            ) / b * _betacf(1.0 - x, b, a)

    # I_x(df/2, 1/2) gives P(T^2 < df*x/(1-x)) which relates to CDF
    p_two_tail = ibeta  # This is the two-sided area in the center
    p_upper = p_two_tail / 2.0 if t > 0 else 1.0 - p_two_tail / 2.0
    return max(0.0, min(1.0, p_upper))


def _betacf(x: float, a: float, b: float, max_iter: int = 200, eps: float = 1e-10) -> float:
    """Continued fraction for regularized incomplete beta function."""
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < 1e-30:
        d = 1e-30
    d = 1.0 / d
    h = d

    for m in range(1, max_iter + 1):
        m2 = 2 * m
        # Even step
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        h *= d * c

        # Odd step
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break

    return h


def welch_ttest_greater(a: list[float], b: list[float]) -> tuple[float, float]:
    """One-sided Welch's t-test: H1 = mean(a) > mean(b).

    Returns (t_statistic, p_value). Returns (0.0, 1.0) if insufficient data.
    """
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return 0.0, 1.0

    mean_a = sum(a) / na
    mean_b = sum(b) / nb
    var_a = sum((x - mean_a) ** 2 for x in a) / (na - 1)
    var_b = sum((x - mean_b) ** 2 for x in b) / (nb - 1)

    se = math.sqrt(var_a / na + var_b / nb)
    if se == 0:
        return 0.0, 1.0

    t = (mean_a - mean_b) / se

    # Welch-Satterthwaite degrees of freedom
    num = (var_a / na + var_b / nb) ** 2
    den = (var_a / na) ** 2 / (na - 1) + (var_b / nb) ** 2 / (nb - 1)
    df = num / den if den > 0 else 1.0

    p = _student_t_cdf_upper(t, df)
    return round(t, 4), round(p, 6)


def check_promotion(
    variant_scores: list[float],
    baseline_scores: list[float],
    threshold: float,
) -> dict:
    """Check if a variant should be promoted over baseline.

    Requires BOTH statistical significance (p < 0.05) AND
    mean improvement > threshold. Returns full stats for auditability.
    """
    t_stat, p_value = welch_ttest_greater(variant_scores, baseline_scores)

    mean_v = statistics.mean(variant_scores) if variant_scores else 0.0
    mean_b = statistics.mean(baseline_scores) if baseline_scores else 0.0
    delta = round(mean_v - mean_b, 4)

    promoted = p_value < 0.05 and delta > threshold

    return {
        "promoted": promoted,
        "delta": delta,
        "t_statistic": t_stat,
        "p_value": p_value,
        "threshold": threshold,
        "n_variant": len(variant_scores),
        "n_baseline": len(baseline_scores),
    }


REGRESSION_FLOOR_RATIO = 0.50  # variant fitness < 50% of baseline = destructive


def check_regression_floor(
    variant_per_benchmark: dict[str, list[float]],
    baseline_per_benchmark: dict[str, float],
    floor_ratio: float = REGRESSION_FLOOR_RATIO,
) -> tuple[bool, list[str]]:
    """Check if a variant has destructively regressed on any benchmark.

    Returns (is_destructive, list_of_regressed_benchmark_ids).
    A variant is destructive if its mean fitness on ANY benchmark
    is below floor_ratio * calibration_baseline_fitness for that benchmark.
    """
    regressed = []
    for bid, baseline_fitness in baseline_per_benchmark.items():
        if baseline_fitness <= 0:
            continue
        variant_scores = variant_per_benchmark.get(bid, [])
        if not variant_scores:
            continue
        variant_mean = statistics.mean(variant_scores)
        floor = baseline_fitness * floor_ratio
        if variant_mean < floor:
            regressed.append(bid)
    return (len(regressed) > 0, regressed)
