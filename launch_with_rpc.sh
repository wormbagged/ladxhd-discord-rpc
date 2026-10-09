#!/usr/bin/env bash
# Link's Awakening DX HD — Auto-Launcher with Discord Rich Presence
# Launches the RPC watcher as parent launcher for real-time memory scanning

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export DOTNET_ROOT="${DOTNET_ROOT:-${HOME}/.dotnet}"
export PATH="$DOTNET_ROOT:$PATH"

GAME_EXEC="${1:-./LinksAwakeningDXHD}"
if [ -f "$GAME_EXEC.real" ]; then
    GAME_EXEC="$GAME_EXEC.real"
fi
if [ "$#" -gt 0 ]; then
    GAME_EXEC="$1"
fi

echo "[+] Launching LADXHD with Discord Rich Presence Watcher..."
exec python3 "$SCRIPT_DIR/ladxhd_discord_rpc.py" --slot 0 --auto-exit --log-file "$SCRIPT_DIR/presence.log" --launch "$GAME_EXEC" "$@"
