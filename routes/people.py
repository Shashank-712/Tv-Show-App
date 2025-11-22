# routes/people.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Actor, Crew, ScreenTime, Episode
from schemas import ActorSchema, CrewSchema, ScreenTimeSchema

people_bp = Blueprint("people", __name__, url_prefix="/api/people")

def admin_required_identity():
    identity = get_jwt_identity()
    return identity and identity.get("role") == "admin"

@people_bp.route('/actors', methods=['POST'])
@jwt_required()
def create_actor():
    if not admin_required_identity():
        return {"msg":"admin only"}, 403
    data = request.get_json() or {}
    errors = ActorSchema().validate(data)
    if errors:
        return errors, 400
    a = Actor(first_name=data['first_name'], last_name=data.get('last_name'))
    db.session.add(a)
    db.session.commit()
    return ActorSchema().dump(a), 201

@people_bp.route('/crews', methods=['POST'])
@jwt_required()
def create_crew():
    if not admin_required_identity():
        return {"msg":"admin only"}, 403
    data = request.get_json() or {}
    errors = CrewSchema().validate(data)
    if errors:
        return errors, 400
    c = Crew(first_name=data.get('first_name'), last_name=data.get('last_name'), person_definition=data.get('person_definition'))
    db.session.add(c)
    db.session.commit()
    return CrewSchema().dump(c), 201

@people_bp.route('/screentimes', methods=['POST'])
@jwt_required()
def create_screentime():
    # both admin and normal users can create, adapt as needed
    data = request.get_json() or {}
    errors = ScreenTimeSchema().validate(data)
    if errors:
        return errors, 400

    # relational existence checks
    actor_exists = Actor.query.get(data["actor_id"])
    if not actor_exists:
        return {"msg": "actor not found"}, 404
    if not Episode.query.get(data["episode_id"]):
        return {"msg": "episode not found"}, 404

    st = ScreenTime(actor_id=data['actor_id'],
                    episode_id=data['episode_id'],
                    start_time=data.get('start_time'),
                    end_time=data.get('end_time'),
                    role_name=data.get('role_name'),
                    role_type=data.get('role_type'))
    db.session.add(st)
    db.session.commit()
    return ScreenTimeSchema().dump(st), 201
