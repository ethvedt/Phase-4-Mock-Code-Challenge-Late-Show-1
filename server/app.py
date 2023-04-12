#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate

from models import db, Episode, Guest, Appearance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/episodes', methods=['GET'])
def episodes():
    episode_list = []
    for episode in Episode.query.all():
        ep_dict = episode.to_dict(only=('id', 'date', 'number'))
        episode_list.append(ep_dict)
    return make_response(episode_list, 200)
    
@app.route('/episodes/<int:id>', methods=['GET','DELETE'])
def episode_by_id(id):
    episode = Episode.query.filter(Episode.id == id).first()
    if not episode:
        return make_response(
            {"error": "404: Episode not found"},
            404
        )
    if request.method == 'GET':
        return make_response(episode.to_dict(), 200)
        
    elif request.method == 'DELETE':
        db.session.delete(episode)
        db.session.commit()
        return make_response('',204)
        
@app.route('/guests', methods=['GET'])
def guests():
    guest_list = []
    guests = Guest.query.all()
    for guest in guests:
        guest_dict = guest.to_dict(only=('id', 'name', 'occupation'))
        guest_list.append(guest_dict)
    return make_response(guest_list, 200)

@app.route('/appearances', methods=['POST'])
def new_app():
    if request.method == 'POST':
        try:
            appearance = Appearance(
                rating=request.form.get('rating'),
                episode_id=request.form.get('episode_id'),
                guest_id=request.form.get('guest_id')
            )
            db.session.add(appearance)
            db.session.commit()
            return make_response(
                appearance.to_dict(),
                201
            )
        except ValueError:
            return make_response(
                {"error": "400: Validation error."},
                400
            )


if __name__ == '__main__':
    app.run(port=5555, debug=True)

