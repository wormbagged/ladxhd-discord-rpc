#!/usr/bin/env python3
"""
Utility script to upscale small pixel art or screenshots to 512x512 PNG
for Discord Developer Portal Rich Presence Art Assets.
Uses nearest-neighbor interpolation to keep pixel art crisp without blur.
"""

import sys
import os
from PIL import Image

def upscale_image(input_path, output_path=None, target_size=512):
    if not os.path.exists(input_path):
        print(f"[-] Error: File '{input_path}' not found.")
        sys.exit(1)

    if not output_path:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_512x512.png"

    try:
        im = Image.open(input_path)
        # Handle transparency / RGBA
        if im.mode != "RGBA":
            im = im.convert("RGBA")
            
        # Nearest neighbor resampling keeps retro pixel art sharp and crisp
        resample_filter = Image.Resampling.NEAREST if im.width < target_size else Image.Resampling.LANCZOS
        
        # Maintain aspect ratio in square canvas
        canvas = Image.new("RGBA", (target_size, target_size), (0, 0, 0, 0))
        
        scale = min(target_size / im.width, target_size / im.height)
        new_w = int(im.width * scale)
        new_h = int(im.height * scale)
        
        resized = im.resize((new_w, new_h), resample_filter)
        
        # Center in 512x512 canvas
        offset_x = (target_size - new_w) // 2
        offset_y = (target_size - new_h) // 2
        canvas.paste(resized, (offset_x, offset_y), resized)
        
        canvas.save(output_path, "PNG")
        print(f"[+] Successfully upscaled '{input_path}' -> '{output_path}' ({target_size}x{target_size} PNG)")
    except Exception as e:
        print(f"[-] Error upscaling image: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 upscale_asset.py <path_to_small_image.png> [output_512x512.png]")
        sys.exit(1)

    inp = sys.argv[1]
    outp = sys.argv[2] if len(sys.argv) > 2 else None
    upscale_image(inp, outp)
