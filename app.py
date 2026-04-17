from config import create_app, db
from routes import register_routes

app = create_app()
register_routes(app)

# Initialize database if it doesn't exist
with app.app_context():
    try:
        db.create_all()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
