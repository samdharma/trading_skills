#!/bin/bash
# Install the kimi-trading-skills skill into the Kimi Code CLI user skills directory
# and ensure the tscli Python environment is ready.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_SRC="${REPO_ROOT}/skills/kimi-trading-skills"
SKILL_DIR="${HOME}/.kimi-code/skills"
SKILL_LINK="${SKILL_DIR}/kimi-trading-skills"

echo "Installing kimi-trading-skills from ${REPO_ROOT}"

if ! command -v uv >/dev/null 2>&1; then
    echo "Error: uv is required but not installed. See https://docs.astral.sh/uv/"
    exit 1
fi

cd "${REPO_ROOT}"
echo "Installing Python dependencies..."
uv sync --extra dev

echo "Linking skill into Kimi user skills directory..."
mkdir -p "${SKILL_DIR}"
if [ -L "${SKILL_LINK}" ] || [ -e "${SKILL_LINK}" ]; then
    rm -rf "${SKILL_LINK}"
fi
ln -s "${SKILL_SRC}" "${SKILL_LINK}"

echo ""
echo "Done. Use one of the following to run Kimi with this skill:"
echo "  1. From any directory:"
echo "       kimi --skills-dir ${SKILL_DIR}"
echo "  2. From the repo root (${REPO_ROOT}):"
echo "       kimi --skills-dir ./skills"
echo "  3. Auto-loaded if ~/.kimi-code/skills is discovered by your Kimi version:"
echo "       cd ${REPO_ROOT} && kimi"
echo ""
echo "The first tscli command inside a session will run from the repo root via uv."
