import random
from flask import Flask, make_response, render_template

from dice import DICE

app = Flask(__name__)

THEMES = [
    "theme-purple",
    "theme-red",
    "theme-blue",
    "theme-green",
    "theme-yellow",
    "theme-magenta",
    "theme-cyan",
    "theme-black",
]


def roll_all():
    """Roll all dice for both languages. Returns a dict keyed by lang."""
    result = {}
    for lang in ("de", "en"):
        d = DICE[lang]
        result[lang] = {
            "article": random.choice(d["articles"]),
            "d1": random.choice(d["d1"]),
            "d2": random.choice(d["d2"]),
            "d3": random.choice(d["d3"]),
            "d4": random.choice(d["d4"]),
            "d5": random.choice(d["d5"]),
        }
    return result


@app.route("/")
def index():
    roll = roll_all()
    theme = random.choice(THEMES)
    response = make_response(render_template("index.html", roll=roll, theme=theme))
    response.headers["Cache-Control"] = "no-store"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
