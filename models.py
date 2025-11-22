from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------------
# User model (auth)
# -------------------------
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(254), nullable=True)
    role = db.Column(db.String(20), default="user", nullable=False)  # 'admin' or 'user'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, pw: str) -> None:
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw: str) -> bool:
        return check_password_hash(self.password_hash, pw)

    def __repr__(self) -> str:
        return f"<User {self.username}>"

# -------------------------
# Association tables (many-to-many)
# -------------------------
episode_actors = db.Table(
    "episode_actors",
    db.Column("episode_id", db.Integer, db.ForeignKey("episode.id"), primary_key=True),
    db.Column("actor_id", db.Integer, db.ForeignKey("actor.id"), primary_key=True)
)

# -------------------------
# TV show, season, episode
# -------------------------
class TVShow(db.Model):
    __tablename__ = "tvshow"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(200), nullable=True)

    seasons = db.relationship("Season", back_populates="tvshow", cascade="all, delete-orphan", lazy="select")

    def __repr__(self) -> str:
        return f"<TVShow {self.title}>"

class Season(db.Model):
    __tablename__ = "season"

    id = db.Column(db.Integer, primary_key=True)
    tvshow_id = db.Column(db.Integer, db.ForeignKey("tvshow.id"), nullable=False)
    season_number = db.Column(db.Integer, nullable=False)
    season_description = db.Column(db.String(200), nullable=True)
    date_started = db.Column(db.Date, nullable=True)
    date_ended = db.Column(db.Date, nullable=True)
    title = db.Column(db.String(128), nullable=True)

    tvshow = db.relationship("TVShow", back_populates="seasons", lazy="joined")
    episodes = db.relationship("Episode", back_populates="season", cascade="all, delete-orphan", lazy="select")

    __table_args__ = (db.UniqueConstraint("tvshow_id", "season_number", name="uq_tv_season"),)

    def __repr__(self) -> str:
        return f"<Season {self.season_number} of tvshow {self.tvshow_id}>"

class Episode(db.Model):
    __tablename__ = "episode"

    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey("season.id"), nullable=False)
    episode_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    date_published = db.Column(db.Date, nullable=True)

    season = db.relationship("Season", back_populates="episodes", lazy="joined")
    screentimes = db.relationship("ScreenTime", back_populates="episode", cascade="all, delete-orphan", lazy="select")
    crews = db.relationship("EpisodeCrew", back_populates="episode", cascade="all, delete-orphan", lazy="select")
    actors = db.relationship("Actor", secondary=episode_actors, back_populates="episodes")

    __table_args__ = (db.UniqueConstraint("season_id", "episode_number", name="uq_season_episode"),)

    def __repr__(self) -> str:
        return f"<Episode S{self.season_id}-E{self.episode_number}>"

# -------------------------
# Crew, actors, screen time
# -------------------------
class Crew(db.Model):
    __tablename__ = "crew"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    person_definition = db.Column(db.String(128), nullable=True)

    episode_crews = db.relationship("EpisodeCrew", back_populates="crew", cascade="all, delete-orphan", lazy="select")

    def __repr__(self) -> str:
        return f"<Crew {self.first_name} {self.last_name}>"

class EpisodeCrew(db.Model):
    __tablename__ = "episode_crew"

    id = db.Column(db.Integer, primary_key=True)
    episode_id = db.Column(db.Integer, db.ForeignKey("episode.id"), nullable=False)
    crew_id = db.Column(db.Integer, db.ForeignKey("crew.id"), nullable=False)

    episode = db.relationship("Episode", back_populates="crews", lazy="joined")
    crew = db.relationship("Crew", back_populates="episode_crews", lazy="joined")

    __table_args__ = (db.UniqueConstraint("episode_id", "crew_id", name="uq_episode_crew"),)

    def __repr__(self) -> str:
        return f"<EpisodeCrew ep={self.episode_id} crew={self.crew_id}>"

class Actor(db.Model):
    __tablename__ = "actor"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=True)

    screentimes = db.relationship("ScreenTime", back_populates="actor", cascade="all, delete-orphan", lazy="select")
    episodes = db.relationship("Episode", secondary=episode_actors, back_populates="actors")

    def __repr__(self) -> str:
        return f"<Actor {self.first_name} {self.last_name}>"

class ScreenTime(db.Model):
    __tablename__ = "screentime"

    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey("actor.id"), nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey("episode.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=True)
    end_time = db.Column(db.DateTime, nullable=True)
    role_name = db.Column(db.String(128), nullable=True)
    role_type = db.Column(db.String(128), nullable=True)

    actor = db.relationship("Actor", back_populates="screentimes", lazy="joined")
    episode = db.relationship("Episode", back_populates="screentimes", lazy="joined")

    __table_args__ = (db.UniqueConstraint("actor_id", "episode_id", "start_time", name="uq_actor_episode_time"),)

    def __repr__(self) -> str:
        return f"<ScreenTime actor={self.actor_id} episode={self.episode_id}>"