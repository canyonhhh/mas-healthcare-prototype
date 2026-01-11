from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ArtifactSpec:
    name: str
    path: str
    rows: int
    schema: List[str]
    lineage: List[str] | None = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CheckResult:
    name: str
    status: str  # expected: "pass", "warn", "fail"
    details: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AgentResult:
    agent: str
    artifacts: List[ArtifactSpec] = field(default_factory=list)
    checks: List[CheckResult] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    notes: Optional[str] = None
    stop: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent": self.agent,
            "artifacts": [a.to_dict() for a in self.artifacts],
            "checks": [c.to_dict() for c in self.checks],
            "metrics": self.metrics,
            "notes": self.notes,
            "stop": self.stop,
        }


@dataclass
class PipelinePaths:
    artifacts_dir: Path
    registry_path: Path
    audit_log_path: Path

    @classmethod
    def default(cls, root: Path) -> "PipelinePaths":
        artifacts_dir = root / "artifacts"
        return cls(
            artifacts_dir=artifacts_dir,
            registry_path=artifacts_dir / "registry.json",
            audit_log_path=artifacts_dir / "audit.jsonl",
        )
