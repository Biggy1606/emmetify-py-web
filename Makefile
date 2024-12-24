.DEFAULT_GOAL := help
.PHONY: help
help:
	@echo "Makefile commands:"
	@echo "  run_quality_checks:    Run black, isort, mypy, and flake8"
	@echo "  run_tests:             Run pytest"

.PHONY: run_quality_checks
run_quality_checks:
	@echo "======== Running black ========"
	poetry run black .
	@echo "======== Running isort ========"
	poetry run isort .
	@echo "======== Running mypy ========"
	poetry run mypy emmetify
	@echo "======== Running flake8 ========"
	poetry run flake8 emmetify

run_tests:
	poetry run pytest -v --cov=emmetify
