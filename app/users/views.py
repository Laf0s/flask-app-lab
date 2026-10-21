from flask import request, render_template, redirect, url_for, flash, session
from . import users_bp

USERS_DATA = {
    "user1": "password123",
    "admin": "admin123"
}
@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)

    return render_template("hi.html", name=name, age=age)


@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    return redirect(to_url)

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        return redirect(url_for("users.profile"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username in USERS_DATA and USERS_DATA[username] == password:
            session["username"] = username
            flash("Успішний вхід!", "success")
            return redirect(url_for("users.profile"))
        else:
            flash("Wrong data! Try again!", "danger")
            return redirect(url_for("users.login"))

    return render_template("login.html")

@users_bp.route("/profile")
def profile():
    if "username" not in session:
        flash("Доступ заборонено. Будь ласка, авторизуйтесь.", "danger")
        return redirect(url_for("users.login"))

    return render_template("profile.html", username=session["username"])

@users_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("users.login"))