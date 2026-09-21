"""Point d'entrée WSGI pour le déploiement sur Render (gunicorn wsgi:app)."""
from dotenv import load_dotenv

load_dotenv()  # no-op en prod (Render fournit déjà les variables d'environnement)

from app import create_app  # noqa: E402

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
