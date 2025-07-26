#!/usr/bin/env -S just --justfile

set shell := ["/bin/bash", "-c"]

alias check := typecheck
alias demo := demonstrate

build: download
    uv build

clean:
    script/clean.py

demonstrate:
    uv run example.py

download:
    script/download.py

format: lint
    uv run ruff format

lint:
    uv run ruff check --extend-select I --fix

lock:
    uv lock

pytion:
    uv python install

sync:
    uv sync --all-packages --all-groups --all-extras

test:
    uv run pytest -vv

typecheck:
    uv run ty check .

upgrade:
    uv lock --upgrade

venv:
    uv venv --seed --allow-existing
