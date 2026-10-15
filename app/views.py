from flask import request, redirect, url_for, render_template, abort
from app import app


@app.route('/')
def resume() -> str:
    return render_template('resume.html', title="Резюме | Андрій Яцишин")

@app.route('/contacts')
def contacts() -> str:
    return render_template('contacts.html', title="Контакти | Андрій Яцишин")

@app.route('/homepage')
def home():
    agent = request.user_agent
    return render_template("homepage.html", agent=agent)