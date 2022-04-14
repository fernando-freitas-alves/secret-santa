#! /usr/bin/env bash
set -euo pipefail

DIRNAME="$(dirname "$0")"
DIRNAME="$(realpath --relative-to=. "$DIRNAME")"
readonly DIRNAME

REPODIR="$DIRNAME/.."
REPODIR="$(realpath --relative-to=. "$REPODIR")"
readonly REPODIR

PYTHON_TARGET_VERSION="3.8"  # Only major.minor
readonly PYTHON_TARGET_VERSION

PYTHON_VENV_PATH="$REPODIR/.venv"
PYTHON_VENV_PATH="$(realpath --relative-to=. "$PYTHON_VENV_PATH")"
readonly PYTHON_VENV_PATH

PYTHON_ENV_FILE="$REPODIR/requirements.txt"
PYTHON_ENV_FILE="$(realpath --relative-to=. "$PYTHON_ENV_FILE")"
readonly PYTHON_ENV_FILE

PYTHON_DEV_ENV_FILE="$REPODIR/requirements-dev.txt"
PYTHON_DEV_ENV_FILE="$(realpath --relative-to=. "$PYTHON_DEV_ENV_FILE")"
readonly PYTHON_DEV_ENV_FILE

HELP="Setup environment.

Usage:
  $(basename "$0") [options]

Options:
  -h, --help                                      Show this help text
  -v, --venv, --virtual, --virtual-environment    Update Python virtual env only (default if no option is passed)
  -r, --req, --requirements                       Update Python requirements only but without using virtual env
  -g, --git, --git-hook                           Install git hooks only (default if no option is passed)"
readonly HELP

RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
CYAN='\033[1;36m'
NC='\033[0m'

readonly RED
readonly GREEN
readonly YELLOW
readonly NC

function print_stderr() {
    MSG="$1"
    COLOR="${2:-$YELLOW}"
    echo -e "\n${COLOR}${MSG}${NC}" >&2
}

install_python_venv()
(
    VIRTUALENV_PATH="$1"
    readonly VIRTUALENV_PATH

    PIP_ACTIVATE="$VIRTUALENV_PATH/bin/activate"
    readonly PIP_ACTIVATE

    PYTHON_VERSION=
    if [ -f "$PIP_ACTIVATE" ]; then
        print_stderr "* Virtual environment already installed." "$CYAN"
        # shellcheck disable=SC1090
        source "$PIP_ACTIVATE"
        PYTHON_VERSION="$(python --version | cut -d' ' -f2 | cut -d. -f1,2)"
        print_stderr "* Found python version: '$PYTHON_VERSION'. (Required: '$PYTHON_TARGET_VERSION')" "$CYAN"
    fi
    if [ "$PYTHON_VERSION" != "$PYTHON_TARGET_VERSION" ]; then
        print_stderr "* Installing required python version ('$PYTHON_TARGET_VERSION') in the virtual environment..." "$CYAN"
        if ! virtualenv -p="python.${PYTHON_TARGET_VERSION//./}" "$VIRTUALENV_PATH"; then
            print_stderr "Make sure you have 'virtualenv' and Python $PYTHON_TARGET_VERSION installed" "$RED"
            exit 1
        fi
        # shellcheck disable=SC1090
        source "$PIP_ACTIVATE"
    fi

    echo "$PIP_ACTIVATE"
)

update_python_env()
(
    REQUIREMENTS_FILE="$1"
    REQUIREMENTS_DEV_FILE="$2"
    VIRTUALENV_PATH="${3:-}"

    readonly REQUIREMENTS_FILE
    readonly REQUIREMENTS_DEV_FILE
    readonly VIRTUALENV_PATH

    if [ "$VIRTUALENV_PATH" != "" ]; then
        PIP_ACTIVATE="$VIRTUALENV_PATH/bin/activate"
        readonly PIP_ACTIVATE
        # shellcheck disable=SC1090
        source "$PIP_ACTIVATE"
    fi

    print_stderr "* Installing requirements from '$REQUIREMENTS_FILE' and '$REQUIREMENTS_DEV_FILE'..." "$CYAN"
    pip install --upgrade -r "$REQUIREMENTS_FILE" -r "$REQUIREMENTS_DEV_FILE"
)

prepare_python_venv()
(
    print_stderr "* Installing Python virtual environment..."
    install_python_venv "$PYTHON_VENV_PATH"
)

update_python_venv()
(
    ARG_PYTHON_VENV_PATH="$1"

    print_stderr "* Updating Python environment..."
    update_python_env "$PYTHON_ENV_FILE" "$PYTHON_DEV_ENV_FILE" "$ARG_PYTHON_VENV_PATH"
)

install_git_hooks()
(
    print_stderr "* Installing pre-commit hooks..."
    # shellcheck disable=SC1091
    source "$PYTHON_VENV_PATH/bin/activate"
    pre-commit install-hooks
    pre-commit install --config "$REPODIR/.pre-commit-config.yaml"
)


declare -a ARGS
if [ $# -eq 0 ]; then
    set -- --env --virtual-environment --git-hook
fi

PYTHON_PIP_ACTIVATE=

while (( $# )); do
    case "$1" in
        # -h or --help show help
        "-h"|"--help")
            echo "$HELP" >&2
            exit 0
            ;;
        # -v or --venv or --virtual or --virtual-environment to update Python virtual env only
        "-v"|"--venv"|"--virtual"|"--virtual-environment")
            prepare_python_venv
            PYTHON_PIP_ACTIVATE="$(prepare_python_venv)"
            update_python_venv "$PYTHON_VENV_PATH"
            ;;
        # -r or --req or --requiements to update Python requirements only but without using virtual env
        "-r"|"--req"|"--requirements")
            set +u
            if [ "$VIRTUAL_ENV" == "" ]; then
                set -u
                update_python_venv
            else
                set -u
                update_python_venv "$PYTHON_VENV_PATH"
            fi
            ;;
        # -g or or --git or --git-hook to install git hooks only
        "-g"|"--git"|"--git-hook")
            install_git_hooks
            ;;
        *)
            ARGS+=("$1")
    esac
    shift
done
set -- "${ARGS[@]+${ARGS[@]}}"

print_stderr "DONE!" "$GREEN"
if [ "$PYTHON_PIP_ACTIVATE" != "" ]; then
    echo "Now you can use the Python virtual enviroment by running:"
    echo "    source $PYTHON_PIP_ACTIVATE"
fi
