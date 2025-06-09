#!/usr/bin/env -S bash --login
set -euo pipefail
# This script is used to install any custom packages required by the algorithm.

# install uv
conda install uv
source $HOME/.local/bin/env

# Get current location of build script
basedir=$( cd "$(dirname "$0")" ; pwd -P )

# install dependencies
UV_PROJECT=$basedir uv sync --no-dev

# unset PROJ env vars
unset PROJ_LIB
unset PROJ_DATA
