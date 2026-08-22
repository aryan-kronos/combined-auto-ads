#!/usr/bin/env bash
set -e

echo "========================================="
echo "🚀 STARTING BITZ ALL-IN-ONE BOT ENGINE"
echo "========================================="

# Start Auto Boost Bot
echo "⚡ Launching Auto Boost Bot..."
cd /app/autobot && python3 main.py &
AUTOBOT_PID=$!

# Start Ads & Bio Bot
echo "📢 Launching Ads & Auto Bio Bot..."
cd /app/adsbot && python3 main.py &
ADSBOT_PID=$!

echo "✅ Both bots are successfully running!"
echo "Autobot PID: $AUTOBOT_PID | Adsbot PID: $ADSBOT_PID"

# Trap exit signals
trap "kill -TERM $AUTOBOT_PID $ADSBOT_PID 2>/dev/null || true" SIGTERM SIGINT

# Keep container alive and monitor
wait -n $AUTOBOT_PID $ADSBOT_PID
