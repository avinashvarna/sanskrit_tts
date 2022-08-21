# -*- coding: utf-8 -*-

import abc
from pydub import AudioSegment


class TTSBase(abc.ABC):
    """Base class for TTS
    """

    @abc.abstractmethod
    def synthesize(
        self, text: str, input_encoding: str = None, modify_visargas: bool = True
    ) -> AudioSegment:
        """Synthesize the provided text using TTS and return the audio

        Parameters
        ----------
        text : str
            input text to be synthesized
        input_encoding : str, optional
            encoding of input text, by default None. Will be auto-detected if None
        modify_visargas : bool, optional
            adapt visargas for pronunciation, by default True

        Returns
        -------
        AudioSegment
            Synthesized audio
        """
        pass
