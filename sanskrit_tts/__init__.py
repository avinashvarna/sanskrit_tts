"""TTS for sanskrit

#TODO - Usage example
"""

from .bhashini_tts import BhashiniProxy


def default_tts():
    return BhashiniProxy()
