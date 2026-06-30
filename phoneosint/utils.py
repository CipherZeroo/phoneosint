#!/usr/bin/env python3
"""
phoneosint — Utility Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Author  : CipherZeroo
Version : 1.0.0
"""

import json
import webbrowser
from datetime import datetime
from colorama import Fore, Style


def open_in_browser(url: str):
    try:
        webbrowser.open(url, new=2)
        print(f"{Fore.GREEN}[✓] Opened: {url}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to open browser: {e}{Style.RESET_ALL}")


def timestamp() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")


def save_json(data: dict, path: str):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4, default=str)
        print(f"{Fore.GREEN}[✓] Saved: {path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to save JSON: {e}{Style.RESET_ALL}")


def print_separator(char="─", length=60, color=None):
    c = Fore.CYAN if color is None else color
    print(f"{c}{char * length}{Style.RESET_ALL}")
