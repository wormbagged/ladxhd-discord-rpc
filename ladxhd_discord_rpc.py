#!/usr/bin/env python3
"""
Link's Awakening DX HD — Discord Rich Presence Watcher
A patch-proof, IPC shared-memory Discord Rich Presence generator for LADXHD.
Reads /dev/shm/ladxhd_state.json written at 4Hz by Game1.cs.
"""

import os
import sys
import time
import math
import socket
import argparse
import json
import tempfile
import psutil
from pypresence import Presence

DEFAULT_CLIENT_ID = "1557493288074739843"

def get_state_file_path():
    shm_path = "/dev/shm/ladxhd_state.json"
    if os.path.exists("/dev/shm") and os.path.isdir("/dev/shm"):
        return shm_path
    return os.path.join(tempfile.gettempdir(), "ladxhd_state.json")

STATE_FILE = get_state_file_path()
DEFAULT_LOG_FILE = os.path.expanduser("~/ladxhd_discord_rpc/presence.log")

last_overworld_location = "🏡 Mabe Village"

DUNGEON_ART_KEYS = {
    "dungeon1.map": "dungeon1",
    "dungeon1_2d_1.map": "dungeon1",
    "dungeon1_2d_2.map": "dungeon1",
    "dungeon2.map": "dungeon2",
    "dungeon2_2d_1.map": "dungeon2",
    "dungeon2_2d_2.map": "dungeon2",
    "dungeon2_2d_3.map": "dungeon2",
    "dungeon3.map": "dungeon3",
    "dungeon3_2d.map": "dungeon3",
    "dungeon4.map": "dungeon4",
    "dungeon4_2d_1.map": "dungeon4",
    "dungeon4_2d_2.map": "dungeon4",
    "dungeon4_2d_3.map": "dungeon4",
    "dungeon4_2d_4.map": "dungeon4",
    "dungeon5.map": "dungeon5",
    "dungeon5_entry.map": "dungeon5",
    "dungeon5_2d_1.map": "dungeon5",
    "dungeon5_2d_2.map": "dungeon5",
    "dungeon5_2d_3.map": "dungeon5",
    "dungeon5_2d_4.map": "dungeon5",
    "dungeon6.map": "dungeon6",
    "dungeon6_2d_1.map": "dungeon6",
    "dungeon6_2d_2.map": "dungeon6",
    "dungeon6_2d_3.map": "dungeon6",
    "dungeon7_1.map": "dungeon7",
    "dungeon7_2.map": "dungeon7",
    "dungeon7_3.map": "dungeon7",
    "dungeon7_4.map": "dungeon7",
    "dungeon7_2d.map": "dungeon7",
    "dungeon8.map": "dungeon8",
    "dungeon8_2d_1.map": "dungeon8",
    "dungeon8_2d_2.map": "dungeon8",
    "dungeon8_2d_3.map": "dungeon8",
    "dungeon8_2d_4.map": "dungeon8",
    "dungeon8_2d_5.map": "dungeon8",
    "dungeon8_2d_6.map": "dungeon8",
    "dungeon_color.map": "dungeon_color",
    "egg_entry.map": "egg",
    "egg_boss_room.map": "egg",
    "egg_lower_floor.map": "egg",
    "final stairs.map": "egg",
}

