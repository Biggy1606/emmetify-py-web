.DEFAULT_GOAL := help
.PHONY: help
help:
	@echo "Makefile commands:"
	@echo "  run-quality-checks:    Run black, isort, mypy, and flake8"
	@echo "  run-tests:             Run pytest"

.PHONY: run-quality-checks
run-quality-checks:
	@echo "======== Running black ========"
	poetry run black .
	@echo "======== Running isort ========"
	poetry run isort .
	@echo "======== Running flake8 ========"
	poetry run flake8 emmetify
	@echo "======== Running mypy ========"
	poetry run mypy emmetify

.PHONY: run-tests
run-tests:
	poetry run pytest -v --cov=emmetify
