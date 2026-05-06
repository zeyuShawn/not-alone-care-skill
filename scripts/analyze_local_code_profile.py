from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

from _local_data import CAREER_PROFILE_DEFAULT, ensure_data_dir, now_iso, read_json, truthy, write_json

SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "build",
    "target",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".mypy_cache",
    ".pytest_cache",
    ".idea",
    ".vscode",
}

SKIP_FILE_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".zip",
    ".tar",
    ".gz",
    ".7z",
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".xlsx",
    ".xls",
    ".sqlite",
    ".db",
    ".pkl",
    ".onnx",
}

SKIP_FILE_NAMES = {
    ".env",
    ".env.local",
    ".env.development",
    ".env.production",
    "id_rsa",
    "id_ed25519",
    "known_hosts",
}

EXT_LANG_MAP = {
    ".py": "Python",
    ".ipynb": "Jupyter",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".kt": "Kotlin",
    ".go": "Go",
    ".rs": "Rust",
    ".c": "C",
    ".cc": "C++",
    ".cpp": "C++",
    ".h": "C/C++",
    ".hpp": "C++",
    ".cs": "C#",
    ".php": "PHP",
    ".rb": "Ruby",
    ".swift": "Swift",
    ".r": "R",
    ".jl": "Julia",
    ".scala": "Scala",
    ".sh": "Shell",
    ".ps1": "PowerShell",
    ".sql": "SQL",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "CSS",
    ".vue": "Vue",
    ".svelte": "Svelte",
    ".md": "Markdown",
}


FRAMEWORK_INDICATORS = {
    "React": ["react", "next"],
    "Vue": ["vue", "nuxt"],
    "Angular": ["@angular/core"],
    "Node.js": ["express", "koa", "fastify", "nestjs"],
    "Django": ["django"],
    "Flask": ["flask"],
    "FastAPI": ["fastapi"],
    "Pandas": ["pandas"],
    "PyTorch": ["torch"],
    "TensorFlow": ["tensorflow"],
    "Spring": ["spring-boot", "springframework"],
    "Go": ["gin-gonic", "echo", "fiber"],
}


TOOLS_HINTS = {
    "pytest": "Testing",
    "unittest": "Testing",
    "jest": "Testing",
    "vitest": "Testing",
    "github/workflows": "CI",
    "dockerfile": "Container",
    "docker-compose": "Container",
    "requirements.txt": "Package Management",
    "pyproject.toml": "Package Management",
    "package.json": "Package Management",
    "go.mod": "Package Management",
    "pom.xml": "Package Management",
    "makefile": "Build Automation",
    "terraform": "Infra as Code",
    "alembic": "Database Migration",
    "prisma": "Database Modeling",
}


def parse_project_arg(value: str) -> Tuple[str, Path]:
    if "=" in value:
        alias, raw_path = value.split("=", 1)
        alias = alias.strip()
        path = Path(raw_path.strip()).expanduser().resolve()
        if not alias:
            alias = path.name or "project"
        return alias, path
    path = Path(value).expanduser().resolve()
    return path.name or "project", path


def should_skip_file(path: Path) -> bool:
    if path.name in SKIP_FILE_NAMES:
        return True
    if path.suffix.lower() in SKIP_FILE_SUFFIXES:
        return True
    return False


def infer_project_types(files: Iterable[Path], has_readme: bool) -> List[str]:
    file_names = {p.name.lower() for p in files}
    suffixes = {p.suffix.lower() for p in files}
    project_types: List[str] = []

    if ".ipynb" in suffixes or "pandas" in file_names:
        project_types.append("data_analysis")
    if {"app.py", "manage.py", "main.py"}.intersection(file_names) or ".py" in suffixes:
        project_types.append("script_or_backend")
    if {"package.json", "next.config.js", "vite.config.ts", "vite.config.js"}.intersection(file_names):
        project_types.append("web_app")
    if {"playwright.config.ts", "selenium", "puppeteer"}.intersection(file_names):
        project_types.append("automation")
    if "readme.md" in file_names and has_readme:
        project_types.append("documented_project")

    if not project_types:
        project_types.append("general_software")
    return sorted(set(project_types))