LOCATION_NAME_MAP = {
    "map_wind_fishs_egg": "⛰️ Mount Tamaranch",
    "map_mt_tamaranch": "⛰️ Tal Tal Mountain Range",
    "map_south_village": "🗺️ South of the Village",
    "map_bay_east": "🗺️ East of the Bay",
    "map_koholint_prairie": "🗺️ Koholint Prairie",
    "map_owl_prairie": "🗺️ Koholint Prairie",
    "map_mabe_village": "🏡 Mabe Village",
    "map_madam_meow": "🏡 Mabe Village",
    "map_marin_tarin": "🏡 Mabe Village",
    "map_quadruplets_house": "🏡 Mabe Village",
    "map_village_library": "🏡 Mabe Village",
    "map_old_man_house": "🏡 Mabe Village",
    "map_trendy_game": "🏡 Mabe Village",
    "map_town_tool_shop": "🏡 Mabe Village",
    "map_dream_shrine": "🏡 Mabe Village",
    "map_fishing_pond": "🏡 Mabe Village",
    "map_tal_tal": "⛰️ Tal Tal Mountain Range",
    "map_hen_house": "⛰️ Tal Tal Mountain Range",
    "map_owl_bridge": "⛰️ Tal Tal Mountain Range",
    "map_owl_mountain": "⛰️ Tal Tal Mountain Range",
    "map_owl_fish": "⛰️ Tal Tal Mountain Range",
    "map_tal_tal_heights": "⛰️ Tal Tal Heights",
    "map_owl_tal_tal_heights": "⛰️ Tal Tal Heights",
    "map_photo_both": "⛰️ Tal Tal Heights",
    "map_weird_mr_write": "⛰️ Tal Tal Heights",
    "map_mysterious_woods": "🌲 Mysterious Woods",
    "map_owl_woods": "🌲 Mysterious Woods",
    "map_owl_woods_entry": "🌲 Mysterious Woods",
    "map_goponga_swamp": "🪷 Goponga Swamp",
    "map_crazy_tracy": "🪷 Goponga Swamp",
    "map_witchs_hut": "🌲 Mysterious Woods",
    "map_cementry": "🪦 Cemetery",
    "map_tabahl_wasteland": "🪨 Tabahl Wasteland",
    "map_kanalet_castle": "🏰 Kanalet Castle",
    "map_rapids_ride": "🛶 Rapids Ride",
    "map_raft_shop": "🛶 Rapids Ride",
    "map_ukuku_prairie": "🗺️ Ukuku Prairie",
    "map_seashell_mansion": "🐚 Seashell Mansion",
    "map_signpost_maze": "🪧 Signpost Maze",
    "map_pothole_field": "🪧 Signpost Maze",
    "map_richards_villa": "🪧 Signpost Maze",
    "map_maraths_bay": "⚓ Martha's Bay",
    "map_house_bay": "⚓ Martha's Bay",
    "map_animal_village": "🏡 Animal Village",
    "map_banana_house": "🌊 Toronbo Shores",
    "map_toronbo_shores": "🌊 Toronbo Shores",
    "map_owl_shore": "🌊 Toronbo Shores",
    "map_yarna_desert": "🏜️ Yarna Desert",
    "map_owl_desert": "🏜️ Yarna Desert",
    "map_face_shrine": "🗿 Ancient Ruins",
    "map_owl_shrine": "🗿 Ancient Ruins",
    "map_owl_level_6_post": "🗿 Ancient Ruins",
    "map_owl_level_6": "🗿 Ancient Ruins",
    "map_level_1": "💀 Tail Cave Entrance",
    "map_owl_level_1": "🗺️ South of the Village",
    "map_level_2": "🪷 Bottle Grotto Entrance",
    "map_level_3": "🗝️ Key Cavern Entrance",
    "map_owl_level_3": "🗺️ Ukuku Prairie",
    "map_level_4": "🐟 Angler's Tunnel Entrance",
    "map_level_5": "🐟 Catfish's Maw Entrance",
    "map_level_6": "🗿 Face Shrine Entrance",
    "map_level_7": "🦅 Eagle's Tower Entrance",
    "map_level_8": "🐢 Turtle Rock Entrance",
    "map_telephone_booth": "☎️ Telephone Booth",
}

