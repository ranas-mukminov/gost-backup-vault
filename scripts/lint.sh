#!/bin/bash
set -e

echo "Running ruff..."
ruff check src tests

echo "Running mypy..."
mypy src tests

echo "Linting complete."
