from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from app import db
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Це поле є обов'язковим."),
            Length(min=4, max=16, message="Довжина повинна бути від 4 до 16 символів."),
            Regexp(
                r"^[A-Za-z][A-Za-z0-9_.]*$",
                message="Username must start with a letter and contain only letters, numbers, dots or underscores."
            ),
        ],
        render_kw={"placeholder": "Username"}
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Це поле є обов'язковим."),
            Email(message="Некоректний формат електронної пошти."),
        ],
        render_kw={"placeholder": "name@example.com"}
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Це поле є обов'язковим."),
            Length(min=6, message="Пароль повинен містити щонайменше 6 символів."),
        ],
        render_kw={"placeholder": "Password"}
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Підтвердіть пароль."),
            EqualTo("password", message="Паролі не збігаються."),
        ],
        render_kw={"placeholder": "Confirm Password"}
    )
    submit = SubmitField("Register")

    def validate_username(self, field):
        existing_user = db.session.scalar(
            db.select(User).where(User.username == field.data.strip())
        )
        if existing_user:
            raise ValidationError(f"Користувач з іменем {field.data} вже існує.")

    def validate_email(self, field):
        existing_user = db.session.scalar(
            db.select(User).where(User.email == field.data.strip().lower())
        )
        if existing_user:
            raise ValidationError(f"Користувач з таким емейлом {field.data} вже існує.")


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Введіть електронну пошту."),
            Email(message="Некоректний формат електронної пошти."),
        ],
        render_kw={"placeholder": "name@example.com"}
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(message="Введіть пароль.")],
        render_kw={"placeholder": "Password"}
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")