# Exact 16x16 Koholint Island overworld grid [Y][X]
# Row = GridY (0..15, North to South), Col = GridX (0..15, West to East)
OVERWORLD_RESOLVED_GRID = [
    # Y = 0 (Far North Ridge)
    [
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Mount Tamaranch",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
    ],
    # Y = 1
    [
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Mount Tamaranch",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
        "⛰️ Tal Tal Mountain Range",
    ],
    # Y = 2
    [
        "🪷 Goponga Swamp",
        "🪷 Goponga Swamp",
        "🪷 Goponga Swamp",
        "🪷 Goponga Swamp",
        "🪷 Goponga Swamp",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
    ],
    # Y = 3
    [
        "🪷 Goponga Swamp",
        "🪷 Goponga Swamp",
        "🪷 Goponga Swamp",
        "🪷 Goponga Swamp",
        "🪷 Goponga Swamp",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "⛰️ Tal Tal Heights",
        "🛶 Rapids Ride",
    ],
    # Y = 4
    [
        "🌲 Mysterious Woods",
        "🌲 Mysterious Woods",
        "🌲 Mysterious Woods",
        "🌲 Mysterious Woods",
        "🗺️ Koholint Prairie",
        "🗺️ Koholint Prairie",
        "🪨 Tabahl Wasteland",
        "🪨 Tabahl Wasteland",
        "🏰 Kanalet Castle",
        "🏰 Kanalet Castle",
        "🏰 Kanalet Castle",
        "🏰 Kanalet Castle",
        "🛶 Rapids Ride",
        "🛶 Rapids Ride",
        "🛶 Rapids Ride",
        "🛶 Rapids Ride",
    ],
    # Y = 5
    [
        "🌲 Mysterious Woods",
        "🌲 Mysterious Woods",
        "🌲 Mysterious Woods",
        "🌲 Mysterious Woods",
        "🗺️ Koholint Prairie",
        "🗺️ Koholint Prairie",
        "🪨 Tabahl Wasteland",
        "🪨 Tabahl Wasteland",
        "🏰 Kanalet Castle",
        "🏰 Kanalet Castle",
        "🏰 Kanalet Castle",
        "🏰 Kanalet Castle",
        "🛶 Rapids Ride",
        "🛶 Rapids Ride",
        "🛶 Rapids Ride",
        "🛶 Rapids Ride",
    ],
    # Y = 6
    [
        "🌲 Mysterious Woods",
        "🌲 Mysterious Woods",
        "🌲 Mysterious Woods",
        "🌲 Mysterious Woods",
        "🗺️ Koholint Prairie",
        "🗺️ Koholint Prairie",
        "🪦 Cemetery",
        "🪦 Cemetery",
        "🏰 Kanalet Castle",
        "🏰 Kanalet Castle",
        "🏰 Kanalet Castle",
        "🏰 Kanalet Castle",
        "🛶 Rapids Ride",
        "🛶 Rapids Ride",
        "🛶 Rapids Ride",
        "🛶 Rapids Ride",
    ],
    # Y = 7
    [
        "🌲 Mysterious Woods",
        "🌲 Mysterious Woods",
        "🌲 Mysterious Woods",
        "🌲 Mysterious Woods",
        "🗺️ Koholint Prairie",
        "🗺️ Koholint Prairie",
        "🪦 Cemetery",
        "🪦 Cemetery",
        "🏰 Kanalet Castle",
        "🏰 Kanalet Castle",
        "🏰 Kanalet Castle",
        "🏰 Kanalet Castle",
        "🛶 Rapids Ride",
        "🛶 Rapids Ride",
        "🛶 Rapids Ride",
        "🛶 Rapids Ride",
    ],
    # Y = 8
    [
        "🏡 Mabe Village",
        "🏡 Mabe Village",
        "🏡 Mabe Village",
        "🏡 Mabe Village",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🐚 Seashell Mansion",
        "🗺️ Ukuku Prairie",
        "🗿 Ancient Ruins",
        "🗿 Ancient Ruins",
        "🛶 Rapids Ride",
        "🛶 Rapids Ride",
    ],
    # Y = 9
    [
        "🏡 Mabe Village",
        "🏡 Mabe Village",
        "🏡 Mabe Village",
        "🏡 Mabe Village",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗿 Ancient Ruins",
        "🗿 Ancient Ruins",
        "🛶 Rapids Ride",
        "🛶 Rapids Ride",
    ],
    # Y = 10
    [
        "🏡 Mabe Village",
        "🏡 Mabe Village",
        "🏡 Mabe Village",
        "🏡 Mabe Village",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗿 Ancient Ruins",
        "🗿 Ancient Ruins",
        "🗿 Ancient Ruins",
        "🗿 Ancient Ruins",
    ],
    # Y = 11
    [
        "🏡 Mabe Village",
        "🏡 Mabe Village",
        "🏡 Mabe Village",
        "🏡 Mabe Village",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗿 Ancient Ruins",
        "🗿 Ancient Ruins",
        "🗿 Ancient Ruins",
        "🗿 Ancient Ruins",
    ],
    # Y = 12
    [
        "🗺️ South of the Village",
        "🗺️ South of the Village",
        "🗺️ South of the Village",
        "🗺️ South of the Village",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "⚓ Martha's Bay",
        "⚓ Martha's Bay",
        "⚓ Martha's Bay",
        "⚓ Martha's Bay",
        "🏡 Animal Village",
        "🏡 Animal Village",
        "🏜️ Yarna Desert",
        "🏜️ Yarna Desert",
    ],
    # Y = 13
    [
        "🗺️ South of the Village",
        "🗺️ South of the Village",
        "🗺️ South of the Village",
        "🗺️ South of the Village",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "🗺️ Ukuku Prairie",
        "⚓ Martha's Bay",
        "⚓ Martha's Bay",
        "⚓ Martha's Bay",
        "⚓ Martha's Bay",
        "🏡 Animal Village",
        "🏡 Animal Village",
        "🏜️ Yarna Desert",
        "🏜️ Yarna Desert",
    ],
    # Y = 14
    [
        "🌊 Toronbo Shores",
        "🌊 Toronbo Shores",
        "🌊 Toronbo Shores",
        "🌊 Toronbo Shores",
        "🌊 Toronbo Shores",
        "🌊 Toronbo Shores",
        "⚓ Martha's Bay",
        "⚓ Martha's Bay",
        "⚓ Martha's Bay",
        "⚓ Martha's Bay",
        "⚓ Martha's Bay",
        "⚓ Martha's Bay",
        "🗺️ East of the Bay",
        "🗺️ East of the Bay",
        "🏜️ Yarna Desert",
        "🏜️ Yarna Desert",
    ],
    # Y = 15 (Far South Coast)
    [
        "🌊 Toronbo Shores",
        "🌊 Toronbo Shores",
        "🌊 Toronbo Shores",
        "🌊 Toronbo Shores",
        "🌊 Toronbo Shores",
        "🌊 Toronbo Shores",
        "⚓ Martha's Bay",
        "⚓ Martha's Bay",
        "⚓ Martha's Bay",
        "⚓ Martha's Bay",
        "⚓ Martha's Bay",
        "⚓ Martha's Bay",
        "🗺️ East of the Bay",
        "🗺️ East of the Bay",
        "🏜️ Yarna Desert",
        "🏜️ Yarna Desert",
    ],
]

