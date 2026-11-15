from flask import render_template, redirect, url_for, flash, request, session
from app import db
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
    if form.validate_on_submit():
        author_name = session.get("username") or "Anonymous"
        new_post = Post(
            title=form.title.data.strip(),
            content=form.content.data.strip(),
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            category=form.category.data,
            author=author_name
        )
        db.session.add(new_post)
        db.session.commit()
        flash(f"Пост успішно створено! Автор: {author_name}.", "success")
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

    if request.method == "GET":
        form.publish_date.data = post.posted

    if form.validate_on_submit():
        form.populate_obj(post)
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