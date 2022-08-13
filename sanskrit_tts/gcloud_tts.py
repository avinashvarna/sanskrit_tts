# -*- coding: utf-8 -*-
"""
Convert Sanskrit text to speech

@author: Avinash Varna
"""

import io

from google.cloud.texttospeech import TextToSpeechClient, SsmlVoiceGender
from google.cloud.texttospeech import VoiceSelectionParams, AudioConfig
from google.cloud.texttospeech import AudioEncoding, SynthesisInput

from indic_transliteration import sanscript
from pydub import AudioSegment


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


def adapt_visargas(text: str) -> str:
    replacements = [
        ("aH", "aha"),
        ("AH", "Aha"),
        ("iH", "ihi"),
        ("IH", "Ihi"),
        ("uH", "uhu"),
        ("UH", "Uhu"),
        ("FH", "Fhi"),
        ("eH", "ehe"),
        ("EH", "ehi"),
        ("oH", "oho"),
        ("OH", "Ohu"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def synthesize_sentence(
    sentence: str,
    voice: VoiceSelectionParams = default_voice,
    audio_config: AudioConfig = default_audio_config,
    modify_visargas: bool = True,
) -> AudioSegment:
    """Synthesizes speech from the input string of text.

        Adapted from Google sample at:
        https://github.com/googleapis/python-texttospeech/
    """
    client = TextToSpeechClient()
    trans_tgt = transliteration_map[voice.language_code]
    # text = sanscript.transliterate(sentence, sanscript.DEVANAGARI,
    #                                trans_tgt)
    text = sanscript.transliterate(sentence, sanscript.DEVANAGARI, sanscript.SLP1)
    if modify_visargas:
        text = adapt_visargas(text)
    text = sanscript.transliterate(text, sanscript.SLP1, trans_tgt)
    input_text = SynthesisInput(text=text)

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    audio = AudioSegment.from_file(io.BytesIO(response.audio_content))
    return audio


def synthesize_text(
    text: str,
    voice: VoiceSelectionParams = default_voice,
    audio_config: AudioConfig = default_audio_config,
    inter_sentence_duration_ms: int = 100,
) -> AudioSegment:
    silence = AudioSegment.silent(inter_sentence_duration_ms)
    sentences = text.split("।")

    audios = []
    for sent in sentences:
        sent = sent.strip()
        if sent == "":
            continue
        audios.append(synthesize_sentence(sent, voice, audio_config))
        audios.append(silence)

    return sum(audios)
