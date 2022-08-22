import io
import logging

import requests
from indic_transliteration import sanscript
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

api_url = "http://tts.bhashini.ai/v1/synthesize"


kn_voices = {
  "male_1": 1,
  "female_1": 0,
  "female_2": 2,
}


def synthesize_sentence_kn(text, api_key=None, voice_id="male_1"):
  import sanskrit_tts
  text = sanskrit_tts.get_kannada_text(text=text)
  json_req = {
    "text": text,
    "languageId": "kn",
    "voiceId": kn_voices[voice_id]
  }
  headers = {
    "accept" : "audio/mpeg",
    "X-API-KEY": api_key
  }
  response = requests.post(api_url, json=json_req, headers=headers)
  try:
    audio = AudioSegment.from_file(io.BytesIO(response.content))
  except CouldntDecodeError:
    logging.error(json_req)
    raise 
  return audio
