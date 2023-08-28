from flask import Flask, render_template


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test key"

    # 블루프린트 인스턴스
    from .view import view
    from .auth import auth

    # from .text_detect import textDetect

    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")
    # app.register_blueprint(textDetect, url_prefix="/textDetect")

    return app
