#!/usr/bin/env bash
# Render build script - Force Python 3.11

set -e  # Exit on error

echo "==> Python version check..."
python --version

# Upgrade pip
echo "==> Upgrading pip..."
python -m pip install --upgrade pip

# Install dependencies with pre-built wheels only (no compilation)
echo "==> Installing dependencies..."
pip install --only-binary=:all: --no-cache-dir -r requirements.txt || \
pip install --prefer-binary --no-cache-dir -r requirements.txt

echo "==> Build completed successfully!"