DUNGEON_NAMES = {
    "dungeon1.map": "💀 Tail Cave (Level 1)",
    "dungeon_1.map": "💀 Tail Cave (Level 1)",
    "level1.map": "💀 Tail Cave (Level 1)",
    "d1.map": "💀 Tail Cave (Level 1)",
    "tail_cave.map": "💀 Tail Cave (Level 1)",
    "tailcave.map": "💀 Tail Cave (Level 1)",

    "dungeon2.map": "💀 Bottle Grotto (Level 2)",
    "dungeon_2.map": "💀 Bottle Grotto (Level 2)",
    "level2.map": "💀 Bottle Grotto (Level 2)",
    "d2.map": "💀 Bottle Grotto (Level 2)",
    "bottle_grotto.map": "💀 Bottle Grotto (Level 2)",
    "bottlegrotto.map": "💀 Bottle Grotto (Level 2)",

    "dungeon3.map": "💀 Key Cavern (Level 3)",
    "dungeon_3.map": "💀 Key Cavern (Level 3)",
    "level3.map": "💀 Key Cavern (Level 3)",
    "d3.map": "💀 Key Cavern (Level 3)",
    "key_cavern.map": "💀 Key Cavern (Level 3)",
    "keycavern.map": "💀 Key Cavern (Level 3)",

    "dungeon4.map": "💀 Angler's Tunnel (Level 4)",
    "dungeon_4.map": "💀 Angler's Tunnel (Level 4)",
    "level4.map": "💀 Angler's Tunnel (Level 4)",
    "d4.map": "💀 Angler's Tunnel (Level 4)",
    "anglers_tunnel.map": "💀 Angler's Tunnel (Level 4)",
    "anglerstunnel.map": "💀 Angler's Tunnel (Level 4)",
    "angler.map": "💀 Angler's Tunnel (Level 4)",

    "dungeon5.map": "💀 Catfish's Maw (Level 5)",
    "dungeon_5.map": "💀 Catfish's Maw (Level 5)",
    "level5.map": "💀 Catfish's Maw (Level 5)",
    "d5.map": "💀 Catfish's Maw (Level 5)",
    "catfishs_maw.map": "💀 Catfish's Maw (Level 5)",
    "catfish_maw.map": "💀 Catfish's Maw (Level 5)",
    "catfish.map": "💀 Catfish's Maw (Level 5)",

    "dungeon6.map": "💀 Face Shrine (Level 6)",
    "dungeon_6.map": "💀 Face Shrine (Level 6)",
    "level6.map": "💀 Face Shrine (Level 6)",
    "d6.map": "💀 Face Shrine (Level 6)",
    "face_shrine.map": "💀 Face Shrine (Level 6)",
    "faceshrine.map": "💀 Face Shrine (Level 6)",

    "dungeon7.map": "💀 Eagle's Tower (Level 7)",
    "dungeon_7.map": "💀 Eagle's Tower (Level 7)",
    "level7.map": "💀 Eagle's Tower (Level 7)",
    "d7.map": "💀 Eagle's Tower (Level 7)",
    "eagles_tower.map": "💀 Eagle's Tower (Level 7)",
    "eagle_tower.map": "💀 Eagle's Tower (Level 7)",
    "eagletower.map": "💀 Eagle's Tower (Level 7)",

    "dungeon8.map": "💀 Turtle Rock (Level 8)",
    "dungeon_8.map": "💀 Turtle Rock (Level 8)",
    "level8.map": "💀 Turtle Rock (Level 8)",
    "d8.map": "💀 Turtle Rock (Level 8)",
    "turtle_rock.map": "💀 Turtle Rock (Level 8)",
    "turtlerock.map": "💀 Turtle Rock (Level 8)",

    "color_dungeon.map": "🌈 Color Dungeon",
    "colordungeon.map": "🌈 Color Dungeon",
    "color.map": "🌈 Color Dungeon",
    "dungeon_color.map": "🌈 Color Dungeon",

    "dungeon_egg.map": "🥚 Wind Fish's Egg",
    "dungeon_egg_boss.map": "🥚 Wind Fish's Egg",
    "egg.map": "🥚 Wind Fish's Egg",
    "wind_fish_egg.map": "🥚 Wind Fish's Egg",
}

