import flask
from flask import jsonify, request
from datetime import date
from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'name', 'about', 'email', 'hashed_password', 'created_date','city_from'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_news(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=(
                'id', 'name', 'about', 'email', 'hashed_password', 'created_date','city_from'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['name', 'about', 'email', 'hashed_password','city_from']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if 'id' not in request.json:
        user_id = None
    else:
        if db_sess.query(User).filter(User.id == request.json['id']).first():
            return jsonify({'error': 'Id already exists.'})
        user_id = request.json['id']
    user = User(id=user_id,
                name=request.json['name'],
                about=request.json['about'],
                email=request.json['email'],
                hashed_password=request.json['hashed_password'],
                created_date=None,
                city_from=request.json['city_from']
                )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['POST'])
def change_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if 'name' in request.json:
        user.name = request.json['name']
    if 'about' in request.json:
        user.about = request.json['about']
    if 'email' in request.json:
        user.email = request.json['email']
    if 'hashed_password' in request.json:
        user.hashed_password = request.json['hashed_password']
    if 'created_date' in request.json:
        user.created_date = request.json['created_date']
    if 'city_from' in request.json:
        user.city_from=request.json['city_from']
    db_sess.commit()
    return jsonify({'success': 'OK'})
