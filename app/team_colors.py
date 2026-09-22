"""Official-ish NBA team primary colors (hex), keyed by full team name
exactly as used by balldontlie/theoddsapi (and thus how they're stored in
Series.team_a/team_b, Game.team_a/team_b - see the README's ingestion
section).

Used only as a light accent (small dot / left border), never as an opaque
background: several teams share red/blue/green tones that would otherwise
clash with the app's own correct/wrong color coding (see style.css). Exact
hues are approximate brand colors, good enough for a decorative dot - not
meant to be pixel-perfect.

A team name that isn't in this table (typo, relocation not added yet, ...)
falls back to DEFAULT_COLOR rather than raising, since this is purely
decorative and must never break a page render.
"""

DEFAULT_COLOR = "#9aa0ac"

TEAM_COLORS = {
    "Atlanta Hawks": "#E03A3E",
    "Boston Celtics": "#007A33",
    "Brooklyn Nets": "#000000",
    "Charlotte Hornets": "#1D1160",
    "Chicago Bulls": "#CE1141",
    "Cleveland Cavaliers": "#860038",
    "Dallas Mavericks": "#00538C",
    "Denver Nuggets": "#0E2240",
    "Detroit Pistons": "#C8102E",
    "Golden State Warriors": "#1D428A",
    "Houston Rockets": "#CE1141",
    "Indiana Pacers": "#002D62",
    "LA Clippers": "#C8102E",
    "Los Angeles Clippers": "#C8102E",  # alias, in case a series was entered with the long name
    "Los Angeles Lakers": "#552583",
    "Memphis Grizzlies": "#5D76A9",
    "Miami Heat": "#98002E",
    "Milwaukee Bucks": "#00471B",
    "Minnesota Timberwolves": "#0C2340",
    "New Orleans Pelicans": "#00285E",
    "New York Knicks": "#006BB6",
    "Oklahoma City Thunder": "#007AC1",
    "Orlando Magic": "#0077C0",
    "Philadelphia 76ers": "#006BB6",
    "Phoenix Suns": "#1D1160",
    "Portland Trail Blazers": "#E03A3E",
    "Sacramento Kings": "#5A2D81",
    "San Antonio Spurs": "#000000",
    "Toronto Raptors": "#CE1141",
    "Utah Jazz": "#002B5C",
    "Washington Wizards": "#002B5C",
}


def team_color(team_name):
    """Hex color for a team name, or DEFAULT_COLOR if unknown. Never
    raises - registered as a Jinja filter (see app/__init__.py) so a typo
    in a manually-entered team name degrades to a gray dot instead of a
    500."""
    return TEAM_COLORS.get(team_name, DEFAULT_COLOR)
