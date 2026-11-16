"""Offline verification and descriptive summaries of preserved evidence.

This portfolio utility was added for inspection. It does not execute agents,
recreate evaluation runs, or infer a historical promotion decision.
"""
from collections import defaultdict
import difflib
import hashlib
import json
from pathlib import Path
from statistics import mean


EVIDENCE = Path(__file__).resolve().parents[1] / 'evidence'


def load_verified_evidence(directory=EVIDENCE):
    data = json.loads((directory / 'experiment.json').read_text())
    baseline = data['baseline']
    entries = [baseline, *data['variants']]
    for entry in entries:
        actual = hashlib.sha256((directory / entry['prompt_file']).read_bytes()).hexdigest()
        if actual != entry['sha256']:
            raise ValueError('Prompt checksum mismatch: ' + entry['prompt_file'])
    if baseline['sha256'][:12] != baseline['recorded_prompt_hash']:
        raise ValueError('Baseline calibration hash does not match prompt')
    original = (directory / baseline['prompt_file']).read_text()
    for variant in data['variants']:
        prompt = (directory / variant['prompt_file']).read_text()
        diff = ''.join(difflib.unified_diff(original.splitlines(True), prompt.splitlines(True),
                      fromfile=baseline['prompt_file'], tofile=variant['prompt_file'], n=0))
        if variant['label'] == 'crossover':
            if diff or not data['artifact_check']['crossover_equals_baseline']:
                raise ValueError('Crossover identity finding no longer matches artifacts')
        elif diff != (directory / (variant['label'] + '.diff')).read_text():
            raise ValueError('Prompt diff mismatch: ' + variant['label'])
    return data


def summarize(data):
    rows = []
    for bid, baseline in data['baseline']['benchmarks'].items():
        runs = baseline['runs']
        acceptance = mean(r['acceptance_score'] for r in runs)
        fitness = mean(r['fitness'] for r in runs)
        if abs(acceptance - baseline['acceptance_score']) > 0.0001:
            raise ValueError('Baseline acceptance disagrees with recorded runs')
        if abs(fitness - baseline['fitness']) > 0.0001:
            raise ValueError('Baseline fitness disagrees with recorded runs')
        rows.append(('baseline', bid, len(runs), acceptance, fitness))
    grouped = defaultdict(list)
    labels = {v['metadata']['variant_id']: v['label'] for v in data['variants']}
    for event in data['recorded_evaluations']:
        label = labels[event['variant_id']]
        grouped[label, event['benchmark_id']].append(event)
    for (label, bid), runs in sorted(grouped.items()):
        rows.append((label, bid, len(runs), mean(r['acceptance'] for r in runs),
                     mean(r['fitness'] for r in runs)))
    return rows


if __name__ == '__main__':
    data = load_verified_evidence()
    print('Prompt hashes and diffs verified. Crossover prompt equals baseline.')
    print('Recorded observations; event counts do not establish independent trials.\n')
    print('Prompt | Benchmark | Records | Mean acceptance | Mean fitness')
    for label, bid, count, acceptance, fitness in summarize(data):
        print(f'{label} | {bid} | {count} | {acceptance:.5f} | {fitness:.5f}')
    print('\nNearby cycle record winner:', data['nearby_cycle_record']['winner'])
    print('Cycle association is inferred; no promotion decision is recomputed.')
