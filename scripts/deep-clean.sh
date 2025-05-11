#!/bin/bash

echo "Starting deep clean..."

# Define project root relative to the script's location for robustness
# This assumes the script is in a 'scripts' subdirectory of the project root.
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "Operating in project root: $PROJECT_ROOT"

# Remove the .astro directory
if [ -d "$PROJECT_ROOT/.astro" ]; then
  echo "Removing .astro directory..."
  rm -rf "$PROJECT_ROOT/.astro"
  echo ".astro directory removed."
else
  echo ".astro directory not found."
fi

# Remove the node_modules directory
if [ -d "$PROJECT_ROOT/node_modules" ]; then
  echo "Removing node_modules directory..."
  rm -rf "$PROJECT_ROOT/node_modules"
  echo "node_modules directory removed."
else
  echo "node_modules directory not found."
fi

# Remove package-lock.json
if [ -f "$PROJECT_ROOT/package-lock.json" ]; then
  echo "Removing package-lock.json..."
  rm -f "$PROJECT_ROOT/package-lock.json"
  echo "package-lock.json removed."
else
  echo "package-lock.json not found."
fi

echo "Deep clean finished."
echo "Please run 'npm install' or 'make install' to reinstall dependencies."
