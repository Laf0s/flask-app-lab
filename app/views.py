import logging
from flask import request, redirect, url_for, render_template, flash
from app import app
from .forms import ContactForm

logger = logging.getLogger("contact_logger")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("contact_messages.log", encoding="utf-8")
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
file_handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(file_handler)

@app.route('/')
def resume() -> str:
    return render_template('resume.html', title="Резюме | Андрій Яцишин")

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = dict(form.subject.choices).get(form.subject.data, form.subject.data)
        message = form.message.data

        logger.info(
            f"Нове повідомлення: Ім'я='{name}', Email='{email}', Phone='{phone}', Тема='{subject}', Повідомлення='{message}'"
        )

        flash("Ваше повідомлення успішно надіслано та збережено!", "success")
        return redirect(url_for('contacts'))

    elif request.method == 'POST':
        flash("Помилка під час відправки форми. Перевірте введені дані.", "danger")

    return render_template('contacts.html', title="Контакти | Андрій Яцишин", form=form)

@app.route('/homepage')
def home():
    agent = request.user_agent
    return render_template("homepage.html", agent=agent)