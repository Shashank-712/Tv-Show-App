from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import User, TVShow, Season, Episode, Actor, Crew
from extensions import db

ui_bp = Blueprint("ui", __name__)

# ---------------- LOGIN ----------------
@ui_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            flash("Invalid username or password", "danger")
            return redirect(url_for("ui.login"))

        session["user_id"] = user.id
        session["role"] = user.role
        return redirect(url_for("ui.dashboard"))

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@ui_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("ui.login"))


# ---------------- DASHBOARD ----------------
@ui_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("ui.login"))
    return render_template("dashboard.html")


# ---------------- SHOWS ----------------
@ui_bp.route("/shows")
def shows():
    all_shows = TVShow.query.all()
    return render_template("shows.html", shows=all_shows)


@ui_bp.route("/shows/add", methods=["GET", "POST"])
def show_add():
    if session.get("role") != "admin":
        flash("Admin only", "danger")
        return redirect(url_for("ui.shows"))

    if request.method == "POST":
        title = request.form["title"].strip()
        description = request.form.get("description", "").strip()

        if not title:
            flash("Title is required", "danger")
            return redirect(url_for("ui.show_add"))

        s = TVShow(title=title, description=description)
        db.session.add(s)
        db.session.commit()

        flash("Show added!", "success")
        return redirect(url_for("ui.shows"))

    return render_template("show_add.html")


@ui_bp.route("/shows/<int:show_id>/edit", methods=["GET", "POST"])
def show_edit(show_id):
    show = TVShow.query.get_or_404(show_id)
    if session.get("role") != "admin":
        flash("Admin only", "danger")
        return redirect(url_for("ui.shows"))

    if request.method == "POST":
        show.title = request.form["title"]
        show.description = request.form.get("description")
        db.session.commit()

        flash("Show updated", "success")
        return redirect(url_for("ui.shows"))

    return render_template("show_edit.html", show=show)


@ui_bp.route("/shows/<int:show_id>/delete", methods=["POST"])
def show_delete(show_id):
    if session.get("role") != "admin":
        flash("Admin only", "danger")
        return redirect(url_for("ui.shows"))

    show = TVShow.query.get_or_404(show_id)
    db.session.delete(show)
    db.session.commit()
    flash("Show deleted", "success")
    return redirect(url_for("ui.shows"))


# ---------------- SEASONS ----------------

@ui_bp.route("/shows/<int:show_id>/seasons")
def seasons(show_id):
    show = TVShow.query.get_or_404(show_id)
    return render_template("seasons.html", show=show, seasons=show.seasons)


@ui_bp.route("/shows/<int:show_id>/seasons/add", methods=["GET", "POST"])
def season_add(show_id):
    if session.get("role") != "admin":
        flash("Admin only", "danger")
        return redirect(url_for("ui.seasons", show_id=show_id))

    show = TVShow.query.get_or_404(show_id)

    if request.method == "POST":
        number = request.form["season_number"]
        title = request.form["title"]

        if not number:
            flash("Season number required", "danger")
            return redirect(url_for("ui.season_add", show_id=show_id))

        s = Season(season_number=number, title=title, tvshow_id=show_id)
        db.session.add(s)
        db.session.commit()

        flash("Season added", "success")
        return redirect(url_for("ui.seasons", show_id=show_id))

    return render_template("season_add.html", show=show)


@ui_bp.route("/seasons/<int:season_id>/edit", methods=["GET", "POST"])
def season_edit(season_id):
    season = Season.query.get_or_404(season_id)
    show_id = season.tvshow_id

    if session.get("role") != "admin":
        flash("Admin only", "danger")
        return redirect(url_for("ui.seasons", show_id=show_id))

    if request.method == "POST":
        season.season_number = request.form["season_number"]
        season.title = request.form["title"]
        db.session.commit()

        flash("Season updated", "success")
        return redirect(url_for("ui.seasons", show_id=show_id))

    return render_template("season_edit.html", season=season)


@ui_bp.route("/seasons/<int:season_id>/delete", methods=["POST"])
def season_delete(season_id):
    season = Season.query.get_or_404(season_id)
    show_id = season.tvshow_id

    if session.get("role") != "admin":
        flash("Admin only", "danger")
        return redirect(url_for("ui.seasons", show_id=show_id))

    db.session.delete(season)
    db.session.commit()

    flash("Season deleted", "success")
    return redirect(url_for("ui.seasons", show_id=show_id))


