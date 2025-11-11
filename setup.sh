#!/usr/bin/env bash
set -euo pipefail

echo "[Setup] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[Setup] Upgrading pip and installing requirements..."
pip install --upgrade pip
if [[ -f requirements.txt ]]; then
  pip install -r requirements.txt
else
  echo "[Warn] requirements.txt not found. Install dependencies manually if needed."
fi

echo "[Setup] Preparing .env file..."
if [[ ! -f .env ]]; then
  if [[ -f .env.example ]]; then
    cp .env.example .env
    echo "Created .env from template. Please update values."
  else
    touch .env
    echo "Created empty .env. Please add required values."
  fi
fi

echo "[Setup] Ensuring directories exist..."
mkdir -p logs cache

echo "[Setup] Done. Next steps:"
echo "  - Update .env with your API keys and settings"
echo "  - Run: python verify_setup.py"
echo "  - Then: python ava_prime_integration.py"

