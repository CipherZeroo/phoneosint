#!/usr/bin/env python3
"""
phoneosint — Core Phone Number Parsing & Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Author  : CipherZeroo
Version : 1.0.0
"""

import phonenumbers
from phonenumbers import carrier, geocoder, timezone, PhoneNumberType
from phonenumbers.phonenumberutil import number_type
from colorama import Fore, Style


AREA_COORDS = {
    "US": (39.8283, -98.5795), "GB": (55.3781, -3.4360),
    "DE": (51.1657, 10.4515), "FR": (46.6034, 1.8883),
    "CA": (56.1304, -106.3468), "AU": (-25.2744, 133.7751),
    "IN": (20.5937, 78.9629), "BR": (-14.2350, -51.9253),
    "JP": (36.2048, 138.2529), "RU": (61.5240, 105.3188),
    "CN": (35.8617, 104.1954), "ZA": (-30.5595, 22.9375),
    "NG": (9.0820, 8.6753), "EG": (26.8206, 30.8025),
    "MX": (23.6345, -102.5528), "IT": (41.8719, 12.5674),
    "ES": (40.4637, -3.7492), "NL": (52.1326, 5.2913),
    "SE": (60.1282, 18.6435), "CH": (46.8182, 8.2275),
    "NO": (60.4720, 8.4689), "FI": (61.9241, 25.7482),
    "DK": (56.2639, 9.5018), "PL": (51.9194, 19.1451),
    "TR": (38.9637, 35.2433), "SA": (23.8859, 45.0792),
    "AE": (23.4241, 53.8478), "SG": (1.3521, 103.8198),
    "HK": (22.3193, 114.1694), "KR": (35.9078, 127.7669),
    "TW": (23.6978, 120.9605), "PH": (12.8797, 121.7740),
    "ID": (-0.7893, 113.9213), "MY": (4.2105, 101.9758),
    "TH": (15.8700, 100.9925), "VN": (14.0583, 108.2772),
    "AR": (-38.4161, -63.6167), "CL": (-35.6751, -71.5430),
    "CO": (4.5709, -74.2973), "PE": (-9.1900, -75.0152),
    "NZ": (-40.9006, 174.8860), "IE": (53.4129, -8.2439),
    "PT": (39.3999, -8.2245), "GR": (39.0742, 21.8243),
    "AT": (47.5162, 14.5501), "BE": (50.5039, 4.4699),
    "HU": (47.1625, 19.5033), "CZ": (49.8175, 15.4730),
    "SK": (48.6690, 19.6990), "RO": (45.9432, 24.9668),
    "BG": (42.7339, 25.4858), "UA": (48.3794, 31.1656),
    "IL": (31.0461, 34.8516), "PK": (30.3753, 69.3451),
    "BD": (23.6850, 90.3563), "KE": (-0.0236, 37.9062),
    "MA": (31.7917, -7.0926), "DZ": (28.0339, 1.6596),
    "TN": (33.8869, 9.5375),
}

LINE_TYPES = {
    PhoneNumberType.FIXED_LINE: "Fixed Line",
    PhoneNumberType.MOBILE: "Mobile",
    PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed Line / Mobile",
    PhoneNumberType.TOLL_FREE: "Toll Free",
    PhoneNumberType.PREMIUM_RATE: "Premium Rate",
    PhoneNumberType.SHARED_COST: "Shared Cost",
    PhoneNumberType.VOIP: "VoIP",
    PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
    PhoneNumberType.PAGER: "Pager",
    PhoneNumberType.UAN: "UAN",
    PhoneNumberType.VOICEMAIL: "Voicemail",
    PhoneNumberType.UNKNOWN: "Unknown",
}


