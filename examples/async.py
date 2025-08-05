import asyncio
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


async def main():
    output = await cloc(".", asynchronous=True)
    result = json.loads(output)
    pretty = json.dumps(result, indent=4)
    print(pretty)


if __name__ == "__main__":
    asyncio.run(main())
