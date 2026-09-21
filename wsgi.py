"""WSGI entry point for deployment on Render (gunicorn wsgi:app)."""
from dotenv import load_dotenv

load_dotenv()  # no-op in prod (Render already provides the environment variables)

from app import create_app  # noqa: E402

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
