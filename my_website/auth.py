from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from my_website.models import User

auth = Blueprint("auth", __name__)


@auth.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if "user_name_" in session:
        return redirect(url_for("view.home"))

    id = request.form.get("id")
    password = request.form.get("password1")

    if id is None:
        return render_template("auth/sign-in.html")

    if User.sign_in(id, password):
        return redirect(url_for("view.home"))

    flash("로그인 실패", category="error")
    return render_template("auth/sign-in.html")


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    if "user_name_" in session:
        User.logout()
    return redirect(url_for("view.home"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if "user_name_" in session:
        return redirect(url_for("view.home"))
    if request.method == "POST":
        invitekey = request.form.get("invitekey")
        userid = request.form.get("userid")
        nickname = request.form.get("nickname")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        # 유효성 검사
        if len(userid) < 5:
            flash("id는 5자 이상입니다.", category="error")

        elif len(nickname) < 1:
            flash("이름은 필수입력입니다.", category="error")

        elif password1 != password2:
            flash("비밀번호 불일치", category="error")

        elif len(password1) < 7:
            flash("비밀번호가 너무 짧습니다.", category="error")
        else:
            # 중복 id, 이름 확인
            if User.dup_check(userid):
                flash("이미 가입된 id입니다.", category="error")

            else:
                # create user
                flash("회원가입 완료", category="success")
                User.add_user_info(nickname, userid, password1)
                User.sign_in(userid, password1)
                return redirect(url_for("view.home"))

    return render_template("auth/sign-up.html")
