# Contributing

This guide will explain how to set the project up locally and make code contributions.

## Requirements

For local development, you will need:

- [`uv`](https://github.com/astral-sh/uv) package manager;
- [`just`](https://github.com/casey/just) command runner.

## Getting Started

Having ensured that all software requirements are met, it's enough to:

```shell
just setup
```

This will:

- Download a standalone build of Python;
- Create a virtual environment with seed packages;
- Install all development dependencies;
- Install `pre-commit` hooks.

And just like that, you're ready to code!

## Testing Changes

To test your code changes, you can:

```shell
just test
```

## Generating Documentation

To generate these pages from their respective Markdown sources, you would:

```shell
just build-documentation
```

If you are developing locally and would like real-time updates while changing content, then:

```shell
just serve-documentation
```
