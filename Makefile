# Use bash for shell commands
SHELL := /bin/bash

# Default target
.DEFAULT_GOAL := launch

# Launch the Streamlit app
launch:
	@echo "🚀 Launching Streamlit app..."
	PYTHONPATH=src uv run streamlit run app.py

# Lint the code with Ruff
lint:
	@echo "🔍 Running Ruff lint..."
	uv run ruff check src

# Autoformat with Ruff
format:
	@echo "🎨 Formatting code with Ruff..."
	uv run ruff format src

# Rebuild the environment
sync:
	@echo "🔄 Syncing dependencies..."
	uv sync --all-extras

# Clean build artifacts
clean:
	@echo "🧹 Cleaning up..."
	rm -rf dist build *.egg-info __pycache__ .pytest_cache .ruff_cache
