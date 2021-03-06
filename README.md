# sanskrit_tts

A simple python library for converting Sanskrit text to speech.

## Pre-requisites
Currently, the only supported method is to use Google Cloud text to speech with a workaround ([see details below](#how-it-works)). A Google Cloud account with text-to-speech API enabled is required. Instructions for enabling the API and setting up application credentials are described [here](https://cloud.google.com/text-to-speech/docs/quickstart-client-libraries#client-libraries-install-python). Please follow these steps before using this library.

Note that the TTS API will incur a cost if the free quota is exceeded ([details](https://cloud.google.com/text-to-speech/pricing)). The library uses a wavenet voice by default, but this can be changed via the `voice` parameter to [`synthesize_text`](https://github.com/avinashvarna/sanskrit_tts/blob/main/sanskrit_tts/gcloud_tts.py#L56).

## Installation
This package has been developed on python 3.8 but should work with any version of python >= 3.6.
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
See the [example notebook](https://github.com/avinashvarna/sanskrit_tts/blob/main/examples/simple_example.ipynb) for a simple example of converting text from Sanskrit Wikipedia to the corresponding audio.

## How it works
Google Text-to-Speech does not support Sanskrit yet. As a workaround, this library uses other languages for speech to text conversion. Kannada is used by default for this workaround. Any other language/voice supported by Google TTS API can be used by changing the `voice` parameter to [`synthesize_text`](https://github.com/avinashvarna/sanskrit_tts/blob/main/sanskrit_tts/gcloud_tts.py#L56), and the results will vary. A complete list of voices is available [here](https://cloud.google.com/text-to-speech/docs/voices).
