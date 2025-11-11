import os
from pathlib import Path
import json


def check_paths():
    paths = {
        "logs": Path("logs"),
        "cache": Path("cache"),
        "config": Path("ava_prime_v2_config.json"),
        "integration": Path("ava_prime_integration.py"),
    }
    results = {name: p.exists() for name, p in paths.items()}
    return results


def check_env():
    keys = [
        "OPENAI_API_KEY",
        "GITHUB_TOKEN",
        "NOTION_API_KEY",
    ]
    return {k: bool(os.environ.get(k)) for k in keys}


def write_health_report(results):
    Path("logs").mkdir(parents=True, exist_ok=True)
    report_path = Path("logs/health_check.json")
    report_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    return str(report_path)


def main():
    print("== Ava Prime v2.0 Health Check ==")
    paths_ok = check_paths()
    env_ok = check_env()
    overall = all(paths_ok.values()) and all(env_ok.values())

    results = {
        "paths": paths_ok,
        "env": env_ok,
        "overall_ok": overall,
    }

    out = write_health_report(results)
    print(f"Health report saved to: {out}")
    print(json.dumps(results, indent=2))
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())

