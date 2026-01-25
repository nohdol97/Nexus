#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

${SCRIPT_DIR}/logging/bootstrap_kibana.sh
${SCRIPT_DIR}/logging/bootstrap_kibana_saved_objects.sh

echo "Observability bootstrap complete."
