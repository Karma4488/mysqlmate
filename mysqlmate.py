#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_sqlmate(sqlmate_dir, args):
    sqlmate_path = Path(sqlmate_dir).expanduser().resolve()
    script = sqlmate_path / "sqlmate"

    if not script.exists():
        raise FileNotFoundError(f"Could not find sqlmate script at: {script}")

    cmd = [sys.executable, str(script)] + args
    result = subprocess.run(cmd, cwd=str(sqlmate_path), text=True, capture_output=True)
    return cmd, result

def main():
    parser = argparse.ArgumentParser(description="Automate SQLMate CLI queries")
    parser.add_argument("--sqlmate-dir", required=True, help="Path to the SQLMate repo")
    parser.add_argument("--dork", help="Run SQLMate with a dork query")
    parser.add_argument("--hash", dest="hash_value", help="Crack a single hash")
    parser.add_argument("--list", dest="hash_file", help="Crack hashes from a file")
    parser.add_argument("--dump", type=int, choices=range(1, 185), help="Dump dorks level 1-184")
    parser.add_argument("--admin", help="Scan for admin panels on a target URL")
    parser.add_argument("--type", dest="scan_type", choices=["PHP", "ASP", "HTML"], help="Use with --admin")
    parser.add_argument("--log-dir", default="logs", help="Directory for saved output")
    args = parser.parse_args()

    sqlmate_args = []
    if args.dork:
        sqlmate_args += ["--dork", args.dork]
    if args.hash_value:
        sqlmate_args += ["--hash", args.hash_value]
    if args.hash_file:
        sqlmate_args += ["--list", args.hash_file]
    if args.dump:
        sqlmate_args += ["--dump", str(args.dump)]
    if args.admin:
        sqlmate_args += ["--admin", args.admin]
    if args.scan_type:
        sqlmate_args += ["--type", args.scan_type]

    if not sqlmate_args:
        parser.error("Provide at least one SQLMate action argument.")

    cmd, result = run_sqlmate(args.sqlmate_dir, sqlmate_args)

    log_dir = Path(args.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"sqlmate_{stamp}.log"

    with open(log_file, "w", encoding="utf-8") as f:
        f.write("Command:\n" + " ".join(cmd) + "\n\n")
        f.write("STDOUT:\n" + result.stdout + "\n\n")
        f.write("STDERR:\n" + result.stderr + "\n")

    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    print(f"\nSaved log to: {log_file}")

    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
