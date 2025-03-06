"""
Strangeloop - A recursive and self-referential AI agent framework.
"""

from importlib.metadata import version

try:
    __version__ = version("strangeloop")
except Exception:
    pass

# Import capabilities if they exist
try:
    from .capabilities import *
except ImportError:
    pass
