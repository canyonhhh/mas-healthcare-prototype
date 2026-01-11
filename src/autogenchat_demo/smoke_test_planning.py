from __future__ import annotations

import asyncio
from pathlib import Path

from autogenchat_demo.pipeline import plan_and_run
from autogenchat_demo.planning.plan_schema import default_plan, validate_plan


async def _run() -> None:
    result = await plan_and_run("cohort report for 5 admissions")
    files = result.get("files", {})
    for path in files.values():
        if not Path(path).exists():
            raise SystemExit(f"Missing output file: {path}")

    broken_plan = {"pipeline": "unknown"}
    validated, errors = validate_plan(broken_plan)
    if not errors:
        raise SystemExit("validate_plan did not report errors for broken plan.")
    if validated != default_plan():
        raise SystemExit("validate_plan should fall back to default plan.")

    print("Smoke test passed.")


def main() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    main()