def detect_frameworks(root: Path) -> List[str]:
    detected: List[str] = []

    package_json = root / "package.json"
    if package_json.exists():
        try:
            pkg = json.loads(package_json.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            pkg = {}
        deps = {}
        deps.update(pkg.get("dependencies", {}) if isinstance(pkg.get("dependencies"), dict) else {})
        deps.update(pkg.get("devDependencies", {}) if isinstance(pkg.get("devDependencies"), dict) else {})
        dep_names = {name.lower() for name in deps.keys()}
        for fw, keys in FRAMEWORK_INDICATORS.items():
            if any(k.lower() in dep_names for k in keys):
                detected.append(fw)

    requirements = root / "requirements.txt"
    if requirements.exists():
        lines = requirements.read_text(encoding="utf-8-sig", errors="ignore").lower().splitlines()
        for fw, keys in FRAMEWORK_INDICATORS.items():
            if any(any(key.lower() in line for key in keys) for line in lines):
                detected.append(fw)

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text(encoding="utf-8-sig", errors="ignore").lower()
        for fw, keys in FRAMEWORK_INDICATORS.items():
            if any(key.lower() in text for key in keys):
                detected.append(fw)

    go_mod = root / "go.mod"
    if go_mod.exists():
        text = go_mod.read_text(encoding="utf-8-sig", errors="ignore").lower()
        if "module" in text:
            detected.append("Go Modules")

    pom = root / "pom.xml"
    if pom.exists():
        text = pom.read_text(encoding="utf-8-sig", errors="ignore").lower()
        if "spring" in text:
            detected.append("Spring")

    return sorted(set(detected))


def detect_tools(root: Path, files: Iterable[Path]) -> List[str]:
    tools: List[str] = []
    lower_paths = [str(p.relative_to(root)).replace("\\", "/").lower() for p in files]
    lower_names = [p.name.lower() for p in files]

    for key, label in TOOLS_HINTS.items():
        if any(key in path for path in lower_paths) or any(key in name for name in lower_names):
            tools.append(label)

    if (root / ".github" / "workflows").exists():
        tools.append("CI")

    return sorted(set(tools))


def scan_project(alias: str, root: Path, max_files: int, include_path: bool = False) -> Dict[str, Any]:
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Project path not found or not directory: {root}")

    files: List[Path] = []
    latest_mtime = 0.0

    for current_raw, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        current = Path(current_raw)
        for name in filenames:
            path = current / name
            if should_skip_file(path):
                continue
            try:
                stat = path.stat()
            except OSError:
                continue
            latest_mtime = max(latest_mtime, stat.st_mtime)
            files.append(path)
            if len(files) >= max_files:
                break
        if len(files) >= max_files:
            break

    language_counter: Counter[str] = Counter()
    for file in files:
        lang = EXT_LANG_MAP.get(file.suffix.lower())
        if lang:
            language_counter[lang] += 1

    has_readme = any(f.name.lower().startswith("readme") for f in files)
    project_types = infer_project_types(files, has_readme)
    frameworks = detect_frameworks(root)
    tools = detect_tools(root, files)

    top_languages = [lang for lang, _ in language_counter.most_common(6)]
    mtime = datetime.fromtimestamp(latest_mtime).replace(microsecond=0).isoformat() if latest_mtime else ""

    evidence = {
        "alias": alias,
        "file_count_scanned": len(files),
        "top_languages": top_languages,
        "frameworks": frameworks,
        "project_types": project_types,
        "tools": tools,
        "has_readme": has_readme,
        "last_modified": mtime,
    }
    if include_path:
        evidence["path"] = str(root)
    return evidence


def merge_unique(items: Iterable[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for item in items:
        value = str(item).strip()
        if not value or value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze authorized local projects into career_profile.json")
    parser.add_argument("--data-dir", default=None)
    parser.add_argument("--consent", required=True, help="Must be true/yes to confirm analysis consent.")
    parser.add_argument("--project", action="append", required=True, help="project alias/path. Example: api=~/repo/api")
    parser.add_argument("--current-role", default="")
    parser.add_argument("--target-role", action="append", default=[])
    parser.add_argument("--location", default="")
    parser.add_argument("--salary-floor", default="")
    parser.add_argument("--remote-preference", default="")
    parser.add_argument("--energy-load-limit", default="")
    parser.add_argument("--avoid", action="append", default=[])
    parser.add_argument("--notes", default="")
    parser.add_argument("--max-files", type=int, default=4000)
    parser.add_argument("--include-path", action="store_true", help="Store absolute project paths in career_profile.json; off by default for privacy.")
    args = parser.parse_args()

    if not truthy(args.consent):
        raise SystemExit("Refusing to scan: --consent must be true.")

    root = ensure_data_dir(args.data_dir)
    profile_path = root / "career_profile.json"

    project_specs = [parse_project_arg(spec) for spec in args.project]

    project_evidence: List[Dict[str, Any]] = []
    sources: List[Dict[str, str]] = []
    all_skills: List[str] = []

    for alias, path in project_specs:
        evidence = scan_project(alias, path, args.max_files, include_path=args.include_path)
        project_evidence.append(evidence)
        sources.append(
            {
                "type": "local_code",
                "path_alias": alias,
                "scanned_at": now_iso(),
            }
        )
        all_skills.extend(evidence.get("top_languages", []))
        all_skills.extend(evidence.get("frameworks", []))
        all_skills.extend(evidence.get("tools", []))
        all_skills.extend(evidence.get("project_types", []))

    existing = read_json(profile_path, CAREER_PROFILE_DEFAULT)
    if not isinstance(existing, dict):
        existing = dict(CAREER_PROFILE_DEFAULT)

    constraints = dict(existing.get("constraints") or {})
    if args.location:
        constraints["location"] = args.location
    if args.salary_floor:
        constraints["salary_floor"] = args.salary_floor
    if args.remote_preference:
        constraints["remote_preference"] = args.remote_preference
    if args.energy_load_limit:
        constraints["energy_load_limit"] = args.energy_load_limit

    payload = {
        "version": 1,
        "updated_at": now_iso(),
        "consent": True,
        "sources": sources,
        "current_role": args.current_role or existing.get("current_role", ""),
        "target_roles": merge_unique(args.target_role or existing.get("target_roles", [])),
        "skills_evidenced": merge_unique(all_skills),
        "skills_to_verify": existing.get("skills_to_verify", []),
        "project_evidence": project_evidence,
        "constraints": {
            "location": constraints.get("location", ""),
            "salary_floor": constraints.get("salary_floor", ""),
            "remote_preference": constraints.get("remote_preference", ""),
            "energy_load_limit": constraints.get("energy_load_limit", ""),
        },
        "avoid": merge_unique(args.avoid or existing.get("avoid", [])),
        "notes_summary": args.notes or existing.get("notes_summary", ""),
    }

    write_json(profile_path, payload)
    print(
        json.dumps(
            {
                "status": "ok",
                "file": str(profile_path),
                "projects": [alias for alias, _ in project_specs],
                "skills_evidenced_count": len(payload["skills_evidenced"]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
