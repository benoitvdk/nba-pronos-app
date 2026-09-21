"""Adds a player with an automatically generated access code (no
password). Prints the full login link to send them.

Usage:
    python -m scripts.add_player "First Last"
    python -m scripts.add_player "First Last" --base-url https://your-app.onrender.com
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
    # Short enough to fit in a link sent via SMS/WhatsApp, long enough to
    # not be guessable.
    return secrets.token_urlsafe(9)  # ~12 characters


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Player name")
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:5000",
        help="App base URL (defaults to the local dev server)",
    )
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        code = generate_access_code()
        while Player.query.filter_by(access_code=code).first() is not None:
            code = generate_access_code()  # very unlikely collision, safety net

        player = Player(name=args.name, access_code=code)
        db.session.add(player)
        db.session.commit()

        print(f"Player created: {player.name} (id={player.id})")
        print(f"Link to send them: {args.base_url}/login/{code}")


if __name__ == "__main__":
    main()
