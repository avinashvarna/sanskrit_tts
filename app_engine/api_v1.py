# -*- coding: utf-8 -*-
# import logging
import os

from flask import Blueprint, make_response
from flask_restx import Resource, Api, reqparse

from indic_transliteration import sanscript
from indic_transliteration.sanscript.schemes import VisargaApproximation

import sanskrit_tts
from sanskrit_tts.bhashini_tts import BhashiniTTS, BhashiniVoice


URL_PREFIX = "/v1"
api_blueprint = Blueprint("sanskrit_tts", __name__)

api = Api(
    app=api_blueprint,
    version="1.0",
    title="sanskrit_tts API",
    description='For detailed intro and to report issues: see <a href="https://github.com/avinashvarna/sanskrit_tts">here</a>. '
    'A list of REST and non-REST API routes avalilable on this server: <a href="../sitemap">sitemap</a>.',
    default_label=api_blueprint.name,
    prefix=URL_PREFIX,
    doc="/docs",
)


api_key = None
if "BHASHINI_API_KEY" in os.environ:
    api_key = os.environ["BHASHINI_API_KEY"]
else:
    # Get it from the datastore
    from google.cloud import datastore
    client = datastore.Client()
    kind = 'api_key'
    name = 'bhashini_api_key'
    key = client.key(kind, name)
    entity = client.get(key)
    api_key = entity["api_key"]
if api_key is None:
    raise Exception("Bhashini API key not found")


@api.route("/version/")
class Version(Resource):
    """sanskrit_tts Library Version"""
    def get(self):
        """sanskrit_tts Library Version"""
        response = {"version": str(sanskrit_tts.__version__)}
        return response


synthesize_parser = reqparse.RequestParser()
synthesize_parser.add_argument(
    "text", type=str, required=True, help="The text to be synthesized"
)
synthesize_parser.add_argument(
    "input_encoding",
    type=str,
    default=None,
    help="Encoding of the text",
    choices=list(sanscript.SCHEMES.keys()) + [None],
)
synthesize_parser.add_argument(
    "voice",
    type=int,
    default=2,
    help="The voice to use",
    choices=[x.value for x in BhashiniVoice.__members__.values()],
)
synthesize_parser.add_argument(
    "visarga_approximation",
    type=int,
    default=0,
    help="Visarga approximation to use",
    choices=[x.value for x in VisargaApproximation.__members__.values()],
)


@api.route("/synthesize/")
# @api.response(200, ['audio/mpeg'])
@api.produces("audio/mpeg")
@api.expect(synthesize_parser, validate=True)
class Synthesize(Resource):
    """Synthesis handler"""

    def post(self):
        """Handle POST"""
        args = synthesize_parser.parse_args()
        tts = BhashiniTTS(
            voice=BhashiniVoice(args.voice),
            api_key=api_key,
        )
        tts_response = tts._synthesis_response(
            args.text, args.input_encoding, args.visarga_approximation
        )
        response = make_response(tts_response.content)
        response.headers.set("Content-Type", "audio/mpeg")
        return response
