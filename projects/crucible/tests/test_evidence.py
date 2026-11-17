"""Offline artifact integrity and historical behavior checks."""
from pathlib import Path
import sys
import tempfile
import unittest
import shutil

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from evolution import SkillSection, crossover, validate_mutation, check_regression_floor, check_promotion
from inspect_experiment import EVIDENCE, load_verified_evidence, summarize


class EvidenceTests(unittest.TestCase):
    def test_archived_prompt_identity_and_all_observations(self):
        data = load_verified_evidence()
        self.assertEqual(len(data['recorded_evaluations']), 20)
        self.assertEqual(data['variants'][2]['sha256'], data['baseline']['sha256'])
        counts = {(label, bid): count for label, bid, count, _, _ in summarize(data)}
        self.assertEqual(sum(c for (label, _), c in counts.items() if label != 'baseline'), 20)

    def test_recorded_means(self):
        rows = {(label, bid): (count, a, f) for label, bid, count, a, f in summarize(load_verified_evidence())}
        count, acceptance, fitness = rows['exploit', 'breed-api-middleware-pipeline']
        self.assertEqual(count, 4)
        self.assertEqual(acceptance, 0.5)
        self.assertAlmostEqual(fitness, 0.5375)
        self.assertAlmostEqual(rows['contrast', 'breed-api-middleware-pipeline'][1], 0.375)
        self.assertAlmostEqual(rows['crossover', 'breed-api-middleware-pipeline'][1], 0.4375)

    def test_modified_prompt_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'evidence'
            shutil.copytree(EVIDENCE, target)
            (target / 'baseline-prompt.md').write_text('changed')
            with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                load_verified_evidence(target)

    def test_crossover_selects_sections_without_mutating_parents(self):
        a = [SkillSection('## Role', 2, 'A role'), SkillSection('## Work', 2, 'A work')]
        b = [SkillSection('## Role', 2, 'B role'), SkillSection('## Work', 2, 'B work')]
        self.assertEqual([s.content for s in crossover(a, b, [0])], ['A role', 'B work'])
        self.assertEqual([s.content for s in b], ['B role', 'B work'])

    def test_mutation_rejects_unchanged_or_corrupt_headings(self):
        original = '## Role\nWrite code.'
        self.assertEqual(validate_mutation(original, original), (False, 'unchanged'))
        self.assertEqual(validate_mutation(original, '## Other\nWrite code.'), (False, 'heading_changed'))
        self.assertEqual(validate_mutation(original, '## Role\nWrite and verify code.'), (True, 'valid'))

    def test_regression_gate_and_missing_coverage_limit(self):
        self.assertEqual(check_regression_floor({'api': [0.2]}, {'api': 0.8}), (True, ['api']))
        # Historical limitation: a missing result is skipped, not a coverage failure.
        self.assertEqual(check_regression_floor({}, {'api': 0.8}), (False, []))

    def test_historical_gate_zero_variance_limit(self):
        # Documents existing behavior, not the desired statistical decision.
        result = check_promotion([1.0, 1.0], [0.0, 0.0], 0.02)
        self.assertFalse(result['promoted'])
        self.assertEqual(result['p_value'], 1.0)


if __name__ == '__main__':
    unittest.main()
