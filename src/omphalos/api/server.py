from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles


@dataclass(frozen=True)
class RunRef:
    run_id: str
    run_dir: Path


def _runs_root() -> Path:
    root = os.environ.get("OMPHALOS_RUNS_ROOT", "artifacts/runs")
    return Path(root)


def _iter_runs(root: Path) -> Iterable[RunRef]:
    if not root.exists():
        return []
    out: List[RunRef] = []
    for p in sorted([x for x in root.iterdir() if x.is_dir()], key=lambda x: x.name):
        mf = p / "run_manifest.json"
        if mf.exists():
            out.append(RunRef(run_id=p.name, run_dir=p))
    return out


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"json_load_failed:{path.name}") from e


def _manifest_for(run: RunRef) -> Dict[str, Any]:
    mf = run.run_dir / "run_manifest.json"
    if not mf.exists():
        raise HTTPException(status_code=404, detail="manifest_not_found")
    obj = _load_json(mf)
    if not isinstance(obj, dict):
        raise HTTPException(status_code=500, detail="manifest_invalid")
    return obj


def _safe_relpath(p: str) -> str:
    rp = p.replace("\\", "/").lstrip("/")
    if rp == "" or rp.startswith("../") or "/../" in rp:
        raise HTTPException(status_code=400, detail="invalid_path")
    return rp


def _text_like(relpath: str) -> bool:
    lower = relpath.lower()
    return any(lower.endswith(s) for s in [".json", ".txt", ".csv", ".log", ".md", ".sql", ".yaml", ".yml"])


def _diff_text(a: str, b: str) -> str:
    import difflib
    al = a.splitlines(keepends=True)
    bl = b.splitlines(keepends=True)
    return "".join(difflib.unified_diff(al, bl, fromfile="left", tofile="right"))


def _file_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except Exception as e:
        raise HTTPException(status_code=500, detail="read_failed") from e


def _search_in_run(run: RunRef, q: str, limit: int) -> List[Dict[str, Any]]:
    qn = q.strip().lower()
    if qn == "":
        return []
    mf = _manifest_for(run)
    candidates: List[str] = []
    files = mf.get("artifacts", {}).get("files", [])
    if isinstance(files, list):
        for f in files:
            if isinstance(f, dict) and isinstance(f.get("path"), str):
                candidates.append(f["path"])
    hits: List[Dict[str, Any]] = []
    for rel in candidates:
        if len(hits) >= limit:
            break
        rlow = rel.lower()
        if qn in rlow:
            hits.append({"path": rel, "kind": "path"})
            continue
        if not _text_like(rel):
            continue
        p = run.run_dir / rel
        if not p.exists() or p.stat().st_size > 512 * 1024:
            continue
        try:
            t = p.read_text(encoding="utf-8", errors="ignore").lower()
        except Exception:
            continue
        if qn in t:
            hits.append({"path": rel, "kind": "content"})
    return hits


def _compare_runs(left: RunRef, right: RunRef) -> Dict[str, Any]:
    ml = _manifest_for(left)
    mr = _manifest_for(right)
    def index(m: Dict[str, Any]) -> Dict[str, str]:
        out: Dict[str, str] = {}
        files = m.get("artifacts", {}).get("files", [])
        if isinstance(files, list):
            for f in files:
                if isinstance(f, dict) and isinstance(f.get("path"), str) and isinstance(f.get("sha256"), str):
                    out[f["path"]] = f["sha256"]
        return out
    il = index(ml)
    ir = index(mr)
    left_only = sorted([p for p in il.keys() if p not in ir])
    right_only = sorted([p for p in ir.keys() if p not in il])
    changed = sorted([p for p in il.keys() if p in ir and il[p] != ir[p]])
    same = sorted([p for p in il.keys() if p in ir and il[p] == ir[p]])
    return {
        "left": left.run_id,
        "right": right.run_id,
        "summary": {"changed": len(changed), "added": len(right_only), "removed": len(left_only), "same": len(same)},
        "changed": changed[:5000],
        "added": right_only[:5000],
        "removed": left_only[:5000],
    }


