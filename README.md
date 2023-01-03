# sanskrit_tts

A simple python library for converting Sanskrit Text-to-Speech (TTS). The supported TTS engines are:

  1. [Google Cloud TTS](https://cloud.google.com/text-to-speech/)
  2. [Bhashini AI TTS](https://tts.bhashini.ai/)

Both of these API options require authentication, in the form of Google cloud credentials, or Bhashini API key. The developers of Bhashini have generously provided an API key for non-commercial, limited usage of the API for creating audio of Sanskrit texts. This can be used via the bhashini proxy (see [Usage](#usage) below). Please note that the Bhashini proxy (the default option) should not be used for other purposes.

## Installation
This package uses `pydub` for managing audio data, which in turn requires `ffmpeg` or `libav`. Please check the details (here)[https://github.com/jiaaro/pydub#dependencies].

This package should work with any version of python >= 3.8.
```bash
pip install sanskrit_tts
```
To install from the master branch of the git repo:
```bash
pip install git+https://github.com/avinashvarna/sanskrit_tts.git
```
For an editable installation (to modify the code and experiment)
```bash
git clone https://github.com/avinashvarna/sanskrit_tts.git
cd sanskrit_tts
pip install -e .
```

## Usage

All TTS classes expose the same interface, so that switching should be fairly easy.

### Default - Bhashini proxy with embedded API key
```python
from sanskrit_tts import default_tts

text = "तैत्तिरीयोपनिषत् प्रसिद्धासु दशसु उपनिषत्सु अन्यतमा ।"
TTS = default_tts()
audio = TTS.synthesize(text)
# Export the audio as an MP3
audio.export("sanskrit_speech.mp3")
```

### Bhashini API with key
```python
from sanskrit_tts.bhashini_tts import BhashiniTTS

text = "तैत्तिरीयोपनिषत् प्रसिद्धासु दशसु उपनिषत्सु अन्यतमा ।"
api_key = ...
TTS = BhashiniTTS(api_key=api_key)
audio = TTS.synthesize(text)
# Export the audio as an MP3
audio.export("sanskrit_speech.mp3")
```

### Google Cloud
Requires credentials, e.g. from a (service account)[https://cloud.google.com/iam/docs/creating-managing-service-accounts].
```python
import os
from sanskrit_tts.gcloud_tts import GCloudTTS

# Setup credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './credentials.json'

text = "तैत्तिरीयोपनिषत् प्रसिद्धासु दशसु उपनिषत्सु अन्यतमा ।"
TTS = GCloudTTS()
audio = TTS.synthesize(text)
# Export the audio as an MP3
audio.export("sanskrit_speech.mp3")
```

See the [example notebook](https://github.com/avinashvarna/sanskrit_tts/blob/main/examples/simple_example.ipynb) for a simple example of converting text from Sanskrit Wikipedia to the corresponding audio.

## How it works
Both Google Cloud TTS and Bhashini Text-to-Speech do not support Sanskrit yet. As a workaround, this library uses other languages for speech to text conversion. Kannada is used by default for this workaround. Any other language/voice supported by the corresponding TTS API can be used by changing the appropriate parameters while instantiating the TTS class, and the results will vary. A complete list of voices supported by Google Cloud TTS is available [here](https://cloud.google.com/text-to-speech/docs/voices). For Bhashini, please check the (demo)[https://tts.bhashini.ai/demo/].
