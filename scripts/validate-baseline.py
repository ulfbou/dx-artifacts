from pathlib import Path
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parents[1]
m=json.loads((root/'tests/baseline/accepted-baseline.json').read_text())
data=(root/m['implementation_path']).read_bytes()
checks=[('accepted status',m['status']=='accepted'),('byte size',len(data)==m['implementation_size']),('sha256',hashlib.sha256(data).hexdigest()==m['implementation_sha256']),('no package extraction',not (root/'src/dx_artifacts').exists())]
for name,passed in checks: print(('PASS' if passed else 'FAIL')+': '+name)
if not all(x[1] for x in checks): sys.exit(1)
raise SystemExit(subprocess.run([sys.executable,'-m','pytest','-q'],cwd=root).returncode)
