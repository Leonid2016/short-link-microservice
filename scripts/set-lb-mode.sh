#!/bin/sh
set -eu

MODE="${1:-}"

if [ "$MODE" != "active-active" ] && [ "$MODE" != "active-passive" ]; then
  echo "Usage: ./scripts/set-lb-mode.sh active-active|active-passive"
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CONF_FILE="$ROOT_DIR/gateway/lb-upstreams.conf"

if [ "$MODE" = "active-active" ]; then
cat > "$CONF_FILE" <<'EOF'
map $request_uri $lb_mode {
    default active-active;
}

upstream auth_pool {
    server auth-service:5001;
    server auth-service-b:5001;
}

upstream links_pool {
    server links-service:5002;
    server links-service-b:5002;
}

upstream analytics_pool {
    server analytics-service:5003;
    server analytics-service-b:5003;
}
EOF
else
cat > "$CONF_FILE" <<'EOF'
map $request_uri $lb_mode {
    default active-passive;
}

upstream auth_pool {
    server auth-service:5001 max_fails=1 fail_timeout=2s;
    server auth-service-b:5001 backup;
}

upstream links_pool {
    server links-service:5002 max_fails=1 fail_timeout=2s;
    server links-service-b:5002 backup;
}

upstream analytics_pool {
    server analytics-service:5003 max_fails=1 fail_timeout=2s;
    server analytics-service-b:5003 backup;
}
EOF
fi

cd "$ROOT_DIR/deploy"
docker compose exec gateway nginx -t
docker compose exec gateway nginx -s reload

echo "LB mode switched to: $MODE"