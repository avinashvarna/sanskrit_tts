"""TTS for sanskrit

#TODO - Usage example
"""

try:
    from ._version import __version__, version
    from ._version import __version_tuple__, version_tuple
except ImportError:
    pass

from .bhashini_tts import BhashiniProxy


def default_tts():
    return BhashiniProxy()
