#!/usr/bin/env python3
import argparse, os, sys, json, fnmatch, datetime
from pathlib import Path

DEFAULT_IGNORES = {".git", "node_modules", "__pycache__", ".venv"}

def match_ignored(name, patterns):
    return any(fnmatch.fnmatch(name, p) for p in patterns)

def iter_entries(base: Path):
    try:
        with os.scandir(base) as it:
            for e in sorted(it, key=lambda x: (not x.is_dir(), x.name.lower())):
                yield e
    except PermissionError:
        return

def fmt_bytes(n: int, unit: str = "b") -> str:
    unit = unit.lower()
    factor = {
        "b": 1,
        "kb": 1024,
        "mb": 1024**2,
        "gb": 1024**3,
        "tb": 1024**4,
    }.get(unit, 1)
    value = n / factor
    if factor == 1:
        return f"{int(value):,}".replace(",", ".") + " B"
    else:
        return f"{value:,.2f}".replace(",", ".") + f" {unit.upper()}"

def build_tree(path: Path, max_depth: int, show_hidden: bool, ignore, only_dirs: bool, follow_symlinks: bool,
               with_size: bool, with_date: bool, exclude_files):
    def _walk(dirpath: Path, depth: int):
        if max_depth is not None and depth > max_depth:
            return
        entries = []
        for e in iter_entries(dirpath):
            name = e.name
            if not show_hidden and name.startswith("."):
                continue
            if match_ignored(name, ignore):
                continue
            is_dir = e.is_dir()
            if not is_dir and exclude_files and match_ignored(name, exclude_files):
                continue
            if only_dirs and not is_dir:
                continue

            size = None
            created = None
            if not is_dir:
                try:
                    st = e.stat(follow_symlinks=False)
                    if with_size:
                        size = st.st_size
                    if with_date:
                        created = datetime.datetime.fromtimestamp(st.st_ctime).strftime("%Y/%m/%d %H:%M:%S")
                except OSError:
                    size = None
                    created = None

            node = {"name": name, "type": "dir" if is_dir else "file"}
            if size is not None:
                node["size"] = size
            if created:
                node["created"] = created
            if is_dir and (max_depth is None or depth < max_depth):
                node["children"] = list(_walk(Path(e.path), depth + 1))
            entries.append(node)
        return entries
    root = {"name": path.name or str(path), "type": "dir", "children": list(_walk(path, 1))}
    return root

def render_text(node, prefix=""):
    lines = [node["name"] + ("/" if node.get("type") == "dir" else "")]
    def _render(children, pref):
        for i, ch in enumerate(children):
            last = i == len(children) - 1
            branch = "└── " if last else "├── "
            cont = "    " if last else "│   "
            label = ch["name"] + ("/" if ch.get("type") == "dir" else "")
            lines.append(pref + branch + label)

            # Riga info sotto ai file solo se ci sono size/date
            if ch.get("type") == "file" and (ch.get("size") is not None or ch.get("created")):
                parts = []
                if ch.get("size") is not None:
                    parts.append(fmt_bytes(ch["size"], size_unit))
                if ch.get("created"):
                    parts.append(f"Created at: {ch['created']}")
                if parts:  # parentesi solo se esistono parti
                    lines.append(pref + cont + "(" + " - ".join(parts) + ")")
                    if space_between:
                        lines.append(pref + cont)

            if ch.get("children"):
                _render(ch["children"], pref + cont)
    if node.get("children"):
        _render(node["children"], "")
    return "\n".join(lines)

def render_md(node):
    return "```text\n" + render_text(node) + "\n```"

def main():
    ap = argparse.ArgumentParser(
        prog="pydirtree",
        description="Stampa l’albero di directory e file con filtri, profondità, e formati multipli."
    )
    ap.add_argument("path", nargs="?", default=".", help="Cartella o disco di partenza (default: .)")
    ap.add_argument("-d", "--max-depth", type=int, default=None, help="Profondità massima (default: nessun limite)")
    ap.add_argument("--hidden", action="store_true", help="Includi file e cartelle nascoste")
    ap.add_argument("--ignore", nargs="*", default=[], help="Pattern da ignorare (glob). Es: *.log build dist")
    ap.add_argument("--only-dirs", action="store_true", help="Mostra solo directory")
    ap.add_argument("--format", choices=["text", "md", "json"], default="text", help="Formato output")
    ap.add_argument("-o", "--output", help="Scrivi su file invece che su stdout")
    ap.add_argument("--follow-symlinks", action="store_true", help="Segui i symlink a directory")
    ap.add_argument("--size", action="store_true", help="Mostra la dimensione dei file")
    ap.add_argument("--date", action="store_true", help="Mostra la data di creazione dei file")
    ap.add_argument("--no-default-ignores", action="store_true", help="Disabilita gli ignore di default")
    ap.add_argument("--exclude-files", nargs="*", default=[], help="Escludi file che combaciano con questi pattern (glob). Es: *.mp4 *.tmp")
    ap.add_argument("--size-unit", choices=["b","kb","mb","gb","tb"], default="b", help="Unità di misura per le dimensioni (default: B)")
    ap.add_argument("--space-between-lines", action="store_true", help="Aggiungi una riga vuota tra i file per maggiore leggibilità")

    args = ap.parse_args()

    global size_unit, space_between
    size_unit = args.size_unit
    space_between = args.space_between_lines

    p = Path(args.path).resolve()
    if not p.exists():
        print(f"Percorso non trovato: {p}", file=sys.stderr)
        sys.exit(2)
    ignore = set(args.ignore)
    if not args.no_default_ignores:
        ignore |= DEFAULT_IGNORES

    tree = build_tree(
        p, args.max_depth, args.hidden, ignore, args.only_dirs,
        args.follow_symlinks, args.size, args.date, args.exclude_files
    )

    if args.format == "json":
        out = json.dumps(tree, ensure_ascii=False, indent=2)
    elif args.format == "md":
        out = render_md(tree)
    else:
        out = render_text(tree)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
    else:
        print(out)

if __name__ == "__main__":
    main()
