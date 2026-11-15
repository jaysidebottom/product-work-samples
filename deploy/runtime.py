"""Local operational configuration. No credentials or host identity in source."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PRIVATE=ROOT/'private'
CONFIG=json.loads((PRIVATE/'connection.json').read_text())
BASE=CONFIG['url'].rstrip('/')
if not BASE.startswith('https://'):raise ValueError('HTTPS is required')
SSH=['ssh','-i',str(PRIVATE/'marketplace.pem'),'-o','IdentitiesOnly=yes','-o','UserKnownHostsFile='+str(PRIVATE/'known_hosts'),'-o','HostKeyAlias='+CONFIG['host_key_alias'],'ubuntu@'+CONFIG['host']]
