#!/usr/bin/env -S bash --login
set -euo pipefail
# This script is used to install any custom packages required by the algorithm.

# install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Get current location of build script
basedir=$( cd "$(dirname "$0")" ; pwd -P )

# install dependencies
UV_PROJECT=$basedir uv sync --no-dev
