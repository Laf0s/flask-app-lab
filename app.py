from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def resume() -> str:
    return render_template('resume.html', title='Резюме | Андрій Яцишин')

@app.route('/contacts')
def contacts() -> str:
    return render_template('contacts.html', title='Контакти | Андрій Яцишин')

if __name__ == '__main__':
    app.run(debug=True)