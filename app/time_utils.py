"""Petit utilitaire de dates. SQLite (utilisé dans les tests) ne conserve pas
le fuseau horaire des colonnes DateTime(timezone=True) - il renvoie des
datetimes naïves, contrairement à Postgres/Neon en production qui renvoie
bien des datetimes avec fuseau. Cette fonction homogénéise les deux avant
toute comparaison, en supposant UTC quand l'info est absente (c'est toujours
ce qu'on stocke)."""
from datetime import timezone


def ensure_aware_utc(dt):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt
