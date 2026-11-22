from flask import request, render_template, redirect, url_for, flash, make_response
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from . import users_bp
from .models import User
from .forms import RegistrationForm, LoginForm

@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("hi.html", name=name, age=age)


@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    return redirect(to_url)


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
            password=""
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {user.username}!", "success")
        return redirect(url_for("users.login"))

    return render_template("register.html", form=form, title="Register")


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data
        user = db.session.scalar(db.select(User).where(User.email == email))

        if user and user.check_password(password):
            login_user(user, remember=form.remember.data)
            flash("You logged in successfully!", "success")
            return redirect(url_for("users.account"))
        else:
            flash("Невірний email або пароль! Спробуйте ще раз.", "danger")

    return render_template("login.html", form=form, title="Login")


@users_bp.route("/account")
@login_required
def account():
    return render_template("account.html", user=current_user)


@users_bp.route("/list")
@login_required
def users_list():
    users = db.session.scalars(db.select(User).order_by(User.id)).all()
    return render_template("users_list.html", users=users)


@users_bp.route("/profile")
@login_required
def profile():
    current_theme = request.cookies.get("profile_theme", "light")
    return render_template(
        "profile.html",
        username=current_user.username,
        cookies=request.cookies,
        theme=current_theme
    )

@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out.", "info")
    return redirect(url_for("users.login"))

@users_bp.route("/cookie/add", methods=["POST"])
@login_required
def add_cookie():
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
@login_required
def delete_cookie_by_key():
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
@login_required
def delete_all_cookies():
    resp = make_response(redirect(url_for("users.profile")))
    for key in request.cookies:
        if key not in ("session", "remember_token"):
            resp.delete_cookie(key)

    flash("Всі користувацькі кукі видалено!", "info")
    return resp

@users_bp.route("/theme/<string:theme_name>")
@login_required
def set_theme(theme_name):
    allowed_themes = ["light", "dark"]
    selected = theme_name if theme_name in allowed_themes else "light"

    resp = make_response(redirect(url_for("users.profile")))
    resp.set_cookie("profile_theme", selected, max_age=60 * 60 * 24 * 30)
    flash(f"Колірну схему змінено на: {selected}", "secondary")
    return resp