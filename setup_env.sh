#!/usr/bin/env bash
set -euo pipefail

ENV_FILE=".bot_env.sh"
TLS_USERNAME_VALUE="${TLS_USERNAME:-}"
TLS_PASSWORD_VALUE="${TLS_PASSWORD:-6E-p9FDmHECwNvy}"
USE_VPN_VALUE="${USE_VPN:-false}"

usage() {
  cat <<'EOF'
Usage:
  bash setup_env.sh [options]

Options:
  -u, --username <value>      TLS username
  -p, --password <value>      TLS password
  -v, --use-vpn <true|false>  Enable/disable VPN (default: true)
  -f, --file <path>           Output env file path (default: .bot_env.sh)
  -h, --help                  Show this help message

Examples:
  bash setup_env.sh --username my_user --password my_pass --use-vpn false
  bash setup_env.sh
EOF
}

to_bool() {
  local raw
  raw="$(echo "$1" | tr '[:upper:]' '[:lower:]')"
  case "$raw" in
    1|true|yes|y|on) echo "true" ;;
    0|false|no|n|off) echo "false" ;;
    *)
      echo "Invalid boolean value: $1 (use true/false)" >&2
      exit 1
      ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    -u|--username)
      TLS_USERNAME_VALUE="${2:-}"
      shift 2
      ;;
    -p|--password)
      TLS_PASSWORD_VALUE="${2:-}"
      shift 2
      ;;
    -v|--use-vpn)
      USE_VPN_VALUE="$(to_bool "${2:-}")"
      shift 2
      ;;
    -f|--file)
      ENV_FILE="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$TLS_USERNAME_VALUE" ]]; then
  read -r -p "TLS username: " TLS_USERNAME_VALUE
fi

if [[ -z "$TLS_PASSWORD_VALUE" ]]; then
  read -r -s -p "TLS password: " TLS_PASSWORD_VALUE
  echo
fi

if [[ -z "$USE_VPN_VALUE" ]]; then
  read -r -p "Use VPN (true/false) [false]: " USE_VPN_INPUT
  if [[ -n "$USE_VPN_INPUT" ]]; then
    USE_VPN_VALUE="$(to_bool "$USE_VPN_INPUT")"
  else
    USE_VPN_VALUE="false"
  fi
else
  USE_VPN_VALUE="$(to_bool "$USE_VPN_VALUE")"
fi

cat > "$ENV_FILE" <<EOF
#!/usr/bin/env bash
export TLS_USERNAME=$(printf '%q' "$TLS_USERNAME_VALUE")
export TLS_PASSWORD=$(printf '%q' "$TLS_PASSWORD_VALUE")
export USE_VPN=$(printf '%q' "$USE_VPN_VALUE")
EOF

chmod 600 "$ENV_FILE"

echo "Environment file created: $ENV_FILE"
echo "Load variables in current shell with:"
echo "  source $ENV_FILE"
