import urllib.parse
import re
import sys

# Patch re.sre_parse which was moved to re._parser in Python 3.11+
try:
    from re import sre_parse
except ImportError:
    import re._parser
    re.sre_parse = re._parser
    sys.modules['re.sre_parse'] = re._parser

def safe_urlparse(url):
    try:
        return urllib.parse._urlparse(url)
    except Exception:
        return urllib.parse._urlparse("http://invalid")

# Save original function
urllib.parse._urlparse = urllib.parse.urlparse
urllib.parse.urlparse = safe_urlparse

# Now import lk21 AFTER monkey patch
import lk21
