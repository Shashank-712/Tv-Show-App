from flask import Flask, redirect, session, url_for
from config import Config
from extensions import db, migrate, jwt
from routes.auth import auth_bp
from routes.tv import tv_bp
from routes.people import people_bp
from ui.ui_routes import ui_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # API routes
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(tv_bp, url_prefix="/api/tv")
    app.register_blueprint(people_bp, url_prefix="/api/people")

    # UI routes
    app.register_blueprint(ui_bp)

    @app.route("/")
    def home():
        if "user_id" in session:
            return redirect(url_for("ui.dashboard"))
        return redirect(url_for("ui.login"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
