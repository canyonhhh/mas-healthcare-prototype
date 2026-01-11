from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from .contracts import AgentResult, ArtifactSpec, PipelinePaths


def ensure_paths(paths: PipelinePaths) -> None:
    paths.artifacts_dir.mkdir(parents=True, exist_ok=True)
    if not paths.registry_path.exists():
        paths.registry_path.write_text("{}", encoding="utf-8")
    if not paths.audit_log_path.exists():
        paths.audit_log_path.touch()


def load_registry(paths: PipelinePaths) -> Dict[str, Dict]:
    ensure_paths(paths)
    text = paths.registry_path.read_text(encoding="utf-8")
    return json.loads(text or "{}")


def save_registry(paths: PipelinePaths, registry: Dict[str, Dict]) -> None:
    ensure_paths(paths)
    paths.registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")


def register_artifact(paths: PipelinePaths, artifact: ArtifactSpec) -> None:
    registry = load_registry(paths)
    registry[artifact.name] = artifact.to_dict()
    save_registry(paths, registry)


def append_audit(paths: PipelinePaths, result: AgentResult) -> None:
    ensure_paths(paths)
    with paths.audit_log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(result.to_dict()) + "\n")
