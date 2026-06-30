"""
phoneosint — Advanced OSINT Reconnaissance Tool for Phone Numbers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Author  : CipherZeroo
License : GPL-3.0-or-later
Version : 1.0.0
"""

__author__ = "CipherZeroo"
__version__ = "1.0.0"
__license__ = "GPL-3.0-or-later"
__credits__ = "CipherZeroo — https://github.com/CipherZeroo"

from .core import PhoneInfo
from .scanners import online_lookup
from .dorker import generate_dorks

__all__ = ["PhoneInfo", "online_lookup", "generate_dorks"]
