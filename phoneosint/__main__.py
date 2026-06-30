#!/usr/bin/env python3
"""
phoneosint — CLI Entry Point
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Author  : CipherZeroo
Version : 1.0.0
"""

import sys
import argparse
from colorama import init, Fore, Style

from . import __version__, __author__, __credits__
from .core import PhoneInfo
from .scanners import online_lookup
from .dorker import generate_dorks

init(autoreset=True)

BANNER = f"""
{Fore.CYAN}{Style.BRIGHT}
   ___ _                      ___  _____ _____ _   _ _____
  / _ \\ |__   ___  _ __ ___  / _ \\/  ___|_   _| \\ | |_   _|
 / /_)/ '_ \\ / _ \\| '_ ` _ \\/ /_\\ \\ `--.  | | |  \\| | | |
/ ___/| | | | (_) | | | | |/ ___ \\ `--. \\ | | | |\\  | | |
\\/    |_| |_|\\___/|_| |_| |_/   \\_\\_____/ \\_/ \\_| \\_/ \\_/
{Style.RESET_ALL}
{Fore.GREEN}Phone OSINT Reconnaissance Tool   v{__version__}{Style.RESET_ALL}
{Fore.YELLOW}Author : {__author__}{Style.RESET_ALL}
{Fore.YELLOW}Credits: {__credits__}{Style.RESET_ALL}
{Fore.RED}[!] Use only on systems you own or have explicit permission to test.
{Style.RESET_ALL}
"""


def main():
    parser = argparse.ArgumentParser(
        prog="phoneosint",
        description="Advanced OSINT reconnaissance tool for phone numbers — by CipherZeroo",
        epilog="CipherZeroo — https://github.com/CipherZeroo/phoneosint",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    target = parser.add_argument_group("Target")
    target.add_argument("-n", "--number", type=str, help="Phone number in international format (e.g. +1234567890)")
    target.add_argument("-b", "--batch", type=str, help="Path to file containing phone numbers (one per line)")
    target.add_argument("--country", type=str, default=None, help="ISO country code hint (e.g. US, GB, DE)")

    scan = parser.add_argument_group("Scan Options")
    scan.add_argument("--dorks", type=str, nargs="?", const="all",
                      choices=["social_networks", "forums", "classifieds", "pastes",
                               "people_search", "phone_directories", "reputation", "all"],
                      help="Generate Google dorks for the given category (default: all)")
    scan.add_argument("--map", action="store_true", help="Open results location in Google Maps (area code level)")
    scan.add_argument("--browser", action="store_true", help="Open dork URLs in default browser")
    scan.add_argument("--json", type=str, help="Export results to JSON file")
    scan.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    api = parser.add_argument_group("External APIs (Optional)")
    api.add_argument("--numverify-key", type=str, help="NumVerify API key for carrier verification")
    api.add_argument("--twilio-sid", type=str, help="Twilio Account SID")
    api.add_argument("--twilio-token", type=str, help="Twilio Auth Token")

    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__} by {__author__}")
    parser.add_argument("--credits", action="store_true", help="Show credits and exit")

    args = parser.parse_args()

    if args.credits:
        print(f"\n{Fore.CYAN}phoneosint v{__version__}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Author : {__author__}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Credits: {__credits__}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}License: GPL-3.0-or-later{Style.RESET_ALL}")
        sys.exit(0)

    print(BANNER)

    numbers = []
    if args.number:
        numbers.append(args.number)
    if args.batch:
        try:
            with open(args.batch, "r") as f:
                batch_nums = [line.strip() for line in f if line.strip()]
                numbers.extend(batch_nums)
            print(f"{Fore.CYAN}[*] Loaded {len(batch_nums)} numbers from {args.batch}{Style.RESET_ALL}")
        except FileNotFoundError:
            print(f"{Fore.RED}[!] File not found: {args.batch}{Style.RESET_ALL}")
            sys.exit(1)

    if not numbers:
        print(f"{Fore.RED}[!] No target specified. Use -n or --batch.{Style.RESET_ALL}")
        parser.print_help()
        sys.exit(1)

    for idx, number in enumerate(numbers, 1):
        if len(numbers) > 1:
            print(f"\n{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}[{idx}/{len(numbers)}] Processing: {number}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}{'='*60}{Style.RESET_ALL}")

        info = PhoneInfo(number, args.country)
        info.display()

        if args.dorks:
            print(f"\n{Fore.CYAN}[*] Generating Google Dorks (type: {args.dorks})...{Style.RESET_ALL}")
            dork_results = generate_dorks(number, args.dorks)
            for source, queries in dork_results.items():
                print(f"\n{Fore.YELLOW}[ {source.upper()} ]{Style.RESET_ALL}")
                for q in queries:
                    print(f"  {Fore.GREEN}→{Style.RESET_ALL} {q}")

        if args.map:
            coords = info.get_coordinates()
            if coords:
                print(f"\n{Fore.CYAN}[*] Approximate Location (country level):{Style.RESET_ALL}")
                print(f"  Lat: {coords[0]}, Lon: {coords[1]}")
                maps_url = f"https://www.google.com/maps?q={coords[0]},{coords[1]}"
                print(f"  Maps: {maps_url}")

        if args.json:
            import json as _json
            export = info.to_dict()
            export["dorks"] = dork_results if args.dorks else {}
            with open(args.json, "w") as f:
                _json.dump(export, f, indent=4)
            print(f"\n{Fore.CYAN}[✓] Results exported to {args.json}{Style.RESET_ALL}")

        print(f"\n{Fore.GREEN}[✓] Scan complete for {number}{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}phoneosint v{__version__} by {__author__}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Remember: Use responsibly. Authorized testing only.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