class PhoneInfo:
    """Parse, validate, and display intelligence from an international phone number."""

    def __init__(self, raw_number: str, country_hint: str = None):
        self.raw = raw_number.strip()
        self.country_hint = country_hint
        self.parsed = None
        self.valid = False
        self._parse()

    def _parse(self):
        try:
            if self.country_hint:
                self.parsed = phonenumbers.parse(self.raw, self.country_hint)
            else:
                self.parsed = phonenumbers.parse(self.raw, None)
            self.valid = phonenumbers.is_valid_number(self.parsed)
        except phonenumbers.NumberParseException as e:
            print(f"{Fore.RED}[!] Parse error: {e}{Style.RESET_ALL}")
            self.parsed = None
            self.valid = False

    @property
    def international(self) -> str:
        if self.parsed:
            return phonenumbers.format_number(self.parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        return "N/A"

    @property
    def national(self) -> str:
        if self.parsed:
            return phonenumbers.format_number(self.parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
        return "N/A"

    @property
    def e164(self) -> str:
        if self.parsed:
            return phonenumbers.format_number(self.parsed, phonenumbers.PhoneNumberFormat.E164)
        return "N/A"

    @property
    def country_code(self) -> int:
        return self.parsed.country_code if self.parsed else 0

    @property
    def national_number(self) -> int:
        return self.parsed.national_number if self.parsed else 0

    @property
    def country_name(self) -> str:
        if self.parsed:
            return geocoder.description_for_number(self.parsed, "en") or "Unknown"
        return "Unknown"

    @property
    def country_iso(self) -> str:
        if self.parsed:
            import phonenumbers.phonenumberutil as util
            return util.region_code_for_number(self.parsed) or "??"
        return "??"

    @property
    def carrier_name(self) -> str:
        if self.parsed:
            return carrier.name_for_number(self.parsed, "en") or "Unknown"
        return "Unknown"

    @property
    def line_type_str(self) -> str:
        if self.parsed:
            nt = number_type(self.parsed)
            return LINE_TYPES.get(nt, "Unknown")
        return "Unknown"

    @property
    def timezones(self) -> list:
        if self.parsed:
            return list(timezone.time_zones_for_number(self.parsed))
        return []

    @property
    def is_possible(self) -> bool:
        return phonenumbers.is_possible_number(self.parsed) if self.parsed else False

    def get_coordinates(self):
        iso = self.country_iso
        return AREA_COORDS.get(iso)

    def to_dict(self) -> dict:
        return {
            "raw": self.raw, "e164": self.e164,
            "international": self.international, "national": self.national,
            "valid": self.valid, "possible": self.is_possible,
            "country_code": self.country_code, "country_iso": self.country_iso,
            "country_name": self.country_name, "national_number": self.national_number,
            "carrier": self.carrier_name, "line_type": self.line_type_str,
            "timezones": self.timezones, "coordinates": self.get_coordinates(),
        }

    def display(self):
        print(f"\n{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}📞 Phone Number Intelligence Report{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")

        print(f"{'Raw Input':<25}: {Fore.WHITE}{self.raw}{Style.RESET_ALL}")

        if not self.parsed or not self.valid:
            print(f"{Fore.RED}[!] Invalid phone number — could not parse.{Style.RESET_ALL}")
            return

        status = f"{Fore.GREEN}✓ Valid{Style.RESET_ALL}" if self.valid else f"{Fore.RED}✗ Invalid{Style.RESET_ALL}"
        possible = f"{Fore.GREEN}✓ Yes{Style.RESET_ALL}" if self.is_possible else f"{Fore.RED}✗ No{Style.RESET_ALL}"

        print(f"{'E.164 Format':<25}: {Fore.WHITE}{self.e164}{Style.RESET_ALL}")
        print(f"{'International':<25}: {Fore.WHITE}{self.international}{Style.RESET_ALL}")
        print(f"{'National':<25}: {Fore.WHITE}{self.national}{Style.RESET_ALL}")
        print(f"{'Valid Number':<25}: {status}")
        print(f"{'Possible Number':<25}: {possible}")
        print(f"{'Country Code':<25}: {Fore.YELLOW}+{self.country_code}{Style.RESET_ALL}")
        print(f"{'Country (ISO)':<25}: {Fore.YELLOW}{self.country_name} ({self.country_iso}){Style.RESET_ALL}")
        print(f"{'National Number':<25}: {Fore.WHITE}{self.national_number}{Style.RESET_ALL}")
        print(f"{'Carrier':<25}: {Fore.YELLOW}{self.carrier_name}{Style.RESET_ALL}")
        print(f"{'Line Type':<25}: {Fore.YELLOW}{self.line_type_str}{Style.RESET_ALL}")

        tz_str = ", ".join(self.timezones) if self.timezones else "Unknown"
        print(f"{'Timezones':<25}: {Fore.WHITE}{tz_str}{Style.RESET_ALL}")

        coords = self.get_coordinates()
        if coords:
            print(f"{'Approx. Location':<25}: {Fore.WHITE}Lat {coords[0]:.4f}, Lon {coords[1]:.4f}{Style.RESET_ALL}")
            print(f"{'Google Maps':<25}: {Fore.CYAN}https://www.google.com/maps?q={coords[0]},{coords[1]}{Style.RESET_ALL}")

        print(f"{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
