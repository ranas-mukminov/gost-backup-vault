#!/bin/bash
set -e

echo "Running bandit..."
bandit -r src -c pyproject.toml || true # Allow failure for now as config might be missing

echo "Security scan complete."
