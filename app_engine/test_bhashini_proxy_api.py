""" Test Bhashini Proxy API"""
from io import BytesIO

from indic_transliteration.sanscript.schemes import VisargaApproximation
from pydub import AudioSegment

from sanskrit_tts.bhashini_tts import BhashiniVoice
from main import app


def test_bhashini_proxy_api():
    """ Test Bhashini Proxy API"""
    text = "कालिदासस्य जीवनवृत्तिविषये अनेकाः लोकविश्रुतयः अनेके वादाः च सन्ति ।"
    client = app.test_client()
    url = "/v1/synthesize/"
    data = {
        "text": text,
        "input_encoding": None,
        "voice": int(BhashiniVoice.FEMALE2),
        "visarga_approximation": int(VisargaApproximation.AHA),
    }
    test_response = client.post(url, json=data)
    assert "Content-Type" in test_response.headers
    assert test_response.headers["Content-Type"] == "audio/mpeg"
    response = test_response.data
    audio = AudioSegment.from_file(BytesIO(response))
    audio.export("proxy.mp3")


if __name__ == "__main__":
    test_bhashini_proxy_api()
