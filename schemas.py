# schemas.py
from marshmallow import Schema, fields, validates, ValidationError, post_load
from datetime import date

# Basic user schema (for serialization, not password handling)
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(allow_none=True)
    role = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)

# TV show schema
class TVShowSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)

# Season schema
class SeasonSchema(Schema):
    id = fields.Int(dump_only=True)
    tvshow_id = fields.Int(required=True)
    season_number = fields.Int(required=True)
    season_description = fields.Str(allow_none=True)
    date_started = fields.Date(allow_none=True)
    date_ended = fields.Date(allow_none=True)
    title = fields.Str(allow_none=True)

    @validates("season_number")
    def validate_season_number(self, value):
        if value is None or value < 1:
            raise ValidationError("season_number must be an integer >= 1")

    @validates("date_ended")
    def validate_date_ended(self, value):
        # Ensure date_ended is not before date_started if both provided
        if value is not None and not isinstance(value, date):
            raise ValidationError("date_ended must be a valid date")
        # We cannot access date_started here directly, full object validation can be done in route if needed

# Episode schema
class EpisodeSchema(Schema):
    id = fields.Int(dump_only=True)
    season_id = fields.Int(required=True)
    episode_number = fields.Int(required=True)
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    rating = fields.Int(allow_none=True)
    date_published = fields.Date(allow_none=True)

    @validates("episode_number")
    def validate_episode_number(self, value):
        if value is None or value < 1:
            raise ValidationError("episode_number must be an integer >= 1")

    @validates("rating")
    def validate_rating(self, value):
        if value is not None and (value < 0 or value > 10):
            raise ValidationError("rating must be between 0 and 10")

# Actor schema
class ActorSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(allow_none=True)

# Crew schema
class CrewSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(allow_none=True)
    person_definition = fields.Str(allow_none=True)

# ScreenTime schema
class ScreenTimeSchema(Schema):
    id = fields.Int(dump_only=True)
    actor_id = fields.Int(required=True)
    episode_id = fields.Int(required=True)
    start_time = fields.DateTime(allow_none=True)
    end_time = fields.DateTime(allow_none=True)
    role_name = fields.Str(allow_none=True)
    role_type = fields.Str(allow_none=True)

    @validates("start_time")
    def validate_start_time(self, value):
        # simple check: must be a datetime string parseable by marshmallow
        if value is None:
            return
