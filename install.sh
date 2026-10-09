#!/usr/bin/env bash
# Link's Awakening DX HD — Platform-Agnostic Automated Setup Script

set -e

echo "=========================================================="
echo " Link's Awakening DX HD — Discord Rich Presence Setup"
echo "=========================================================="

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ensure Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "[-] Error: python3 is required but not installed."
    exit 1
fi

echo "[*] Installing required Python packages (pypresence, psutil)..."
python3 -m pip install --user --break-system-packages pypresence psutil 2>/dev/null || \
python3 -m pip install --user pypresence psutil

# Make scripts executable
chmod +x "$SCRIPT_DIR/ladxhd_discord_rpc.py" "$SCRIPT_DIR/launch_with_rpc.sh"

echo "[+] Setup complete!"
echo ""
echo "Automatic Execution Methods:"
echo "1. Game Directory Auto-Launcher Shim:"
echo "   Launching 'Link's Awakening DX HD' from Steam, Lutris, Desktop, or File Manager"
echo "   will automatically launch Discord RPC alongside the game."
echo ""
echo "2. Steam Launch Options (Alternative):"
echo "   \"$SCRIPT_DIR/launch_with_rpc.sh\" %command%"
echo ""
echo "Modding Support:"
echo "   Custom .map files in Data/Maps or Mods/ are automatically discovered!"
echo "   Define custom location names & artwork keys in rpc_mods.json"
echo "=========================================================="