def resolve_location(map_name, grid_x, grid_y, last_overworld):
    clean_map = (map_name or "").lower().strip()

    if clean_map == "overworld.map":
        if 0 <= grid_x < 16 and 0 <= grid_y < 16:
            loc = OVERWORLD_RESOLVED_GRID[grid_y][grid_x]
            return loc, loc
        return last_overworld, last_overworld

    if clean_map in DUNGEON_NAMES:
        return DUNGEON_NAMES[clean_map], last_overworld

    if "color" in clean_map:
        return "🌈 Color Dungeon", last_overworld

    if "egg" in clean_map:
        return "🥚 Wind Fish's Egg", last_overworld

    if "dungeon1" in clean_map or "tail" in clean_map:
        return "💀 Tail Cave (Level 1)", last_overworld
    if "dungeon2" in clean_map or "bottle" in clean_map:
        return "💀 Bottle Grotto (Level 2)", last_overworld
    if "dungeon3" in clean_map or "key" in clean_map:
        return "💀 Key Cavern (Level 3)", last_overworld
    if "dungeon4" in clean_map or "angler" in clean_map:
        return "💀 Angler's Tunnel (Level 4)", last_overworld
    if "dungeon5" in clean_map or "catfish" in clean_map:
        return "💀 Catfish's Maw (Level 5)", last_overworld
    if "dungeon6" in clean_map or "face" in clean_map:
        return "💀 Face Shrine (Level 6)", last_overworld
    if "dungeon7" in clean_map or "eagle" in clean_map:
        return "💀 Eagle's Tower (Level 7)", last_overworld
    if "dungeon8" in clean_map or "turtle" in clean_map:
        return "💀 Turtle Rock (Level 8)", last_overworld

    return last_overworld, last_overworld

