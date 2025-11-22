# create_superuser.py
from app import create_app
from extensions import db
from models import User

app = create_app()
app.app_context().push()

username = "superadmin"
password = "SuperPass123"
email = "admin@example.com"

if User.query.filter_by(username=username).first():
    print("User already exists. Updating role to admin.")
    u = User.query.filter_by(username=username).first()
    u.role = "admin"
    u.set_password(password)
else:
    u = User(username=username, email=email, role="admin")
    u.set_password(password)
    db.session.add(u)

db.session.commit()
print("Superuser created/updated:", username)