# ---------------- EPISODES ----------------
@ui_bp.route("/seasons/<int:season_id>/episodes", methods=["GET", "POST"])
def episodes(season_id):
    season = Season.query.get_or_404(season_id)

    if request.method == "POST":
        if session.get("role") != "admin":
            flash("Admin only", "danger")
            return redirect(url_for("ui.episodes", season_id=season_id))

        ep = Episode(
            episode_number=request.form["episode_number"],
            title=request.form["title"],
            description=request.form.get("description"),
            season_id=season_id
        )
        db.session.add(ep)
        db.session.commit()

        flash("Episode added!", "success")
        return redirect(url_for("ui.episodes", season_id=season_id))

    return render_template("episodes.html", season=season)


# ---------------- ACTORS ----------------
@ui_bp.route("/actors", methods=["GET", "POST"])
def actors():
    if request.method == "POST":
        if session.get("role") != "admin":
            flash("Admin only", "danger")
            return redirect(url_for("ui.actors"))

        actor = Actor(
            first_name=request.form["first_name"],
            last_name=request.form.get("last_name")
        )
        db.session.add(actor)
        db.session.commit()

        flash("Actor added!", "success")
        return redirect(url_for("ui.actors"))

    all_actors = Actor.query.all()
    return render_template("actors.html", actors=all_actors)


# ---------------- CREW ----------------
@ui_bp.route("/crew", methods=["GET", "POST"])
def crew():
    if request.method == "POST":
        if session.get("role") != "admin":
            flash("Admin only", "danger")
            return redirect(url_for("ui.crew"))

        c = Crew(
            first_name=request.form["first_name"],
            last_name=request.form.get("last_name"),
            person_definition=request.form.get("person_definition")
        )
        db.session.add(c)
        db.session.commit()

        flash("Crew added!", "success")
        return redirect(url_for("ui.crew"))

    all_crew = Crew.query.all()
    return render_template("crew.html", crew=all_crew)


# ---------------- REGISTER ----------------
@ui_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        password2 = request.form["password2"]
        email = request.form["email"].strip()

        if not username or not password:
            flash("Username and password required.", "danger")
            return redirect(url_for("ui.register"))

        if password != password2:
            flash("Passwords do not match", "danger")
            return redirect(url_for("ui.register"))

        if User.query.filter_by(username=username).first():
            flash("Username already exists", "danger")
            return redirect(url_for("ui.register"))

        u = User(username=username, email=email, role="user")
        u.set_password(password)
        db.session.add(u)
        db.session.commit()

        flash("Registration successful!", "success")
        return redirect(url_for("ui.login"))

    return render_template("register.html")

# ---------------- EPISODE EDIT ----------------
@ui_bp.route("/episodes/<int:episode_id>/edit", methods=["GET", "POST"])
def episode_edit(episode_id):
    ep = Episode.query.get_or_404(episode_id)
    season = ep.season

    if session.get("role") != "admin":
        flash("Admin only", "danger")
        return redirect(url_for("ui.episodes", season_id=ep.season_id))

    # load all actors/crew for selection lists
    all_actors = Actor.query.order_by(Actor.first_name, Actor.last_name).all()
    all_crew = Crew.query.order_by(Crew.first_name, Crew.last_name).all()

    if request.method == "POST":
        # basic fields
        ep.episode_number = request.form.get("episode_number")
        ep.title = request.form.get("title")
        ep.description = request.form.get("description")

        # actor assignments (checkboxes or multi-select)
        actor_ids = request.form.getlist("actor_ids")  # list of strings
        if actor_ids:
            ep.actors = Actor.query.filter(Actor.id.in_(actor_ids)).all()
        else:
            ep.actors = []

        # crew assignments
        crew_ids = request.form.getlist("crew_ids")
        if crew_ids:
            ep.crew = Crew.query.filter(Crew.id.in_(crew_ids)).all()
        else:
            ep.crew = []

        db.session.commit()
        flash("Episode updated", "success")
        return redirect(url_for("ui.episodes", season_id=ep.season_id))

    return render_template("episode_edit.html", episode=ep, season=season, all_actors=all_actors, all_crew=all_crew)


# ---------------- EPISODE DELETE ----------------
@ui_bp.route("/episodes/<int:episode_id>/delete", methods=["POST"])
def episode_delete(episode_id):
    ep = Episode.query.get_or_404(episode_id)
    season_id = ep.season_id
    if session.get("role") != "admin":
        flash("Admin only", "danger")
        return redirect(url_for("ui.episodes", season_id=season_id))

    db.session.delete(ep)
    db.session.commit()
    flash("Episode deleted", "success")
    return redirect(url_for("ui.episodes", season_id=season_id))