CUSTOM_MOD_LOCATIONS = {}
CUSTOM_MOD_ART_KEYS = {}

def read_live_state():
    """Reads real-time state emitted by Game1.cs / DiscordRpcBridge at 4Hz into ladxhd_state.json."""
    state_file = get_state_file_path()
    if not os.path.exists(state_file):
        return {
            "InGame": False, "Map": "menu.map", "X": 0.0, "Y": 0.0,
            "GridX": -1, "GridY": -1,
            "CurrentHealth": 0, "MaxHearts": 0, "Rupees": 0,
            "Instruments": 0, "Seashells": 0, "TradeItem": "None",
            "Cleared": False, "GameTime": 0
        }
    try:
        with open(state_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {
                "InGame": bool(data.get("InGame", False)),
                "Map": str(data.get("Map", "menu.map")),
                "X": float(data.get("X", 0.0)),
                "Y": float(data.get("Y", 0.0)),
                "GridX": int(data.get("GridX", -1)),
                "GridY": int(data.get("GridY", -1)),
                "CurrentHealth": int(data.get("CurrentHealth", 0)),
                "MaxHearts": int(data.get("MaxHearts", 0)),
                "Rupees": int(data.get("Rupees", 0)),
                "Instruments": int(data.get("Instruments", 0)),
                "Seashells": int(data.get("Seashells", 0)),
                "TradeItem": str(data.get("TradeItem", "None")),
                "Cleared": bool(data.get("Cleared", False)),
                "GameTime": int(data.get("GameTime", 0)),
            }
    except Exception:
        return {
            "InGame": False, "Map": "menu.map", "X": 0.0, "Y": 0.0,
            "GridX": -1, "GridY": -1,
            "CurrentHealth": 0, "MaxHearts": 0, "Rupees": 0,
            "Instruments": 0, "Seashells": 0, "TradeItem": "None",
            "Cleared": False, "GameTime": 0
        }

def resolve_art_key(map_file):
    """Resolves Discord rich presence image asset key."""
    if map_file in CUSTOM_MOD_ART_KEYS:
        return CUSTOM_MOD_ART_KEYS[map_file]
    return DUNGEON_ART_KEYS.get(map_file, "logo")

def log_event(msg, log_path=DEFAULT_LOG_FILE):
    """Outputs a timestamped log message to stdout and presence.log."""
    t_str = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{t_str}] {msg}"
    print(formatted, flush=True)
    if log_path:
        try:
            log_dir = os.path.dirname(os.path.abspath(log_path))
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            if os.path.exists(log_path) and os.path.getsize(log_path) > 1024 * 1024:
                try:
                    with open(log_path, "r", encoding="utf-8", errors="ignore") as f_in:
                        lines = f_in.readlines()[-100:]
                    with open(log_path, "w", encoding="utf-8") as f_out:
                        f_out.writelines(lines)
                except Exception:
                    pass
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(formatted + "\n")
                f.flush()
        except Exception:
            pass

