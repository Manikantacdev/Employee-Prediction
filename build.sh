#!/usr/bin/env bash
# Render build script

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install dependencies with pre-built wheels (no source compilation)
pip install --no-cache-dir --prefer-binary -r requirements.txt

echo "Build completed successfully!"
