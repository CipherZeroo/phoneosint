#!/usr/bin/env python3
"""
phoneosint — Google Dork Generator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Author  : CipherZeroo
Version : 1.0.0
"""

from colorama import Fore, Style

DORK_TEMPLATES = {
    "social_networks": [
        'site:facebook.com "{number}"',
        'site:twitter.com "{number}"',
        'site:linkedin.com "{number}"',
        'site:instagram.com "{number}"',
        'site:tiktok.com "{number}"',
        'site:snapchat.com "{number}"',
        'site:reddit.com "{number}"',
        'site:telegram.org "{number}"',
        'site:whatsapp.com "{number}"',
        'site:signal.org "{number}"',
    ],
    "forums": [
        'site:4chan.org "{number}"',
        'site:8kun.top "{number}"',
        'site:boards.net "{number}"',
        'site:phpbb.com "{number}"',
        'inurl:forum "{number}"',
        'inurl:board "{number}"',
    ],
    "classifieds": [
        'site:craigslist.org "{number}"',
        'site:gumtree.com "{number}"',
        'site:kijiji.ca "{number}"',
        'site:olx.com "{number}"',
        'site:ebay.com "{number}"',
        'site:facebook.com/marketplace "{number}"',
    ],
    "pastes": [
        'site:pastebin.com "{number}"',
        'site:paste.ee "{number}"',
        'site:hastebin.com "{number}"',
        'site:ghostbin.com "{number}"',
        'site:rentry.org "{number}"',
        'site:bpaste.net "{number}"',
    ],
    "people_search": [
        'site:whitepages.com "{number}"',
        'site:spokeo.com "{number}"',
        'site:truecaller.com "{number}"',
        'site:peoplefinder.com "{number}"',
        'site:pipl.com "{number}"',
        'site:411.com "{number}"',
    ],
    "phone_directories": [
        'site:telstra.com.au/phone-directory "{number}"',
        'site:dasoertliche.de "{number}"',
        'site:pagesjaunes.fr "{number}"',
        'site:paginebianche.it "{number}"',
        'site:infobel.com "{number}"',
        'site:qname.com "{number}"',
        'tel +{number}',
        'phone +{number}',
    ],
    "reputation": [
        'site:800notes.com "{number}"',
        'site:whocallsme.com "{number}"',
        'site:who-called.co.uk "{number}"',
        'site:spamcalls.net "{number}"',
        'site:callercenter.com "{number}"',
        'site:callfilter.app "{number}"',
        '"{number}" scam OR spam OR fraud',
    ],
}


def generate_dorks(number: str, dork_type: str = "all") -> dict:
    clean = number.lstrip("+").replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

    results = {}

    if dork_type == "all":
        categories = list(DORK_TEMPLATES.keys())
    else:
        categories = [dork_type] if dork_type in DORK_TEMPLATES else []

    for cat in categories:
        templates = DORK_TEMPLATES.get(cat, [])
        queries = []
        for tpl in templates:
            variants = [
                tpl.format(number=number),
                tpl.format(number=clean),
            ]
            queries.extend(variants)
        results[cat] = queries

    return results