def ensure_flatpak_discord_symlink():
    """Ensures Flatpak Discord IPC socket is symlinked to $XDG_RUNTIME_DIR/discord-ipc-0 for pypresence compatibility on SteamOS/Linux."""
    if sys.platform == "win32":
        return
    xdg_runtime = os.environ.get("XDG_RUNTIME_DIR")
    uid = os.getuid() if hasattr(os, "getuid") else 1000
    base_dir = xdg_runtime or f"/run/user/{uid}"
    
    flatpak_sockets = [
        os.path.join(base_dir, "app/com.discordapp.Discord/discord-ipc-0"),
        f"/run/user/{uid}/app/com.discordapp.Discord/discord-ipc-0",
        os.path.join(base_dir, ".flatpak/dev.vencord.Vesktop/xdg-run/discord-ipc-0"),
        f"/run/user/{uid}/.flatpak/dev.vencord.Vesktop/xdg-run/discord-ipc-0",
    ]
    
    target_symlink = os.path.join(base_dir, "discord-ipc-0")
    
    for flatpak_socket in flatpak_sockets:
        if os.path.exists(flatpak_socket):
            if not os.path.exists(target_symlink):
                try:
                    os.symlink(flatpak_socket, target_symlink)
                    log_event(f"[+] Created Flatpak Discord IPC symlink: {target_symlink} -> {flatpak_socket}")
                except Exception:
                    pass
            break

