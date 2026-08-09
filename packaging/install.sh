#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/opt/zelda"
SERVICE_USER="zelda"
UNIT_SOURCE="$(dirname "$(readlink -f "$0")")/systemd/zelda.service"
UNIT_TARGET="/etc/systemd/system/zelda.service"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "Run this installer as root." >&2
  exit 1
fi

if [[ ! -f "$UNIT_SOURCE" ]]; then
  echo "Missing systemd unit: $UNIT_SOURCE" >&2
  exit 1
fi

if ! id "$SERVICE_USER" >/dev/null 2>&1; then
  useradd --system --home-dir "$APP_DIR" --shell /usr/sbin/nologin "$SERVICE_USER"
fi

install -d -o "$SERVICE_USER" -g "$SERVICE_USER" -m 0750 "$APP_DIR"

if [[ -f requirements.txt ]]; then
  python3 -m venv "$APP_DIR/.venv"
  "$APP_DIR/.venv/bin/python" -m pip install --upgrade pip
  "$APP_DIR/.venv/bin/pip" install -r requirements.txt
fi

install -d -m 0755 "$(dirname "$UNIT_TARGET")"
install -m 0644 "$UNIT_SOURCE" "$UNIT_TARGET"

chown -R "$SERVICE_USER:$SERVICE_USER" "$APP_DIR"
systemctl daemon-reload
systemctl enable zelda.service
systemctl restart zelda.service

systemctl --no-pager --full status zelda.service || true
