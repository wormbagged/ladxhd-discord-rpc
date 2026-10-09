# Link's Awakening DX HD — Discord Rich Presence (LADXHD-RPC)

A patch-proof, standalone Discord Rich Presence watcher for *The Legend of Zelda: Link's Awakening DX HD*.

## Features
- **Real-Time Game Tracking**: Reads active save state (`save0`) to display your exact location on Koholint Island or inside dungeons in real time.
- **Detailed Player Stats**:
  - 📍 **Location**: Dungeons (Tail Cave, Bottle Grotto, Key Cavern, etc.), Villages, Caves, Shrines, Egg.
  - ❤️ **Hearts**: Live current / max heart count.
  - 💎 **Rupees**: Current rupee balance.
  - 🐚 **Secret Seashells**: Total collected.
  - 🎷 **Sirens Instruments**: Progress toward the 8 Instruments of the Sirens.
  - 💀 **Deaths**: Total death count.
- **Patch-Proof Architecture**: Runs as an external state watcher, meaning game updates (v2.0.8, v2.0.9, etc.) won't break the Rich Presence integration.
- **Cross-Platform & Vesktop Compatible**: Works natively with Discord and Vesktop (Flatpak/Linux).

---

## Setup Instructions

### Step 1: Create Your Free Discord Application ID
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click **New Application** and name it `Link's Awakening DX HD`.
3. Copy the **Application ID** (Client ID).
4. *(Optional)* Upload artwork under **Rich Presence → Art Assets**:
   - `logo` (Large image): Game artwork or logo
   - `link` (Small image): Link or Heart icon

### Step 2: Configure Client ID
Open `ladxhd_discord_rpc.py` in a text editor and set your Application ID:
```python
CLIENT_ID = "YOUR_DISCORD_APPLICATION_ID_HERE"
```

### Step 3: Run the Watcher
Run the script in terminal:
```bash
python3 ladxhd_discord_rpc.py
```

Or run it alongside LADXHD automatically!
