import json
import os
import sys
from pathlib import Path


def check_python_version():
    major, minor = sys.version_info[:2]
    return (major, minor) >= (3, 8)


def check_files_exist(files):
    missing = [f for f in files if not Path(f).exists()]
    return missing


def load_config(path="ava_prime_v2_config.json"):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as e:
        return {"error": str(e)}


def check_env_vars(required):
    missing = [k for k in required if not os.environ.get(k)]
    return missing


def test_audit_log_write():
    try:
        logs_dir = Path(os.environ.get("AUDIT_LOG_DIR", "logs"))
        logs_dir.mkdir(parents=True, exist_ok=True)
        test_file = logs_dir / "verify_setup.log"
        test_file.write_text("verify_setup: audit log write OK\n", encoding="utf-8")
        return True, str(test_file)
    except Exception as e:
        return False, str(e)


def main():
    print("== Ava Prime v2.0 Setup Verification ==")

    # Python version
    ok_python = check_python_version()
    print(f"Python >= 3.8: {'OK' if ok_python else 'FAIL'} (detected {sys.version.split()[0]})")

    # Files
    required_files = [
        "ava_prime_integration.py",
        "ava_prime_v2_config.json",
        "integration_demo.py",
        "requirements.txt",
    ]
    missing_files = check_files_exist(required_files)
    if missing_files:
        print(f"Missing files: {missing_files}")
    else:
        print("Core files present: OK")

    # Config
    cfg = load_config()
    if "error" in cfg:
        print(f"Config load error: {cfg['error']}")
    else:
        print("Config load: OK")

    # Environment
    required_env = [
        "OPENAI_API_KEY",
        "GITHUB_TOKEN",
        "NOTION_API_KEY",
    ]
    missing_env = check_env_vars(required_env)
    if missing_env:
        print(f"Missing environment variables: {missing_env}")
    else:
        print("Essential environment variables: OK")

    # Audit log write
    ok_write, info = test_audit_log_write()
    print(f"Audit log write: {'OK' if ok_write else 'FAIL'} ({info})")

    # Summary
    all_ok = ok_python and not missing_files and "error" not in cfg and ok_write
    print("\nSummary:")
    print(f"  Python: {'OK' if ok_python else 'FAIL'}")
    print(f"  Files: {'OK' if not missing_files else 'FAIL'}")
    print(f"  Config: {'OK' if 'error' not in cfg else 'FAIL'}")
    print(f"  Audit Log: {'OK' if ok_write else 'FAIL'}")
    print("\nNext:")
    print("  - Fill in .env values if missing")
    print("  - Run: python ava_prime_integration.py")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())

