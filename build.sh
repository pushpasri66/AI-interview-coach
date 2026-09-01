#!/usr/bin/env bash
# build.sh — Render.com build script for AI Interview Coach
# Runs once during each deployment before the app starts.
set -e  # Exit immediately on any error

echo "==> Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# NOTE: Do NOT run 'flask db upgrade' here.
# Render's database hostname is only reachable at RUNTIME, not during the build phase.
# Database tables are created automatically by db.create_all() on first app startup.

echo "==> Build complete."
