# -*- coding: utf-8 -*-
import logging
import os
from base64 import b64encode

import flask
import jsonpickle
from flask_cors import CORS
import api_v1


app = flask.Flask(__name__)

# Let Javascsipt hosted elsewhere access our API.
CORS(
    app=app,
    # injects the `Access-Control-Allow-Credentials` header in responses. This allows cookies and credentials to be submitted across domains.
    supports_credentials=True,
)
logging.info(str(app))

app.config.update(
    DEBUG=True,
    # Used to encrypt session cookies.
    SECRET_KEY=b64encode(os.urandom(24)).decode("utf-8"),
)

app.register_blueprint(api_v1.api_blueprint)

# TODO
@app.route("/")
def index():
    flask.session["logstatus"] = 1
    return "Welcome"  # flask.redirect('')


# Cant use flask-sitemap - won't list flask restplus routes.
@app.route("/sitemap")
def site_map():
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ",".join(rule.methods)
        url = str(rule)
        import urllib.request

        line = urllib.request.unquote(
            "{:50s} {:20s} {}".format(rule.endpoint, methods, url)
        )
        output.append(line)

    logging.info(str(output))
    response = app.response_class(
        response=jsonpickle.dumps(output), status=200, mimetype="application/json"
    )
    return response


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
