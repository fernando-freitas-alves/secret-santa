#! /usr/bin/env bash
set -euo pipefail

DIRNAME="$(dirname "$0")"
DIRNAME="$(realpath --relative-to=. "$DIRNAME")"
readonly DIRNAME

REPODIR="$DIRNAME/.."
REPODIR="$(realpath --relative-to=. "$REPODIR")"
readonly REPODIR

ROOT="$REPODIR/src"
ROOT="$(realpath --relative-to=. "$ROOT")"
readonly ROOT

PYTHON_VENV_PATH="$REPODIR/.venv"
PYTHON_VENV_PATH="$(realpath --relative-to=. "$PYTHON_VENV_PATH")"
readonly PYTHON_VENV_PATH

PYTHONPATH="$ROOT:${PYTHONPATH:-}"
export PYTHONPATH

ENTRYPOINT="$ROOT/__main__.py"
ENTRYPOINT="$(realpath --relative-to=. "$ENTRYPOINT")"
readonly ENTRYPOINT

DEFAULT_ARGS=(
    "data/people.txt"
    "data/pair_exclusions.txt"
    "--only-initials"
    "--remove-comments"
    "--strip-whitespaces"
)
readonly DEFAULT_ARGS

if [[ $# -gt 0 ]]; then
    ARGS=$*
else
    ARGS=${DEFAULT_ARGS[*]}
fi

# shellcheck disable=SC2120
enter_python_env()
{
    VIRTUALENV_PATH="$1"
    readonly VIRTUALENV_PATH

    PIP_ACTIVATE="$VIRTUALENV_PATH/bin/activate"
    readonly PIP_ACTIVATE

    # shellcheck disable=SC1090
    source "$PIP_ACTIVATE"
}

(
    # shellcheck disable=SC2119
    enter_python_env "$PYTHON_VENV_PATH"
    set -x
    # shellcheck disable=SC2048,SC2086
    python "$ENTRYPOINT" ${ARGS[*]}
)
