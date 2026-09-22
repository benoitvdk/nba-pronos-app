"""Official-ish NBA team primary colors (hex), keyed by full team name
exactly as used by balldontlie/theoddsapi (and thus how they're stored in
Series.team_a/team_b, Game.team_a/team_b - see the README's ingestion
section).

Used as the fill for prediction buttons/cells (team_color) plus a matching
readable text color (team_text_color). Several teams share the exact same
primary (e.g. Bulls/Rockets/Raptors are all "#CE1141", Jazz/Wizards are
both "#002B5C") so a plain white-or-black text color alone can't tell two
same-primary teams apart. team_text_color tries each team's own secondary
color (TEAM_SECONDARY_COLORS) first and only falls back to white/black
when that secondary doesn't read clearly on the primary - see its
docstring below. A few teams override this entirely (TEAM_STYLE_OVERRIDES)
with a hand-picked fill/text pair; a couple of those use a two-tone
diagonal-split fill instead of a flat color (see _css_fill). Exact hues
are approximate brand colors, good enough for this purpose - not meant to
be pixel-perfect.

IMPORTANT for template authors: team_color()'s result is CSS for the
`background` property, not necessarily a plain hex (it can be a
`linear-gradient(...)` for a two-tone team) - always write
`style="background:{{ ... | team_color }}"`, never `background-color:`,
which can't render a gradient and would silently show no fill at all for
a two-tone team.

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

# Each team's secondary/accent brand color, used by team_text_color() below
# as the preferred text color on top of the primary fill - mainly so two
# teams sharing the same primary (see the module docstring) don't also end
# up with identical text. Deliberately not every team's most famous accent:
# a few picks (Knicks, Pistons, ...) favor whichever of a team's real
# secondary colors actually contrasts with ITS OWN primary, since a color
# that doesn't read clearly there is useless as text no matter how iconic
# it is - team_text_color falls back to white/black for those anyway.
TEAM_SECONDARY_COLORS = {
    "Atlanta Hawks": "#C4D600",
    "Boston Celtics": "#BA9653",
    "Brooklyn Nets": "#FFFFFF",
    "Charlotte Hornets": "#00778C",
    "Chicago Bulls": "#000000",
    "Cleveland Cavaliers": "#FDBB30",
    "Dallas Mavericks": "#002B5E",
    "Denver Nuggets": "#FEC524",
    "Detroit Pistons": "#B1B3B3",
    "Golden State Warriors": "#FFC72C",
    "Houston Rockets": "#FDB927",
    "Indiana Pacers": "#FDBB30",
    "LA Clippers": "#000000",
    "Los Angeles Clippers": "#000000",  # alias, see TEAM_COLORS
    "Los Angeles Lakers": "#FDB927",
    "Memphis Grizzlies": "#F5B112",
    "Miami Heat": "#F9A01B",
    "Milwaukee Bucks": "#EEE1C6",
    "Minnesota Timberwolves": "#78BE20",
    "New Orleans Pelicans": "#B4975A",
    "New York Knicks": "#000000",
    "Oklahoma City Thunder": "#EF3B24",
    "Orlando Magic": "#C4CED4",
    "Philadelphia 76ers": "#ED174C",
    "Phoenix Suns": "#E56020",
    "Portland Trail Blazers": "#000000",
    "Sacramento Kings": "#63727A",
    "San Antonio Spurs": "#C4CED4",
    "Toronto Raptors": "#A1A1A4",
    "Utah Jazz": "#F9A01B",
    "Washington Wizards": "#C8102E",
}

# WCAG AA's "large text" contrast minimum (button labels here are bold,
# ~14-15px - close enough in spirit). Real team secondary colors routinely
# fall short of the stricter 4.5:1 normal-text bar against their own
# primary, which would make the secondary-color branch above dead code for
# most teams; 3.0 is the lowest bar that still means something (below it,
# text is genuinely hard to read, not just "not textbook AA").
MIN_TEXT_CONTRAST = 3.0

# Manual fill/text picks for a handful of teams where the automatic
# contrast logic above didn't land on the look actually wanted - some
# swap which of the two brand colors is the fill vs. the text (Knicks,
# Hornets, Suns, Pelicans, Lakers), others just pin a specific accent
# instead of whichever one happened to win the contrast check (Pacers -
# its auto pick is in a comment for context). 76ers and Pistons go further
# with a two-tone diagonal fill (fill is a (color, color) pair instead of
# a single hex - see _css_fill) plus white text, rather than a flat color.
# {team_name: (fill, text)}. Checked first by team_color()/team_text_color(),
# ahead of everything else in this file - a team listed here skips the
# contrast math entirely.
TEAM_STYLE_OVERRIDES = {
    "New York Knicks": ("#FF671F", "#006BB6"),                  # fill/text swapped
    "Philadelphia 76ers": (("#006BB6", "#E4002B"), "#FFFFFF"),  # two-tone blue/red fill, white text
    "Detroit Pistons": (("#C8102E", "#001F3F"), "#FFFFFF"),     # two-tone red/navy fill, white text
    "Indiana Pacers": ("#FDBB30", "#002D62"),                   # was navy fill -> yellow fill, navy text
    "Charlotte Hornets": ("#00778C", "#1D1160"),                # fill/text swapped
    "Phoenix Suns": ("#E56020", "#1D1160"),                     # fill/text swapped
    "New Orleans Pelicans": ("#B4975A", "#00285E"),             # fill/text swapped
    "Los Angeles Lakers": ("#FDB927", "#552583"),               # fill/text swapped
}


def _css_fill(fill):
    """A plain hex string passes through unchanged; a (hex, hex) pair
    (a two-tone TEAM_STYLE_OVERRIDES entry) becomes a hard-stop diagonal
    split - a CSS gradient string, still valid for the `background`
    property but NOT for `background-color` (see the module docstring)."""
    if isinstance(fill, (tuple, list)):
        a, b = fill
        return f"linear-gradient(135deg, {a} 0%, {a} 50%, {b} 50%, {b} 100%)"
    return fill


def team_color(team_name):
    """CSS `background` value for a team name (a hex color, or a two-tone
    gradient for a team overridden that way - see _css_fill), or
    DEFAULT_COLOR if unknown. Never raises - registered as a Jinja filter
    (see app/__init__.py) so a typo in a manually-entered team name
    degrades to a gray fill instead of a 500."""
    if team_name in TEAM_STYLE_OVERRIDES:
        return _css_fill(TEAM_STYLE_OVERRIDES[team_name][0])
    return TEAM_COLORS.get(team_name, DEFAULT_COLOR)


def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def _srgb_channel(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def _relative_luminance(hex_color):
    r, g, b = _hex_to_rgb(hex_color)
    return 0.2126 * _srgb_channel(r) + 0.7152 * _srgb_channel(g) + 0.0722 * _srgb_channel(b)


def _contrast_ratio(hex_a, hex_b):
    """WCAG contrast ratio between two colors - 1 (identical) to 21
    (black on white)."""
    la, lb = _relative_luminance(hex_a), _relative_luminance(hex_b)
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def team_secondary_color(team_name):
    """Hex for a team's secondary/accent color, or None when the team
    isn't in TEAM_SECONDARY_COLORS. Not registered as a Jinja filter on
    its own - team_text_color() below is what templates use."""
    return TEAM_SECONDARY_COLORS.get(team_name)


def team_text_color(team_name):
    """Text color for team_color(team_name): the team's own secondary
    color when it contrasts clearly against the primary (>= MIN_TEXT_
    CONTRAST) - this is what tells apart two teams that happen to share
    the same primary, e.g. Bulls (black text) vs Rockets (gold text) even
    though both fill red - otherwise plain white or near-black, whichever
    contrasts more (WCAG relative luminance). Registered as a Jinja filter
    alongside team_color - see app/__init__.py. Never raises, for the same
    reason team_color doesn't."""
    if team_name in TEAM_STYLE_OVERRIDES:
        return TEAM_STYLE_OVERRIDES[team_name][1]
    primary = team_color(team_name)
    secondary = team_secondary_color(team_name)
    if secondary and _contrast_ratio(primary, secondary) >= MIN_TEXT_CONTRAST:
        return secondary
    return "#111111" if _relative_luminance(primary) > 0.5 else "#ffffff"
