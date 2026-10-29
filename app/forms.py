from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

class ContactForm(FlaskForm):
    name = StringField(
        "Ім'я",
        validators=[
            DataRequired(message="Це поле є обов'язковим."),
            Length(min=4, max=10, message="Довжина імені повинна бути від 4 до 10 символів.")
        ],
        render_kw={"placeholder": "Ваше ім'я"}
    )
    email = StringField(
        "Електронна пошта",
        validators=[
            DataRequired(message="Це поле є обов'язковим."),
            Email(message="Некоректний формат електронної пошти.")
        ],
        render_kw={"placeholder": "name@example.com"}
    )
    phone = StringField(
        "Номер телефону",
        validators=[
            DataRequired(message="Це поле є обов'язковим."),
            Regexp(r"^\+380\d{9}$", message="Формат телефону повинен бути: +380XXXXXXXXX")
        ],
        render_kw={"placeholder": "+380XXXXXXXXX"}
    )
    subject = SelectField(
        "Тема повідомлення",
        choices=[
            ("", "Оберіть тему..."),
            ("cooperation", "Співпраця"),
            ("support", "Технічна підтримка"),
            ("feedback", "Відгук або пропозиція"),
            ("other", "Інше")
        ],
        validators=[DataRequired(message="Будь ласка, оберіть тему.")]
    )
    message = TextAreaField(
        "Повідомлення",
        validators=[
            DataRequired(message="Це поле є обов'язковим."),
            Length(max=500, message="Повідомлення не може перевищувати 500 символів.")
        ],
        render_kw={"placeholder": "Текст повідомлення...", "rows": 4}
    )
    submit = SubmitField("Надіслати")