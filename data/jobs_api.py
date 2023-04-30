import flask
from flask import jsonify, request
from datetime import date
from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    if not jobs:
        return jsonify({'error': 'Not found'})
    sl = {'jobs': []}
    for el in jobs:
        sl['jobs'].append({'id': el.id, 'team_leader': el.team_leader, 'job': el.job, 'work_size':
            el.work_size, 'collaborators': el.collaborators, 'start_date': el.start_date, 'end_date': el.end_date,
                           'is_finished': el.is_finished})

    return jsonify(sl)


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_job(jobs_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(jobs_id)
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'job': job.to_dict(only=(
                'team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if 'id' not in request.json:
        job_id=None
    else:
        if db_sess.query(Jobs).filter(Jobs.id == request.json['id']).first():
            return jsonify({'error': 'Id already exists.'})
        job_id=request.json['id']
    job = Jobs(id=job_id,
               team_leader=request.json['team_leader'],
               job=request.json['job'],
               work_size=request.json['work_size'],
               collaborators=request.json['collaborators'],
               start_date=date(*map(int, request.json['start_date'].split('-'))),
               end_date=date(*map(int, request.json['end_date'].split('-'))),
               is_finished=request.json['is_finished']
               )
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_user(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})
