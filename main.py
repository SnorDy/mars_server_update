from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
import json
from data.users import User
from requests import get
from os import listdir
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from data import db_session, news_api, jobs_api, users_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    # db_sess=db_session.create_session()
    # user=User()
    # user.name='Marshall Maters'
    # user.about='something2'
    # user.email='slimshady@mars.com'
    # user.hashed_password='1234567890'
    # user.city_from='Detroit'
    # db_sess.add(user)
    # db_sess.commit()
    app.register_blueprint(news_api.blueprint)
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run()


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
    id = StringField('id астронавта', validators=[DataRequired()])
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
    motivation = 'Всегда мечтал застрять на Марсе!'
    ready_or_not = True
    return render_template('auto_answer.html', surname=surname, name=name, education=education, prof=prof, sex=sex,
                           motivation=motivation, ready_or_not=ready_or_not)


@app.route('/member')
def member():
    with open('templates/members.json', encoding='utf-8') as file:
        members = json.load(file)
    return render_template('member.html', members=members)


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    try:
        user = get(f'http://127.0.0.1:5000/api/users/{user_id}').json()['user']
    except Exception:
        return 'Извините, что-то пошло не так, проверьте правильность написания ссылки.'
    name, surname = user['name'].split()
    city = user['city_from']
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={city}&format=json"
    response = get(geocoder_request)
    if response:
        response = response.json()
        toponym = response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"].split()
        link = f'https://static-maps.yandex.ru/1.x/?ll={toponym_coodrinates[0]},{toponym_coodrinates[1]}&size=450,450&z=14&l=sat'
    else:
        link = 'Извините, не получилось!'
    return render_template('users_show.html', name=name, surname=surname, city=city, link=link)


if __name__ == '__main__':
    main()
    app.run()