def create_app() -> FastAPI:
    app = FastAPI(title="omphalOS API", version="0.1.0")
    ui_dir = Path(__file__).resolve().parents[3] / "ui" / "dist"
    if ui_dir.exists():
        app.mount("/", StaticFiles(directory=str(ui_dir), html=True), name="ui")

    @app.get("/api/health")
    def health() -> Dict[str, Any]:
        r = _runs_root()
        return {"status": "ok", "runs_root": str(r), "runs_found": len(list(_iter_runs(r)))}

    @app.get("/api/runs")
    def runs() -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        for run in _iter_runs(_runs_root()):
            mf = _manifest_for(run)
            out.append({"run_id": run.run_id, "created_at": mf.get("created_at"), "schema_version": mf.get("schema_version")})
        return out

    @app.get("/api/runs/{run_id}/manifest")
    def manifest(run_id: str) -> Dict[str, Any]:
        for run in _iter_runs(_runs_root()):
            if run.run_id == run_id:
                return _manifest_for(run)
        raise HTTPException(status_code=404, detail="run_not_found")

    @app.get("/api/runs/{run_id}/artifacts")
    def artifacts(run_id: str) -> Dict[str, Any]:
        for run in _iter_runs(_runs_root()):
            if run.run_id == run_id:
                mf = _manifest_for(run)
                files = mf.get("artifacts", {}).get("files", [])
                control = mf.get("artifacts", {}).get("control_files", [])
                return {"run_id": run_id, "files": files, "control_files": control}
        raise HTTPException(status_code=404, detail="run_not_found")

    @app.get("/api/runs/{run_id}/artifact")
    def artifact(run_id: str, path: str = Query(...), mode: str = Query("text")):
        rp = _safe_relpath(path)
        for run in _iter_runs(_runs_root()):
            if run.run_id == run_id:
                fp = run.run_dir / rp
                if not fp.exists():
                    raise HTTPException(status_code=404, detail="artifact_not_found")
                if mode == "download":
                    return FileResponse(str(fp))
                if mode == "json":
                    return JSONResponse(_load_json(fp))
                if mode == "text":
                    if fp.stat().st_size > 2 * 1024 * 1024:
                        raise HTTPException(status_code=413, detail="artifact_too_large")
                    return PlainTextResponse(fp.read_text(encoding="utf-8", errors="replace"))
                raise HTTPException(status_code=400, detail="invalid_mode")
        raise HTTPException(status_code=404, detail="run_not_found")

    @app.get("/api/runs/{run_id}/search")
    def search(run_id: str, q: str = Query(...), limit: int = Query(50, ge=1, le=500)):
        for run in _iter_runs(_runs_root()):
            if run.run_id == run_id:
                return {"run_id": run_id, "query": q, "hits": _search_in_run(run, q, limit)}
        raise HTTPException(status_code=404, detail="run_not_found")

    @app.get("/api/compare")
    def compare(left: str = Query(...), right: str = Query(...)) -> Dict[str, Any]:
        runs = {r.run_id: r for r in _iter_runs(_runs_root())}
        if left not in runs or right not in runs:
            raise HTTPException(status_code=404, detail="run_not_found")
        return _compare_runs(runs[left], runs[right])

    @app.get("/api/compare/diff")
    def compare_diff(left: str = Query(...), right: str = Query(...), path: str = Query(...)) -> Dict[str, Any]:
        runs = {r.run_id: r for r in _iter_runs(_runs_root())}
        if left not in runs or right not in runs:
            raise HTTPException(status_code=404, detail="run_not_found")
        rp = _safe_relpath(path)
        lp = runs[left].run_dir / rp
        rp2 = runs[right].run_dir / rp
        if not lp.exists() or not rp2.exists():
            raise HTTPException(status_code=404, detail="artifact_not_found")
        if lp.stat().st_size > 2 * 1024 * 1024 or rp2.stat().st_size > 2 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="artifact_too_large")
        lt = lp.read_text(encoding="utf-8", errors="replace")
        rt = rp2.read_text(encoding="utf-8", errors="replace")
        return {"path": rp, "diff": _diff_text(lt, rt)}
    return app


app = create_app()
