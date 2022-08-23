# -*- coding: utf-8 -*-
"""
TTS Client for Bhashini API https://tts.bhashini.ai/

"""
import logging
from urllib import response
from urllib.error import HTTPError

import requests
import io

from dataclasses import dataclass
from enum import IntEnum
from pydub import AudioSegment

from .util import transliterate_text
from .base import TTSBase


class BhashiniVoice(IntEnum):
    FEMALE1 = 0
    MALE1 = 1
    FEMALE2 = 2


@dataclass
class BhashiniTTS(TTSBase):
    url: str = "https://tts.bhashini.ai/v1/synthesize"
    voice: BhashiniVoice = BhashiniVoice.FEMALE2
    api_key: str = None

    def synthesize(
        self, text: str, input_encoding: str = None, modify_visargas: bool = True
    ) -> AudioSegment:
        response = self._synthesis_response(text, input_encoding, modify_visargas)
        audio = AudioSegment.from_file(io.BytesIO(response.content))
        return audio
    
    def _synthesis_response(
        self, text: str, input_encoding: str = None, modify_visargas: bool = True
    ):
        text = transliterate_text(
            text, input_encoding=input_encoding, modify_visargas=modify_visargas
        )
        headers = {"accept": "audio/mpeg"}
        if self.api_key is not None:
            headers["X-API-KEY"] = self.api_key
        data = {"languageId": "kn", "voiceId": self.voice.value, "text": text}
        try:
            response = requests.post(self.url, headers=headers, json=data)
            response.raise_for_status()
        except Exception as e:
            logging.info(data)
            raise
        return response


@dataclass
class BhashiniProxy(TTSBase):
    url: str = "https://sanskrit-tts-306817.appspot.com/v1/synthesize/"
    voice: BhashiniVoice = BhashiniVoice.FEMALE2
    
    def synthesize(
        self, text: str, input_encoding: str = None, modify_visargas: bool = True
    ) -> AudioSegment:
        data = {
            "text": text,
            "input_encoding": input_encoding,
            "voice": self.voice.value,
            "modify_visargas": modify_visargas
        }
        response = requests.post(self.url, json=data)
        response.raise_for_status()
        audio = AudioSegment.from_file(io.BytesIO(response.content))
        return audio
    