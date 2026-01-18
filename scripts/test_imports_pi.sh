#!/usr/bin/expect -f
# Script para probar imports en Raspberry Pi

set IP [lindex $argv 0]
set USER [lindex $argv 1]
set PASS [lindex $argv 2]
set timeout 15

puts "Probando imports en Pi..."
spawn ssh -o StrictHostKeyChecking=no $USER@$IP "cd ~/Pi_camara && cat > /tmp/test_import.py << 'PYEOF'
import sys
from pathlib import Path

project_root = Path('.').absolute()
sys.path.insert(0, str(project_root))
print('Project root:', project_root)
print('sys.path[0]:', sys.path[0])

try:
    from src.config_env import configure_system_paths
    configure_system_paths()
    print('config_env OK')
except Exception as e:
    print('config_env ERROR:', e)

try:
    from src.data.lerobot_dataset import EpisodeRecorder
    print('EpisodeRecorder import OK')
except Exception as e:
    print('EpisodeRecorder import ERROR:', e)

try:
    from src.main import main
    print('main import OK')
except Exception as e:
    print('main import ERROR:', e)
PYEOF
./venv/bin/python3 /tmp/test_import.py"

expect {
    "password:" {
        send "$PASS\r"
        exp_continue
    }
    eof
}
