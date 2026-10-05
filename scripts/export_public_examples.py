"""Export reviewed, answered harness runs (config/public-examples.json) as the public examples.

    uv run python scripts/export_public_examples.py   # reads $HARNESS_ROOT/artifacts/<run id>/run.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

from harness_public_gateway.app import project_run

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="config/public-examples.json")
    parser.add_argument("--artifacts", default=str(Path(os.environ.get("HARNESS_ROOT", "../rambodambo")).expanduser()
                                                   / "artifacts"), help="the harness runs (default $HARNESS_ROOT/artifacts)")
    parser.add_argument("--output", default="public_examples/examples.json")
    args = parser.parse_args()
    manifest = json.loads(Path(args.manifest).read_text())
    ids = manifest.get("run_ids")
    if not isinstance(ids, list) or any(
        not isinstance(x, str) or not re.fullmatch(r"r-[a-f0-9]+", x) for x in ids
    ):
        raise SystemExit("manifest run_ids must contain valid explicit run IDs")
    result = []
    for run_id in ids:
        path = Path(args.artifacts) / run_id / "run.json"
        run = json.loads(path.read_text())
        if run.get("status") != "answered" or run.get("chosenReading") is None:
            raise SystemExit(f"manifest run {run_id} is not answered")
        public = project_run(run)
        if public["state"] != "answered" or not public.get("evidence") or not public.get("triples"):
            raise SystemExit(f"manifest run {run_id} failed public provenance review")
        result.append(
            {
                "question": run["question"],
                "answer": public["answer"],
                "evidence": public["evidence"],
                "triples": public["triples"],
                "graph": public["graph"],
            }
        )
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
