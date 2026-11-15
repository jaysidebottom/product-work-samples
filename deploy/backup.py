"""Consistent local backups; executed as the app user by systemd."""
import datetime
import os
from pathlib import Path
import sqlite3

root = Path('/var/lib/marketplace')
stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
destination = root / 'backups' / (stamp + '.sqlite3')
temporary = destination.with_suffix('.tmp')
os.umask(0o077)
with sqlite3.connect(f'file:{root}/marketplace.sqlite3?mode=rw', uri=True) as source:
    with sqlite3.connect(temporary) as target:
        source.backup(target)
        assert target.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        assert not target.execute('PRAGMA foreign_key_check').fetchall()
os.replace(temporary, destination)
for old in sorted((root / 'backups').glob('*.sqlite3'))[:-7]:
    old.unlink()
print('Verified backup:', destination.name)
