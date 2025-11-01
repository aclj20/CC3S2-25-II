#!/bin/bash
set -euo pipefail

PORT="${PORT}"
APP_NAME="${APP_NAME}"
LOG_LEVEL="${LOG_LEVEL}"

echo "Arrancando $APP_NAME en puerto $PORT (log level: $LOG_LEVEL)"