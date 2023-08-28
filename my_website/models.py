from flask import session
from passlib.hash import pbkdf2_sha256
import keras_ocr
import matplotlib.pyplot as plt
from io import BytesIO, StringIO
from my_website.module import dbModule
from secret import SALT


class User:
    user_list_ = []
    user_data_ = {}
    user_data_table = "USER_DATA"

    @classmethod
    def sign_in(cls, id, password):
        if id in User.user_data_:
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
        User.insert_userdata(userid, User.user_data_[userid])

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

    @classmethod
    def read_userdata(cls):
        db_class = dbModule.Database()
        sql = f"SELECT * FROM {dbModule.DB_NAME}.{cls.user_data_table}"
        row = db_class.executeAll(sql)
        db_class.db.close()

        key = "user_id_"
        result = {}
        for data in row:
            result[data[key]] = {
                "user_name_": data["user_name_"],
                "user_password_": data["user_password_"],
            }

        User.user_data_ = result

    @classmethod
    def insert_userdata(cls, userid, data):
        db_class = dbModule.Database()
        sql = f"INSERT INTO {dbModule.DB_NAME}.{cls.user_data_table}(user_name_,user_id_, user_password_)\
            VALUES('{data['user_name_']}', '{userid}', '{data['user_password_']}');"
        db_class.execute(sql)
        db_class.commit()
        db_class.db.close()

    @classmethod
    def update_userdata(cls, userid, nickname=None, password=None):
        if nickname is None:
            nickname = cls.user_data_[userid]["user_name_"]
        if password is None:
            password = cls.user_data_[userid]["user_password_"]
        else:
            password = pbkdf2_sha256.hash(password + SALT)

        db_class = dbModule.Database()
        sql = f"UPDATE {dbModule.DB_NAME}.{cls.user_data_table}\
            SET user_name_ =  '{nickname}', user_password_ = '{password}'\
            WHERE user_id_='{userid}'"
        db_class.execute(sql)
        db_class.commit()
        db_class.db.close()

    @classmethod
    def delete_userdata(cls, userid):
        db_class = dbModule.Database()
        sql = f"DELETE {dbModule.DB_NAME}.{cls.user_data_table}\
            WHERE user_id_='{userid}'"
        db_class.execute(sql)
        db_class.commit()
        db_class.db.close()


User.read_userdata()


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
