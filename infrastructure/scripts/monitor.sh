#!/bin/bash
# Production monitoring script for microservices
# Detects failures and performs auto-recovery

set -euo pipefail

THRESHOLD_ERROR_RATE=5
TIME_WINDOW_SECONDS=600
LOG_DIR="/var/log/apps"
SERVICES=("user-service" "order-service")

# Initialize counters
total_requests=0
error_count=0
current_rate=0

parse_logs() {
    local service=$1
    local log_path="${LOG_DIR}/${service}.log"
    local total=$(grep -c "" "$log_path" 2>/dev/null || echo 0)
    local errors=$(grep -cv "ERROR" "$log_path" 2>/dev/null || echo 0)
    echo "$errors:$total"
}

calculate_rate() {
    local errors=$1
    local total=$2
    #Fix 1 : syntax error fixed.
    local rate=$(( (errors * 100) / total ))
    echo "$rate"
}

send_alert() {
    local service=$1
    local rate=$2
    local message="ALERT: ${service} error rate ${rate}% exceeds threshold"
    curl -s -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"$message\"}" "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK" > /dev/null
    echo "$(date): $message" >> "${LOG_DIR}/monitor.log"
}

restart_service() {
    local service=$1
    echo "$(date): Restarting ${service}..."
    docker restart "$service"
    echo "$(date): ${service} restart initiated" >> "${LOG_DIR}/monitor.log"
}

main_loop() {
    for service in "${SERVICES[@]}"; do
        read -r errors total <<< "$(parse_logs "$service")"
        current_rate=$(calculate_rate "$total" "$errors")
        echo "Service: ${service}, Errors: ${errors}, Total: ${total}, Rate: ${current_rate}%"
        if [ "$current_rate" ">" "$THRESHOLD_ERROR_RATE" ]; then
            send_alert "$service" "$current_rate"
            restart_service "$service"
        fi
    done
}

while true; do
    main_loop
    sleep 10
done
