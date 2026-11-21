from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, DateTimeLocalField, SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length

CATEGORY_CHOICES = [
    ("news", "Новини"),
    ("publication", "Публікація"),
    ("tech", "Технології"),
    ("other", "Інше")
]


class PostForm(FlaskForm):
    title = StringField(
        "Заголовок",
        validators=[
            DataRequired(message="Заголовок є обов'язковим."),
            Length(min=2, max=150, message="Мінімум 2 символи.")
        ],
        render_kw={"placeholder": "Введіть заголовок поста"}
    )
    content = TextAreaField(
        "Зміст",
        validators=[DataRequired(message="Текст поста не може бути порожнім.")],
        render_kw={"rows": 5, "cols": 40, "placeholder": "Текст публікації..."}
    )
    is_active = BooleanField("Активний пост", default=True)
    publish_date = DateTimeLocalField(
        "Дата публікації",
        format="%Y-%m-%dT%H:%M",
        default=datetime.now
    )
    category = SelectField(
        "Категорія",
        choices=CATEGORY_CHOICES,
        validators=[DataRequired(message="Оберіть категорію.")]
    )
    author_id = SelectField(
        "Автор",
        coerce=int,
        validators=[DataRequired(message="Оберіть автора.")]
    )
    tags = SelectMultipleField(
        "Теги",
        coerce=int,
        render_kw={"size": 4}
    )
    submit = SubmitField("Зберегти пост")