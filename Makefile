.PHONY: check install-hooks

check:
	.venv/bin/ruff check .
	.venv/bin/pytest

install-hooks:
	ln -sf ../../scripts/pre-push .git/hooks/pre-push
	@echo "Installed pre-push hook (ruff + pytest)."
