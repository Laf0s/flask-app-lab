from flask import request, render_template, redirect, url_for, flash, session, make_response
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

    return render_template(
        "profile.html",
        username=session["username"],
        cookies=request.cookies
    )

@users_bp.route("/logout")
def logout():
    session.pop("username", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("users.login"))

@users_bp.route("/cookie/add", methods=["POST"])
def add_cookie():
    if "username" not in session:
        flash("Дія дозволена лише авторизованим користувачам.", "danger")
        return redirect(url_for("users.login"))

    key = request.form.get("key", "").strip()
    val = request.form.get("val", "").strip()
    max_age = request.form.get("max_age", "").strip()

    if not key:
        flash("Вкажіть ключ куки!", "warning")
        return redirect(url_for("users.profile"))

    try:
        expire_seconds = int(max_age) if max_age else None
    except ValueError:
        expire_seconds = None

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie(key=key, value=val, max_age=expire_seconds)
    flash(f"Куку '{key}' успішно збережено!", "success")
    return resp

@users_bp.route("/cookie/delete-by-key", methods=["POST"])
def delete_cookie_by_key():
    if "username" not in session:
        flash("Дія дозволена лише авторизованим користувачам.", "danger")
        return redirect(url_for("users.login"))

    key = request.form.get("key_to_delete", "").strip()
    if not key:
        flash("Вкажіть ключ куки для видалення!", "warning")
        return redirect(url_for("users.profile"))

    if key not in request.cookies:
        flash(f"Куку з ключем '{key}' не знайдено.", "warning")
        return redirect(url_for("users.profile"))

    resp = make_response(redirect(url_for("users.profile")))
    resp.delete_cookie(key)
    flash(f"Куку '{key}' успішно видалено!", "info")
    return resp

@users_bp.route("/cookie/delete-all", methods=["POST"])
def delete_all_cookies():
    if "username" not in session:
        flash("Дія дозволена лише авторизованим користувачам.", "danger")
        return redirect(url_for("users.login"))

    resp = make_response(redirect(url_for("users.profile")))
    for key in request.cookies:
        if key != "session":
            resp.delete_cookie(key)

    flash("Всі користувацькі кукі видалено!", "info")
    return resp