#! /usr/bin/env bash
set -euo pipefail
shopt -s expand_aliases
export PROMPT_DIRTRIM=1

## SETUP ###############################################################################

DIRNAME="$(dirname "$0")"
DIRNAME="$(realpath --relative-to=. "$DIRNAME")"
readonly DIRNAME

REPODIR="$DIRNAME/.."
REPODIR="$(realpath --relative-to=. "$REPODIR")"
readonly REPODIR

PYTHON_VENV_PATH="$REPODIR/.venv"
PYTHON_VENV_PATH="$(realpath --relative-to=. "$PYTHON_VENV_PATH")"
readonly PYTHON_VENV_PATH

ROOT="$REPODIR/src"
ROOT="$(realpath --relative-to=. "$ROOT")"
readonly ROOT

BANDIT_CONFIG="./bandit.yaml"
BANDIT_CONFIG="$(realpath --relative-to=. "$BANDIT_CONFIG")"
readonly BANDIT_CONFIG

MYPY_CONFIG="$REPODIR/setup.cfg"
MYPY_CONFIG="$(realpath --relative-to=. "$MYPY_CONFIG")"
readonly MYPY_CONFIG

HELP="Run linters.

Usage:
  $(basename "$0") [options] [LINTERS...]

Options:
  -h, --help    Show this help text
  -c, --check   Run linters in check mode, which will NOT try to automatically fix the code if any error is found

Examples:
  $(basename "$0")                # run all (fix) linters in a docker container
  $(basename "$0") -c             # run all (check-only) linters in a docker container
  $(basename "$0") black          # run black linter in a docker container
  $(basename "$0") -c isort mypy  # run (check-only) isort and mypy linters"
readonly HELP

## PRINTS ##############################################################################

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
NC='\033[0m'
readonly RED
readonly GREEN
readonly YELLOW
readonly NC

function print_stderr()
(
    MSG="$1"
    COLOR="${2:-$YELLOW}"
    echo -e "\n${COLOR}${MSG}${NC}" >&2
)

## METHODS #############################################################################

alias run_linter_mypy='print_stderr MYPY && execute python -m mypy --config-file "$MYPY_CONFIG" "$ROOT" && echo All done! ✨ 🍪 ✨'

function define_check_linters() {
    alias run_linter_black='print_stderr BLACK && execute python -m black --diff --check "$ROOT"'
    alias run_linter_isort='print_stderr ISORT && execute python -m isort --check "$ROOT" && echo All done! ✨ 🍪 ✨'
    alias run_linter_autoflake='print_stderr AUTOFLAKE && execute python -m autoflake -r "$ROOT" && echo All done! ✨ 🌯 ✨'
}

alias run_linter_autoflake='print_stderr AUTOFLAKE && execute python -m autoflake -r --in-place --remove-unused-variables "$ROOT" && echo All done! ✨ 🌯 ✨'
alias run_linter_bandit='print_stderr BANDIT && execute bandit -c "$BANDIT_CONFIG" -r "$ROOT" && echo All done! ✨ 🧁 ✨'
alias run_linter_black='print_stderr BLACK && execute python -m black "$ROOT"'
alias run_linter_flake8='print_stderr FLAKE8 && execute python -m flake8 "$ROOT" && echo All done! ✨ 🍩 ✨'
alias run_linter_isort='print_stderr ISORT && execute python -m isort "$ROOT" && echo All done! ✨ 🍪 ✨'
alias run_linter_mypy='print_stderr MYPY && execute python -m mypy --config-file "$MYPY_CONFIG" --cache-dir ".mypy_cache/container" "$ROOT" && echo All done! ✨ 🍪 ✨'

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

function execute() (
    echo "> $*"
    echo ""
    eval "$*"
)

## ARGS ################################################################################

read -r -a run_all_linters <<< "$(compgen -a | grep '^run_' | xargs)"
declare -a run_spec_linters

declare -a ARGS
while (( $# )); do
    case "$1" in
        # -h or --help show help
        "-h"|"--help")
            echo "$HELP" >&2
            exit 0
            ;;
        # -c or --check argument to run in check mode
        "-c"|"--check")
            define_check_linters
            ;;
        *)
            ARGS+=("$1")
    esac
    shift
done
set -- "${ARGS[@]+${ARGS[@]}}"

while (( $# )); do
    # argument as the name of the linter to run only that linter
    run_all_linters=()
    run_spec_linters+=("run_linter_$1")
    shift
done

run_linter_cmds=( "${run_all_linters[@]+${run_all_linters[@]}}" "${run_spec_linters[@]+${run_spec_linters[@]}}" )

function run_linters() {
    RC=0
    EC=
    for run_linter_cmd in "${run_linter_cmds[@]}"; do
        # shellcheck disable=SC1083
        set +e
        eval "$run_linter_cmd"
        EC=$?
        set -e
        if [ $EC -ne 0 ]; then
            RC=$EC
            linter_name="${run_linter_cmd:11}"
            print_stderr "ERROR while running $linter_name linter!" "$RED"
        fi
    done
    if [ $RC -eq 0 ]; then
        print_stderr "DONE!" "$GREEN"
        echo "All linters run successfully."
    else
        print_stderr "ERROR in one or more linters. Check above for details." "$RED"
    fi
    exit $RC
}


## MAIN ################################################################################

(
    cd "$REPODIR"
    # shellcheck disable=SC2119
    enter_python_env "$PYTHON_VENV_PATH"
    run_linters
)
