#!/usr/bin/env python3
import sys
import time
from ladxhd_discord_rpc import read_live_state, resolve_location

def main():
    print("==========================================================")
    print(" LADXHD Real-Time Location & Shared Memory Monitor")
    print("==========================================================")
    
    last_overworld = "🏡 Mabe Village"
    while True:
        state = read_live_state()
        if state["InGame"]:
            map_name = state["Map"]
            x = state["X"]
            y = state["Y"]
            grid_x = state["GridX"]
            grid_y = state["GridY"]
            if grid_x < 0 or grid_y < 0:
                grid_x = max(0, min(15, int(x // 160)))
                grid_y = max(0, min(15, int(y // 128)))
            location, last_overworld = resolve_location(map_name, grid_x, grid_y, last_overworld)
        else:
            x, y = 0.0, 0.0
            grid_x, grid_y = 0, 0
            map_name = "menu.map"
            location = "Main Menu"

        out_str = f"[DEBUG] RawX: {x:.2f} | RawY: {y:.2f} -> Grid: [{grid_x}, {grid_y}] | Map: {map_name} | Location: {location}"
        if sys.stdout.isatty():
            print(f"\r{out_str}", end="", flush=True)
        else:
            print(out_str, flush=True)
        time.sleep(0.25)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Stopped Live Terminal Monitor.")
