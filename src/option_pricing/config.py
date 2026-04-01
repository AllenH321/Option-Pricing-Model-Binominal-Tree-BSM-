from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    root: Path
    data: Path
    raw_data: Path
    processed_data: Path
    docs: Path
    notebooks: Path
    figures: Path
    tables: Path


def get_project_root(anchor: str = "src") -> Path:
    here = Path(__file__).resolve()
    for path in [here.parent, *here.parents]:
        if (path / anchor).exists():
            return path
    raise FileNotFoundError(f"Could not locate project root using anchor '{anchor}'.")


def get_project_paths(create: bool = True) -> ProjectPaths:
    root = get_project_root()
    paths = ProjectPaths(
        root=root,
        data=root / "data",
        raw_data=root / "data" / "raw",
        processed_data=root / "data" / "processed",
        docs=root / "docs",
        notebooks=root / "notebooks",
        figures=root / "docs" / "figures",
        tables=root / "docs" / "tables",
    )
    if create:
        for path in [
            paths.data,
            paths.raw_data,
            paths.processed_data,
            paths.docs,
            paths.notebooks,
            paths.figures,
            paths.tables,
        ]:
            path.mkdir(parents=True, exist_ok=True)
    return paths
