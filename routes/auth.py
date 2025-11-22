# routes/auth.py
from flask import Blueprint, request, jsonify
from models import User
from extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return {"msg":"username and password required"}, 400
    if User.query.filter_by(username=username).first():
        return {"msg":"username exists"}, 400
    u = User(username=username, email=data.get("email"), role=data.get("role","user"))
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return {"msg":"user created", "id": u.id}, 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password", "")
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return {"msg":"bad credentials"}, 401
    token = create_access_token(identity={"id": user.id, "role": user.role})
    return {"access_token": token}, 200

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    identity = get_jwt_identity()
    user = User.query.get(identity["id"])
    if not user:
        return {"msg": "user not found"}, 404
    return {"id": user.id, "username": user.username, "role": user.role}
