# CLAUDE.md — ct-generator

## What this is

A single-page Flask web app that rolls five D20 dice server-side and assembles an absurdist German/English conspiracy theory. No database, no sessions, no query parameters, no caching.

## Architecture in one paragraph

`app.py` has a single route (`GET /`). It calls `roll_all()` from `dice.py`, picks a random theme from `THEMES`, renders `templates/index.html` with Jinja2, and sets `Cache-Control: no-store`. Both DE and EN content are pre-rendered in the HTML; a CSS class on `<html data-lang="…">` hides the inactive language. Language preference is persisted via `localStorage` and applied via an inline IIFE in `<head>` before the body renders (prevents flash).

## Key design decisions

- **No client-side roll** — every new theory requires a round-trip to `/`. The roll button is an `<a href="/">`.
- **D2 and D3 are directly adjacent** with no space — they form a German compound word (`Pharma-Elite`). Do not add whitespace between `.s-d2` and `.s-d3` in the template.
- **Die accent colours are fixed** (defined in `:root`) and never change between themes. Only `--bg`, `--surface`, and `--text` vary per theme.
- **Explicit die classes** (`.die-art`, `.die-d1`–`.die-d5`) — not nth-child selectors.
- **English article** is always "The" (single-element list); the badge label is "D1" (not D3) because English has only one choice.
- **Disclaimer is always visible in both languages** — it uses no `.lang-de`/`.lang-en` class.

## Running

```bash
pip install flask
python app.py          # http://localhost:5000

pytest                 # 17 tests (requires pip install pytest)

docker compose up --build   # Docker alternative
```

## File map

| File | Responsibility |
|------|---------------|
| `app.py` | Flask app, single route, theme selection |
| `dice.py` | All dice data — `DICE["de"]` and `DICE["en"]`, each with `articles` + `d1`–`d5` (20 items each) |
| `templates/index.html` | Jinja2 template — bilingual, language toggle script |
| `static/style.css` | All styles — 8 theme classes, die colour vars, lang visibility |
| `tests/test_dice.py` | Dice data integrity (counts, no blanks, no duplicates) |
| `tests/test_app.py` | Flask integration tests (200, no-store header, theming, sentence structure) |
| `Dockerfile` / `docker-compose.yml` | Container deployment |

## Non-goals (do not add)

- User accounts / sessions
- Persistent storage
- API endpoints
- JavaScript framework
- Build step
- White or light colour themes
- Query parameters
- Client-side dice rolling
