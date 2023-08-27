from flask import Blueprint, send_file, render_template, make_response
from my_website.models import TextDetect

from functools import wraps, update_wrapper
from datetime import datetime


textDetect = Blueprint("textDetect", __name__)


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Last-Modified"] = datetime.now()
        response.headers[
            "Cache-Control"
        ] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "-1"
        return response

    return update_wrapper(no_cache, view)


@textDetect.route("/fig")
@nocache
def fig():
    # img 읽어오기

    # text detect
    img = TextDetect.detect()
    return send_file(img, mimetype="image/png")


@textDetect.route("/detect")
@nocache
def detect():
    return render_template("detect.html", width=800, height=600)
