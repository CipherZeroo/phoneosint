#!/usr/bin/env python3
"""
phoneosint — Online Scanner Modules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Author  : CipherZeroo
Version : 1.0.0
"""

import requests
from colorama import Fore, Style


def online_lookup(
    number: str = None,
    numverify_key: str = None,
    twilio_sid: str = None,
    twilio_token: str = None,
) -> dict:
    results = {}

    if numverify_key and number:
        try:
            resp = requests.get(
                "http://apilayer.net/api/validate",
                params={"access_key": numverify_key, "number": number},
                timeout=15,
            )
            data = resp.json()
            if data.get("valid"):
                results["numverify"] = data
                print(f"  {Fore.GREEN}[NumVerify]{Style.RESET_ALL}")
                print(f"    Carrier  : {data.get('carrier', 'N/A')}")
                print(f"    Line Type: {data.get('line_type', 'N/A')}")
                print(f"    Location : {data.get('location', 'N/A')}")
            else:
                print(f"  {Fore.YELLOW}[NumVerify] Number invalid or API limit reached.{Style.RESET_ALL}")
        except Exception as e:
            print(f"  {Fore.RED}[NumVerify] Error: {e}{Style.RESET_ALL}")

    if twilio_sid and twilio_token and number:
        try:
            from twilio.rest import Client
            client = Client(twilio_sid, twilio_token)
            lookup = client.lookups.v2.phone_numbers(number).fetch(
                fields=["caller_name", "line_type_intelligence", "sms_pumping_risk"]
            )
            results["twilio"] = lookup.__dict__
            print(f"  {Fore.GREEN}[Twilio]{Style.RESET_ALL}")
            print(f"    Caller Name: {getattr(lookup, 'caller_name', {}).get('caller_name', 'N/A')}")
            print(f"    Line Type  : {getattr(lookup, 'line_type_intelligence', {}).get('type', 'N/A')}")
            print(f"    SIM Swap   : {getattr(lookup, 'sms_pumping_risk', {}).get('sms_pumping_risk_score', 'N/A')}")
        except ImportError:
            print(f"  {Fore.YELLOW}[Twilio] twilio package not installed. Run: pip3 install twilio{Style.RESET_ALL}")
        except Exception as e:
            print(f"  {Fore.RED}[Twilio] Error: {e}{Style.RESET_ALL}")

    return results
