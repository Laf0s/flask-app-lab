from flask import render_template, redirect, url_for, flash, request
from app import db
from app.users.models import User
from . import post_bp
from .models import Post
from .forms import PostForm


@post_bp.route("", strict_slashes=False)
def list_posts():
    stmt = (
        db.select(Post)
        .where(Post.is_active.is_(True))
        .order_by(Post.posted.desc())
    )
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)


@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    authors = db.session.scalars(db.select(User).order_by(User.id)).all()
    form.author_id.choices = [(author.id, author.username) for author in authors]

    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data.strip(),
            content=form.content.data.strip(),
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            category=form.category.data,
            user_id=form.author_id.data
        )
        db.session.add(new_post)
        db.session.commit()
        flash("Пост успішно створено!", "success")
        return redirect(url_for("posts.list_posts"))
    elif request.method == "POST":
        flash("Помилка валідації. Перевірте заповнені поля.", "danger")

    return render_template("add_post.html", form=form, title="Створити новий пост")


@post_bp.route("/<int:id>")
def detail_post(id: int):
    post = db.get_or_404(Post, id)
    return render_template("detail_post.html", post=post)


@post_bp.route("/<int:id>/update", methods=["GET", "POST"])
def update_post(id: int):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)
    authors = db.session.scalars(db.select(User).order_by(User.id)).all()
    form.author_id.choices = [(author.id, author.username) for author in authors]

    if request.method == "GET":
        form.publish_date.data = post.posted
        form.author_id.data = post.user_id

    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.content = form.content.data.strip()
        post.is_active = form.is_active.data
        post.category = form.category.data
        post.user_id = form.author_id.data
        if form.publish_date.data:
            post.posted = form.publish_date.data
        db.session.commit()
        flash("Пост оновлено!", "success")
        return redirect(url_for("posts.detail_post", id=post.id))
    elif request.method == "POST":
        flash("Помилка при оновленні поста.", "danger")

    return render_template("add_post.html", form=form, title="Редагувати пост")


@post_bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id: int):
    post = db.get_or_404(Post, id)
    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Пост видалено!", "warning")
        return redirect(url_for("posts.list_posts"))

    return render_template("delete_confirm.html", post=post)