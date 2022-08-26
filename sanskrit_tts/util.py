# -*- coding: utf-8 -*-
"""
Common utilities for TTS

"""
from indic_transliteration import sanscript
from indic_transliteration.sanscript.schemes import VisargaApproximation


def adapt_visargas(text: str) -> str:
    """Replace visargas with the corresponding variant of h based on common pronunciation patterns

    Parameters
    ----------
    text : str
        input text

    Returns
    -------
    str
        text with visargas adapted for pronunciation
    """
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
    visarga_approximation : bool, optional
        adapt visargas for pronunciation, by default True

    Returns
    -------
    str
        transliterated text
        
    See also
    --------
    adapt_visargas
    """
    if visarga_approximation == VisargaApproximation.AHA:
        text = sanscript.transliterate(text, input_encoding, sanscript.SLP1)
        text = adapt_visargas(text)
        text = sanscript.transliterate(text, sanscript.SLP1, output_encoding)
    else:
        text = sanscript.transliterate(text, _from=input_encoding, _to=output_encoding)
        if visarga_approximation not in [VisargaApproximation.H, None]:
            text = sanscript.SCHEMES[output_encoding].approximate_visargas(text, mode=visarga_approximation)
    if output_encoding not in [sanscript.DEVANAGARI]:
        text = sanscript.SCHEMES[output_encoding].force_lazy_anusvaara(text)
    return text
