# routes/tv.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import TVShow, Season, Episode
from extensions import db
from schemas import TVShowSchema, SeasonSchema, EpisodeSchema

tv_bp = Blueprint("tv", __name__, url_prefix="/tv")  # note: app registers with /api/tv, keep consistent in app.register

def is_admin():
    claims = get_jwt() or {}
    role = claims.get("role")
    # fallback if identity used differently
    identity = get_jwt_identity()
    if isinstance(identity, dict):
        role = role or identity.get("role")
    return role == "admin"

# LIST & DETAIL (existing)
@tv_bp.route("/shows", methods=["GET"])
def list_shows():
    shows = TVShow.query.all()
    return jsonify(TVShowSchema(many=True).dump(shows))

@tv_bp.route("/shows/<int:show_id>", methods=["GET"])
def show_detail(show_id):
    show = TVShow.query.get_or_404(show_id)
    return TVShowSchema().dump(show), 200

# CREATE (existing)
@tv_bp.route("/shows", methods=["POST"])
@jwt_required()
def create_show():
    if not is_admin():
        return {"msg":"admin only"}, 403
    data = request.get_json() or {}
    errors = TVShowSchema().validate(data)
    if errors:
        return errors, 400
    show = TVShow(title=data["title"], description=data.get("description"))
    db.session.add(show)
    db.session.commit()
    return TVShowSchema().dump(show), 201

# UPDATE (NEW)
@tv_bp.route("/shows/<int:show_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_show(show_id):
    if not is_admin():
        return {"msg":"admin only"}, 403
    show = TVShow.query.get_or_404(show_id)
    data = request.get_json() or {}
    # validate incoming fields
    errors = TVShowSchema(partial=True).validate(data)
    if errors:
        return errors, 400

    title = data.get("title")
    description = data.get("description")

    if title is not None:
        show.title = title
    if description is not None:
        show.description = description

    db.session.commit()
    return TVShowSchema().dump(show), 200

# DELETE (NEW)
@tv_bp.route("/shows/<int:show_id>", methods=["DELETE"])
@jwt_required()
def delete_show(show_id):
    if not is_admin():
        return {"msg":"admin only"}, 403
    show = TVShow.query.get_or_404(show_id)
    db.session.delete(show)
    db.session.commit()
    return {"msg": "deleted", "id": show_id}, 200

# the Season/Episode create endpoints remain unchanged below (if present in your file).
# Make sure this file is imported by app.py and the blueprint registered as before.

# ---------- UPDATE Season ----------
@tv_bp.route("/seasons/<int:season_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_season(season_id):
    if not is_admin():
        return {"msg": "admin only"}, 403

    season = Season.query.get_or_404(season_id)
    data = request.get_json() or {}

    errors = SeasonSchema(partial=True).validate(data)
    if errors:
        return errors, 400

    if "season_number" in data:
        season.season_number = data["season_number"]

    if "title" in data:
        season.title = data["title"]

    db.session.commit()
    return SeasonSchema().dump(season), 200


# ---------- DELETE Season ----------
@tv_bp.route("/seasons/<int:season_id>", methods=["DELETE"])
@jwt_required()
def delete_season(season_id):
    if not is_admin():
        return {"msg": "admin only"}, 403

    season = Season.query.get_or_404(season_id)
    db.session.delete(season)
    db.session.commit()

    return {"msg": "deleted", "id": season_id}, 200
