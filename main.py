from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from os import listdir
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/<title>')
def index(title):
    return render_template('base.html', title=title)


@app.route('/galery', methods=['POST', 'GET'])
def galery():
    images = listdir('static/img')
    if request.method == 'POST':
        file = request.files['file']
        file.save('static/img/' + file.filename)
    return render_template('carousel.html', images=images)


@app.route('/list_prof/<list>')
def list_prof(list):
    return render_template('list-template.html', list=list)


class LoginForm(FlaskForm):
    id = StringField('id асторонавта', validators=[DataRequired()])
    password = PasswordField('Пароль астронавта', validators=[DataRequired()])
    id_cap = StringField('id капитана', validators=[DataRequired()])
    password_cap = PasswordField('Пароль капитана', validators=[DataRequired()])

    submit = SubmitField('Доступ')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/auto_answer')
@app.route('/answer')
def auto_ans():
    surname = 'Watny'
    name = 'Mark'
    education = 'выше среднего'
    prof = 'штурман марсохода'
    sex = 'male'
    motivation = 'Всегда местал застрять на Марсе!'
    ready_or_not = True
    return render_template('auto_answer.html', surname=surname, name=name, education=education, prof=prof, sex=sex,
                           motivation=motivation, ready_or_not=ready_or_not)


if __name__ == '__main__':
    app.run()
