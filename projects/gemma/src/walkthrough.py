"""Synthetic routing and progression walkthrough; no agents or services started."""
from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile

from routing import pick_best_agent
from progression import calculate_xp, apply_xp


def run_demo():
    with tempfile.TemporaryDirectory(prefix='agent-sample-') as tmp:
        root = Path(tmp)
        for name in ('skills', 'heartbeat', 'active'):
            (root / name).mkdir()
        registry = {'agents': {name: {'role': 'development', 'capabilities': ['api_design']}
                              for name in ('agent-a', 'agent-b')}}
        for name, score in [('agent-a', 70), ('agent-b', 60)]:
            (root / 'skills' / (name + '.json')).write_text(json.dumps({
                'skills': {'api_design': {'score': score}}}))
            (root / 'heartbeat' / (name + '.json')).write_text(json.dumps({
                'timestamp': datetime.now(timezone.utc).isoformat()}))
        kwargs = dict(needs=['api_design'], registry=registry, skills_dir=root / 'skills',
                      heartbeat_dir=root / 'heartbeat', active_dir=root / 'active', ipc_dir=root)
        print('Both available:', pick_best_agent(**kwargs))
        (root / 'active/agent-a.json').write_text(json.dumps({'task_id': 'synthetic-task'}))
        print('Agent A busy:', pick_best_agent(**kwargs))
        skill = {'score': 0, 'total_xp': 0}
        reward = calculate_xp(6, 'good', 'none', source='quest')
        apply_xp(skill, reward.xp_gained)
        print('One medium/good practice task:', reward.xp_gained, 'XP; score', skill['score'])
        print('Synthetic policy demonstration. XP is not independently measured mastery.')


if __name__ == '__main__':
    run_demo()
