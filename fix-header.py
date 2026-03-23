#!/usr/bin/env python3
"""
Restores the MDMP header (0x4D 0x44 0x4D 0x50) to a file.
Usage: python3 fix_header.py <path_to_dump>
"""
import sys
import os
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file>")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"[!] Error: File not found: {filepath}")
        sys.exit(1)

    print(f"[*] Fixing header for {filepath}...")
    
    try:
        with open(filepath, "r+b") as f:
            f.seek(0)
            f.write(bytes([0x4D, 0x44, 0x4D, 0x50]))
        print(f"[+] Header restored successfully.")
    except Exception as e:
        print(f"[!] Error: Could not write to file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
