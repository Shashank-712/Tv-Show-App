TV SHOW MANAGEMENT APPLICATION
==============================

This project is a fully functional web application built using Python (Flask)
based on the provided ER diagram for TV Shows, Seasons, Episodes, Actors, and Crew.

The application includes:
- Authentication (Login, Logout, Password Hashing)
- Authorization (Admin & User roles)
- CRUD operations for Shows, Seasons, Episodes, Actors, Crew
- Many-to-many relationships (Episode ↔ Actors, Episode ↔ Crew)
- Relational integrity enforcement via SQLAlchemy ORM
- Dynamic UI with clean navigation
- PostgreSQL database
- API + UI integration

--------------------------------------------------------------------------------
1. FEATURES
--------------------------------------------------------------------------------

A. AUTHENTICATION
- Secure Login and Logout
- Password hashing (Werkzeug)
- User registration

B. AUTHORIZATION
- Admin and User roles
- Only Admin can:
    - Add/Edit/Delete Shows
    - Add/Edit/Delete Seasons
    - Add/Edit/Delete Episodes
    - Add/Edit/Delete Actors/Crew
- Users can only view data

C. COMPLETE CRUD OPERATIONS
- TV Shows: Add, View, Update, Delete
- Seasons: Add, View, Update, Delete
- Episodes:
    • Add episode to a season
    • Edit episode details
    • Assign multiple actors
    • Assign multiple crew members
    • Delete episode
- Actors + Crew:
    • Add new Actor/Crew
    • Auto-link via episode editor

D. CLIENT-SIDE + SERVER-SIDE VALIDATION
- Required field checks
- Simple JavaScript validation
- Server-side relational checks

E. DATABASE
- PostgreSQL (tvdb)
- SQLAlchemy ORM
- Many-to-many relationship tables

F. UI (Bootstrap + Custom CSS)
- Dashboard
- Shows List → Seasons List → Episodes List → Episode Editor
- Actors & Crew Pages
- Fully responsive layout

--------------------------------------------------------------------------------
Project Structure
-----------------
```
tvshow_app/
│
├── app.py                      # Flask entry point
├── models.py                   # ORM models (TVShow, Season, Episode, Actor, Crew, User)
├── extensions.py               # Database, JWT & other extensions
│
├── ui/
│   └── ui_routes.py            # UI (HTML pages) routes
│
├── api/
│   └── api_routes.py           # API endpoints
│
├── templates/                  # Frontend HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   ├── shows.html
│   ├── show_add.html
│   ├── show_edit.html
│   ├── seasons.html
│   ├── season_add.html
│   ├── season_edit.html
│   ├── episodes.html
│   ├── episode_edit.html
│   ├── actors.html
│   └── crew.html
│
├── static/
│   └── css/
│       └── styles.css          # Custom UI styling
│
└── migrations/                 # Flask-Migrate auto-generated migration files
```
--------------------------------------------------------------------------------
3. HOW TO RUN THE PROJECT
--------------------------------------------------------------------------------

1. Create a virtual environment
   python -m venv venv
   venv\Scripts\activate  (Windows)

2. Install dependencies
   pip install -r requirements.txt

3. Setup PostgreSQL
   Create database:  tvdb
   Create user:      tvuser  (your chosen user)
   Password:         your-password

4. Update database URL if needed in app.py:
   postgresql+psycopg://tvuser:password@localhost:5432/tvdb

5. Apply migrations
   flask db upgrade

6. Run the server
   python app.py

7. Access UI:
   http://127.0.0.1:5000/login

--------------------------------------------------------------------------------
4. API ENDPOINTS (SUMMARY)
--------------------------------------------------------------------------------

AUTH:
- POST /api/auth/register
- POST /api/auth/login

TV SHOWS:
- GET /api/tv/shows
- POST /api/tv/shows   (Admin)
- PUT /api/tv/shows/<id>  (Admin)
- DELETE /api/tv/shows/<id> (Admin)

SEASONS:
- GET /api/tv/shows/<id>/seasons
- POST /api/tv/shows/<id>/seasons (Admin)

EPISODES:
- GET /api/seasons/<id>/episodes
- POST /api/seasons/<id>/episodes (Admin)
- PUT /api/episodes/<id>
- DELETE /api/episodes/<id>

--------------------------------------------------------------------------------
5. DATABASE SCHEMA EXPORT
--------------------------------------------------------------------------------

Run:
pg_dump -s -U tvuser -d tvdb > schema.sql

Include schema.sql in your GitHub repo.

--------------------------------------------------------------------------------
6. ADMIN CREATION SCRIPT
--------------------------------------------------------------------------------

You can include “create_admin.py” like:

from app import create_app
from models import User
from extensions import db

app = create_app()

with app.app_context():
    admin = User(username="admin", role="admin")
    admin.set_password("Admin123")
    db.session.add(admin)
    db.session.commit()
    print("Admin created.")

--------------------------------------------------------------------------------
7.  ER Diagram
--------------------------------------------------------------------------------

Below is the Entity-Relationship diagram used to design this application:

<p align="center">
  <img src="templates/static/er_diagram.png" width="750">
</p>

🙌 Author
Made with 💻 by Shashank Rawat👹
👉 github.com/Shashank-712

