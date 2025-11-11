import argparse
import json
from pathlib import Path


FEATURES = [
    "secure_code_review",
    "morning_briefing",
    "sync_daemon",
]


def parse_args():
    p = argparse.ArgumentParser(description="Deploy Ava Prime v2.0 features")
    p.add_argument(
        "--environment",
        choices=["development", "staging", "production"],
        default="development",
        help="Target environment",
    )
    p.add_argument(
        "--enable-features",
        default="all",
        help="Comma-separated features to enable or 'all'",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without persisting state",
    )
    return p.parse_args()


def main():
    args = parse_args()
    if args.enable_features == "all":
        selected = FEATURES
    else:
        selected = [f.strip() for f in args.enable_features.split(",") if f.strip()]

    print(f"Deploying to: {args.environment}")
    print(f"Enabling features: {selected}")

    state = {
        "environment": args.environment,
        "enabled_features": selected,
    }

    if args.dry_run:
        print("[DRY RUN] Deployment plan:")
        print(json.dumps(state, indent=2))
        return 0

    Path("deploy_state.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
    print("Deployment state written to deploy_state.json")
    print("Next: run 'python ava_prime_integration.py' in the target environment.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

