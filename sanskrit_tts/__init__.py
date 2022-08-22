import regex
from indic_transliteration import sanscript
from pydub import AudioSegment
from tqdm import tqdm


def synthesize_text(
    text: str,
    synthesizer,
    separator_pattern: str = "[।॥.]|\n+",
    inter_sentence_duration_ms: int = 100, *args, **kwargs
) -> AudioSegment:
  silence = AudioSegment.silent(inter_sentence_duration_ms)
  sentences = regex.split(separator_pattern, text)

  audios = []
  for sent in tqdm(sentences):
    sent = sent.strip()
    if sent == "":
      continue
    audios.append(synthesizer(sent, *args, **kwargs))
    audios.append(silence)

  return sum(audios)


def get_kannada_text(text):
  text = sanscript.transliterate(text, _to=sanscript.KANNADA)
  text = sanscript.SCHEMES[sanscript.KANNADA].force_lazy_anusvaara(text)
  return text