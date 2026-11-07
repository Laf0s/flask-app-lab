from flask import render_template, abort, redirect, url_for, flash, request
from . import products_bp
from app.forms import ProductForm
from .repository import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product
)

@products_bp.route("/")
def list_products():
    items = get_all_products()
    return render_template("products.html", products=items)


@products_bp.route("/<int:product_id>")
def detail_product(product_id: int):
    product = get_product_by_id(product_id)
    if product is None:
        abort(404)
    return render_template("detail_product.html", product=product)


@products_bp.route("/add", methods=["GET", "POST"])
def add_product_view():
    form = ProductForm()
    if form.validate_on_submit():
        create_product(form.data, form.image.data)
        flash(f"Товар '{form.name.data}' успішно додано!", "success")
        return redirect(url_for("products.list_products"))
    elif request.method == "POST":
        flash("Помилка додавання товару. Перевірте введені дані.", "danger")

    return render_template("product_form.html", form=form, title="Додати новий товар")


@products_bp.route("/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product_view(product_id: int):
    product = get_product_by_id(product_id)
    if product is None:
        abort(404)

    form = ProductForm(data=product)
    if form.validate_on_submit():
        success = update_product(product_id, form.data, form.image.data)
        if success:
            flash(f"Товар '{form.name.data}' успішно оновлено!", "success")
            return redirect(url_for("products.detail_product", product_id=product_id))
        else:
            flash("Не вдалося оновити товар.", "danger")
    elif request.method == "POST":
        flash("Помилка редагування. Перевірте правильність заповнення форми.", "danger")

    return render_template(
        "product_form.html",
        form=form,
        product=product,
        title=f"Редагування: {product['name']}"
    )


@products_bp.route("/<int:product_id>/delete", methods=["POST"])
def delete_product_view(product_id: int):
    success = delete_product(product_id)
    if success:
        flash("Товар успішно видалено!", "warning")
    else:
        flash("Товар не знайдено або не вдалося видалити.", "danger")
    return redirect(url_for("products.list_products"))