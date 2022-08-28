# -*- coding: utf-8 -*-
"""
Convert Sanskrit text to speech

@author: Avinash Varna
"""

import io
from dataclasses import dataclass

from google.cloud.texttospeech import TextToSpeechClient, SsmlVoiceGender
from google.cloud.texttospeech import VoiceSelectionParams, AudioConfig
from google.cloud.texttospeech import AudioEncoding, SynthesisInput

from indic_transliteration import sanscript
from indic_transliteration.sanscript.schemes import VisargaApproximation
from pydub import AudioSegment

from .util import transliterate_text
from .base import TTSBase


default_voice = VoiceSelectionParams(
    language_code="kn-IN", name="kn-IN-Wavenet-A", ssml_gender=SsmlVoiceGender.FEMALE,
)

default_audio_config = AudioConfig(audio_encoding=AudioEncoding.MP3, speaking_rate=0.8)

transliteration_map = {
    "bn-IN": sanscript.BENGALI,
    "gu-IN": sanscript.GUJARATI,
    "hi-IN": sanscript.DEVANAGARI,
    "kn-IN": sanscript.KANNADA,
    "ml-IN": sanscript.MALAYALAM,
    "ta-IN": sanscript.TAMIL,
    "te-IN": sanscript.TELUGU,
}


@dataclass
class GCloudTTS(TTSBase):
    voice: VoiceSelectionParams = default_voice
    audio_config: AudioConfig = default_audio_config
    inter_sentence_duration_ms: int = 100

    def synthesize_sentence(self, sentence: str,) -> AudioSegment:
        """Synthesizes speech from the input string of text.
    
            Adapted from Google sample at:
            https://github.com/googleapis/python-texttospeech/
        """
        client = TextToSpeechClient()
        input_text = SynthesisInput(text=sentence)

        response = client.synthesize_speech(
            request={
                "input": input_text,
                "voice": self.voice,
                "audio_config": self.audio_config,
            }
        )

        audio = AudioSegment.from_file(io.BytesIO(response.audio_content))
        return audio

    def synthesize(
        self, text: str, input_encoding: str = None, visarga_approximation: int = VisargaApproximation.H
    ) -> AudioSegment:
        trans_tgt = transliteration_map[self.voice.language_code]
        text = transliterate_text(
            text,
            input_encoding=input_encoding,
            output_encoding=trans_tgt,
            visarga_approximation=visarga_approximation,
        )
        sentences = text.split(".")

        silence = AudioSegment.silent(self.inter_sentence_duration_ms)
        audios = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence == "":
                continue
            audios.append(self.synthesize_sentence(sentence))
            audios.append(silence)

        return sum(audios)
