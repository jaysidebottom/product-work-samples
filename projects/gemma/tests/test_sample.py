"""Disposable routing tests and checks of historical progression limitations."""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from routing import pick_best_agent, build_retry_task
from progression import calculate_xp, xp_for_score, score_from_xp, apply_decay


class RoutingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ('skills', 'heartbeat', 'active'):
            (self.root / folder).mkdir()
        self.registry = {'agents': {name: {'role': 'development', 'capabilities': ['api']}
                                   for name in ('a', 'b')}}
        for name, score in [('a', 70), ('b', 60)]:
            (self.root / 'skills' / (name + '.json')).write_text(json.dumps({'skills': {'api': {'score': score}}}))
            (self.root / 'heartbeat' / (name + '.json')).write_text(json.dumps({'timestamp': datetime.now(timezone.utc).isoformat()}))

    def pick(self, **extra):
        return pick_best_agent(['api'], registry=self.registry, skills_dir=self.root / 'skills',
                               heartbeat_dir=self.root / 'heartbeat', active_dir=self.root / 'active',
                               ipc_dir=self.root, **extra)

    def test_busy_penalty_changes_choice(self):
        self.assertEqual(self.pick(), 'a')
        (self.root / 'active/a.json').write_text(json.dumps({'task_id': 'fixture'}))
        self.assertEqual(self.pick(), 'b')

    def test_offline_and_excluded_agents_are_not_selected(self):
        old = datetime.now(timezone.utc) - timedelta(seconds=300)
        (self.root / 'heartbeat/a.json').write_text(json.dumps({'timestamp': old.isoformat()}))
        self.assertEqual(self.pick(), 'b')
        self.assertIsNone(self.pick(exclude=['b']))

    def test_retry_preserves_original_and_excludes_failed_agent(self):
        original = {'task_id': 'fixture', 'to': 'a', 'description': 'Build an API'}
        retry = build_retry_task(original, 'a')
        self.assertEqual(retry['exclude_agents'], ['a'])
        self.assertNotIn('to', retry)
        self.assertEqual(original['to'], 'a')


class ProgressionTests(unittest.TestCase):
    def test_thresholds_and_roundtrip(self):
        self.assertEqual([xp_for_score(n) for n in (25, 50, 75)], [572, 3209, 15353])
        for n in range(101):
            self.assertEqual(score_from_xp(xp_for_score(n)), n)

    def test_reward_is_not_mastery(self):
        self.assertEqual(calculate_xp(6, 'good', 'none', source='quest').xp_gained, 3)
        self.assertEqual(calculate_xp(6, 'poor', 'none', is_failure=True, source='quest').xp_gained, 1)
        self.assertEqual(calculate_xp(6, 'good', 'full_escalation', source='quest').xp_gained, 1)

    def test_repeated_decay_reproduces_historical_limit(self):
        now = datetime(2026, 11, 15, tzinfo=timezone.utc)
        last_event = (now - timedelta(days=90)).isoformat()
        initial = xp_for_score(50)
        once = apply_decay(initial, last_event, now)
        twice = apply_decay(once, last_event, now)
        self.assertEqual([score_from_xp(v) for v in (initial, once, twice)], [50, 47, 45])


if __name__ == '__main__':
    unittest.main()
