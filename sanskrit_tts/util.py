# -*- coding: utf-8 -*-
"""
Common utilities for TTS

"""
from indic_transliteration import sanscript
from indic_transliteration.sanscript.schemes import VisargaApproximation



def transliterate_text(
    text: str,
    input_encoding: str = None,
    output_encoding: str = sanscript.KANNADA,
    visarga_approximation: int = VisargaApproximation.H,
) -> str:
    """Transliterate input text modifying visargas if necessary

    Parameters
    ----------
    text : str
        input text
    input_encoding : str, optional
        encoding of input text, by default None. Will be auto-detected if None
    output_encoding : str, optional
        encoding of output, by default sanscript.KANNADA
    visarga_approximation : int, optional
        adapt visargas for pronunciation, by default - replacement with h

    Returns
    -------
    str
        transliterated text
        
    See also
    --------
    adapt_visargas
    """
    text = sanscript.transliterate(text, _from=input_encoding, _to=output_encoding)
    if visarga_approximation is not None:
        text = sanscript.SCHEMES[output_encoding].approximate_visargas(text, mode=visarga_approximation)
    if output_encoding not in [sanscript.DEVANAGARI]:
        text = sanscript.SCHEMES[output_encoding].force_lazy_anusvaara(text)
    return text
