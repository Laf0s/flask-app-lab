from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_wtf.file import FileField, FileAllowed


class ProductForm(FlaskForm):
    name = StringField('Назва товару', validators=[
        DataRequired(message="Назва товару є обов'язковою"),
        Length(min=3, message="Мінімум 3 символи")
    ], render_kw={"placeholder": "Назва товару"})

    content = TextAreaField('Опис товару', render_kw={"rows": 5, "cols": 40, "placeholder": "Детальний опис товару..."},
                            validators=[
                                DataRequired(message="Опис товару є обов'язковим")
                            ])

    price = DecimalField('Ціна ($)', places=2, validators=[
        DataRequired(message="Вкажіть коректну ціну"),
        NumberRange(min=0.01, message="Ціна має бути додатною")
    ], render_kw={"placeholder": "0.00", "step": "0.01"})

    category = SelectField('Категорія', choices=[
        ('', 'Оберіть категорію...'),
        ('electronics', 'Електроніка'),
        ('computers', 'Комп’ютери та ноутбуки'),
        ('peripherals', 'Периферія та аксесуари'),
        ('books', 'Книги')
    ], validators=[DataRequired(message="Будь ласка, оберіть категорію")])

    quantity = IntegerField('Кількість одиниць', validators=[
        DataRequired(message="Вкажіть кількість одиниць"),
        NumberRange(min=0, message="Кількість не може бути від'ємною")
    ], render_kw={"placeholder": "0"})

    image = FileField('Зображення товару', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Дозволено тільки формати JPG, JPEG та PNG!')
    ])

    submit = SubmitField('Зберегти товар')