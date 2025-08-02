#!/usr/bin/env -S just --justfile

set shell := ["/bin/bash", "-c"]

alias check := run-type-checker
alias clean := clean-generated-files
alias demo := run-example
alias docs := build-documentation
alias docserver := serve-documentation
alias download := download-cloc-script
alias export := export-requirements
alias format := run-formatter
alias hooks := run-hooks
alias lint := run-linter
alias lock := check-lockfile
alias package := build-package
alias python := install-python
alias setup := set-up-project
alias sync := sync-dependencies
alias test := run-tests
alias upgrade := upgrade-lockfile
alias venv := create-virtual-environment

default:
    just --list

build-documentation:
    uv run mkdocs build

build-package: download-cloc-script
    uv build

check-lockfile:
    uv lock --check

clean-generated-files:
    uv run script/clean.py

create-virtual-environment:
    uv venv --seed --allow-existing

download-cloc-script:
    uv run script/download.py

export-requirements:
    uv export --format requirements-txt \
              --output-file requirements-dev.txt \
              --all-extras \
              --all-groups \
              --all-packages \
              --no-annotate \
              --no-hashes \
              --no-header \
              --quiet

install-hooks:
    uv run pre-commit install

install-python:
    uv python install

run-example: download-cloc-script
    uv run example.py

run-formatter: run-linter
    uv run ruff format

run-hooks:
    uv run pre-commit run --all-files

run-linter:
    uv run ruff check --fix

run-tests: download-cloc-script
    uv run pytest -vv

run-type-checker:
    uv run ty check

serve-documentation:
    uv run mkdocs serve

set-up-project: install-python create-virtual-environment sync-dependencies install-hooks

sync-dependencies:
    uv sync --all-packages --all-groups --all-extras

upgrade-lockfile:
    uv lock --upgrade