def find_ipc_pipe():
    """Finds active Discord, Vesktop, or Flatpak IPC socket path."""
    if sys.platform == "win32":
        return r"\\.\pipe\discord-ipc-0"

    ensure_flatpak_discord_symlink()

    uid = os.getuid() if hasattr(os, "getuid") else 1000
    xdg_runtime = os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{uid}")

    candidates = [
        os.path.join(xdg_runtime, "discord-ipc-0"),
        f"/run/user/{uid}/discord-ipc-0",
        f"/run/user/{uid}/app/com.discordapp.Discord/discord-ipc-0",
        f"/run/user/{uid}/.flatpak/dev.vencord.Vesktop/xdg-run/discord-ipc-0",
        "/tmp/discord-ipc-0",
        f"/run/user/{uid}/app/dev.vencord.Vesktop/discord-ipc-0",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                s.connect(p)
                s.close()
                return p
            except Exception:
                pass
    return None

def get_game_pid():
    """Finds active LADXHD game process PID cross-platform."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            name = proc.info['name'] or ''
            cmdline = ' '.join(proc.info['cmdline'] or [])
            if any(x in cmdline for x in ['reaper', 'steam-launch-wrapper', 'ladxhd_discord_rpc', 'live_terminal', 'bash', '/bin/sh']):
                continue
            if "Link's Awakening DX HD.real" in name or "Link's Awakening DX HD.real" in cmdline or "LADXHD.real" in cmdline:
                return proc.info['pid']
            if "Link's Awakenin" in name or "Links Awakening" in cmdline or "LADXHD" in cmdline:
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

def is_ladxhd_running():
    return get_game_pid() is not None

def main():
    parser = argparse.ArgumentParser(description="LADXHD Discord Rich Presence Watcher")
    parser.add_argument("--client-id", default=DEFAULT_CLIENT_ID, help="Discord Application Client ID")
    parser.add_argument("--game-dir", default=None, help="Path to LADXHD game installation folder")
    parser.add_argument("--slot", type=int, default=None, help="Save slot index")
    parser.add_argument("--auto-exit", action="store_true", help="Exit watcher when LADXHD closes")
    parser.add_argument("--launch", default=None, help="Path to LADXHD game binary")
    parser.add_argument("--log-file", default=DEFAULT_LOG_FILE, help="Path to presence log file")
    args = parser.parse_args()

    log_path = args.log_file
    log_event("===============================================", log_path)
    log_event(" Link's Awakening DX HD — Live Discord RPC", log_path)
    log_event("===============================================", log_path)

    game_dir = args.game_dir
    game_proc = None

    if args.launch:
        import subprocess
        try:
            game_proc = subprocess.Popen([args.launch])
            log_event(f"[+] Launched game process (PID {game_proc.pid})", log_path)
        except Exception as e:
            log_event(f"[-] Failed to launch game executable: {e}", log_path)
            sys.exit(1)

    ipc_pipe = find_ipc_pipe()
    if ipc_pipe:
        log_event(f"[*] Found active Discord IPC socket: {ipc_pipe}", log_path)
        import pypresence.baseclient
        import pypresence.utils
        pypresence.baseclient.get_ipc_path = lambda pipe=None: ipc_pipe
        pypresence.utils.get_ipc_path = lambda pipe=None: ipc_pipe

    log_event("[*] Connecting to Discord / Vesktop RPC...", log_path)
    try:
        rpc = Presence(args.client_id)
        rpc.connect()
        log_event("[+] Connected to Discord RPC successfully!", log_path)
    except Exception as e:
        log_event(f"[-] Failed to connect to Discord/Vesktop: {e}", log_path)
        sys.exit(1)

    start_time = time.time()
    last_update_time = 0.0
    last_location = None
    last_map = None
    last_ingame_state = False
    global last_overworld_location

    log_event("[*] Watching shared memory state (/dev/shm/ladxhd_state.json)...", log_path)

    try:
        while True:
            if game_proc and game_proc.poll() is not None:
                log_event("[*] Game process exited. Shutting down RPC.", log_path)
                break

            if args.auto_exit and not is_ladxhd_running():
                log_event("[*] LADXHD process closed. Shutting down RPC.", log_path)
                break

            now = time.time()
            live_state = read_live_state()
            is_ingame = live_state["InGame"]

            if is_ingame:
                map_file = live_state["Map"]
                world_x = live_state["X"]
                world_y = live_state["Y"]
                grid_x = live_state["GridX"]
                grid_y = live_state["GridY"]
                
                if grid_x < 0 or grid_y < 0:
                    grid_x = max(0, min(15, int(world_x // 160)))
                    grid_y = max(0, min(15, int(world_y // 128)))

                location, last_overworld_location = resolve_location(map_file, grid_x, grid_y, last_overworld_location)
                art_key = resolve_art_key(map_file)
                
                cur_hearts = max(0, live_state["CurrentHealth"] // 4)
                max_hearts = max(3, live_state["MaxHearts"])
                rupees = live_state["Rupees"]
                shells = live_state["Seashells"]
                instruments = live_state["Instruments"]
                trade_item = live_state["TradeItem"]
                cleared = live_state["Cleared"]
                game_sec = live_state["GameTime"]
                
                hrs = game_sec // 3600
                mins = (game_sec % 3600) // 60
                secs = game_sec % 60
                time_str = f"{hrs:02d}:{mins:02d}:{secs:02d}"

                star_prefix = "⭐ " if cleared else ""
                t_str = f" • 🔄 {trade_item}" if (trade_item and trade_item != "None") else ""
                
                details_str = f"{star_prefix}❤️ {cur_hearts}/{max_hearts} • 🎶 {instruments}/8 • 🐚 {shells} • 💎 {rupees}{t_str} • ⏱️ {time_str}"
                state_str = location
                tooltip_str = "Link's Awakening DX HD" + (" (Cleared)" if cleared else "")
            else:
                map_file = "menu.map"
                world_x, world_y = 0.0, 0.0
                location = "Main Menu"
                art_key = "logo"
                details_str = "📍 Main Menu"
                state_str = "In Main Menu"
                tooltip_str = "Link's Awakening DX HD"

            # Force immediate update when transitioning from Main Menu to InGame
            state_transition = (is_ingame and not last_ingame_state)

            if state_transition or (now - last_update_time >= 1.0 and (
                location != last_location or 
                map_file != last_map or 
                (now - last_update_time > 10.0))):

                last_ingame_state = is_ingame
                last_location = location
                last_map = map_file
                last_update_time = now

                log_event(f"[RPC Output] Sending -> Details: '{details_str}' | State: '{state_str}'", log_path)

                try:
                    rpc.update(
                        details=details_str,
                        state=state_str,
                        start=int(start_time),
                        large_image=art_key,
                        large_text=location,
                        small_image="link",
                        small_text=tooltip_str
                    )
                    log_event(f"[RPC Updated] Sent successfully: Details: '{details_str}' | State: '{state_str}'", log_path)
                except Exception as e:
                    log_event(f"[RPC ERROR] Failed to update Discord RPC: {e}", log_path)

            time.sleep(0.25)
    except KeyboardInterrupt:
        log_event("[*] Exiting Discord RPC watcher.", log_path)
        rpc.close()

if __name__ == "__main__":
    main()
