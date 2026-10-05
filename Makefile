.PHONY: setup test web-build preview examples

setup:
	uv sync --group dev
	corepack pnpm --dir web install

test:
	uv run ruff check . && uv run pytest -q
	corepack pnpm --dir web build && corepack pnpm --dir web check:public-build

web-build:
	corepack pnpm --dir web build

# The harness side (corpus server, private API) runs from HARNESS_ROOT on loopback.
preview:
	./scripts/public-preview.sh

examples:
	uv run python scripts/export_public_examples.py
