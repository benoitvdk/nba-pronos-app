"""Ajoute un joueur avec un code d'accès généré automatiquement (pas de mot
de passe). Affiche le lien de connexion complet à lui envoyer.

Usage:
    python -m scripts.add_player "Prénom Nom"
    python -m scripts.add_player "Prénom Nom" --base-url https://ton-app.onrender.com
"""
import argparse
import os
import secrets
import sys

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models import Player  # noqa: E402


def generate_access_code():
    # Assez court pour tenir dans un lien qu'on envoie par SMS/WhatsApp, assez
    # long pour ne pas être devinable.
    return secrets.token_urlsafe(9)  # ~12 caractères


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Nom du joueur")
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:5000",
        help="URL de base de l'app (par défaut : serveur de dev local)",
    )
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        code = generate_access_code()
        while Player.query.filter_by(access_code=code).first() is not None:
            code = generate_access_code()  # collision très improbable, sécurité

        player = Player(name=args.name, access_code=code)
        db.session.add(player)
        db.session.commit()

        print(f"Joueur créé : {player.name} (id={player.id})")
        print(f"Lien à lui envoyer : {args.base_url}/login/{code}")


if __name__ == "__main__":
    main()
