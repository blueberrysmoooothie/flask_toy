from flask import Blueprint, render_template, session


view = Blueprint("view", __name__)


@view.route("/")
def home():
    return render_template(
        "home.html",
        username=session["user_name_"] if "user_name_" in session else None,
    )
