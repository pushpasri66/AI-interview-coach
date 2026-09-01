#!/usr/bin/env bash
# build.sh — Render.com build script for AI Interview Coach
# Runs once during each deployment before the app starts.
set -e  # Exit immediately on any error

echo "==> Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Running database migrations..."
flask db upgrade || echo "No migrations to run (db may not exist yet — tables created on first start)."

echo "==> Build complete."
