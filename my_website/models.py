from flask import session
from passlib.hash import pbkdf2_sha256
import keras_ocr
import matplotlib.pyplot as plt
from io import BytesIO, StringIO
from secret import SALT


class User:
    user_list_ = []
    user_data_ = {}

    @classmethod
    def sign_in(cls, id, password):
        if id in User.user_list_:
            user_info = User.user_data_[id]

            if cls.check_password(password, user_info["user_password_"]):
                session["user_name_"] = user_info["user_name_"]
                session["user_id_"] = id
                return True
        return False

    @classmethod
    def logout(cls):
        session.clear()

    @classmethod
    def add_user_info(cls, nickname, userid, password):
        User.user_list_.append(userid)
        User.user_data_[userid] = {
            "user_name_": nickname,
            "user_password_": cls.hash_password(password),
        }

    @classmethod
    def dup_check(cls, userid):
        if userid in User.user_list_:
            return True
        return False

    @classmethod
    def hash_password(cls, password):
        return pbkdf2_sha256.hash(password + SALT)

    @classmethod
    def check_password(cls, password, hashed_password):
        check = pbkdf2_sha256.verify(password + SALT, hashed_password)
        return check


# https://frhyme.github.io/python-lib/flask_matplotlib/
class TextDetect:
    pipline = keras_ocr.pipeline.Pipeline()

    @classmethod
    def detect(cls, images=None):
        if images is None:
            images = [keras_ocr.tools.read("my_website/input/test.png")]
        prediction_groups = TextDetect.pipline.recognize(images)
        plt.figure(figsize=(4, 3))
        keras_ocr.tools.drawAnnotations(
            image=images[0], predictions=prediction_groups[0]
        )
        img = BytesIO()
        plt.savefig(img, format="png", dpi=300)
        img.seek(0)
        return img
