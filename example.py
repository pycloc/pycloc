import json
from pathlib import Path

from pycloc import CLOC

cwd = Path.cwd()

cloc = CLOC(
    workdir=cwd,
    timeout=30,
    by_file=True,
    json=True,
    exclude_dir=".idea,.venv,htmlcov,site",
)

output = cloc(".")
result = json.loads(output)
pretty = json.dumps(
    obj=result,
    indent=4,
)

print(pretty)
