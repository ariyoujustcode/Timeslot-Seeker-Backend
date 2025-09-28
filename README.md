# Timeslot Seeker — FastAPI backend

This repository is now a backend service (FastAPI) that provides endpoints to find common free meeting slots across multiple Google Calendar accounts. The user-facing GUI is implemented in a separate frontend repository; this backend exposes JSON APIs that the frontend consumes.

Highlights:

-   FastAPI-based JSON API (instead of a CLI)
-   Google Calendar Free/Busy integration
-   Working-hours-aware slot generation (defaults to 9:00–17:00 local)
-   Weekday-only results and overlap merging

If you previously used the command-line tool, note that the code has been reorganized into an API-first backend.

## Quick links

-   Backend entry: `main.py` (FastAPI app)
-   API router(s): `app/api.py`
-   Frontend: see the companion frontend repository (add link or repo name here)

## Table of contents

-   [Requirements](#requirements)
-   [Installation](#installation)
-   [Configuration](#configuration)
-   [Running the server](#running-the-server)
-   [API overview](#api-overview)
-   [Development & testing](#development--testing)
-   [Customization](#customization)
-   [Troubleshooting](#troubleshooting)
-   [Contributing](#contributing)
-   [License](#license)

## Requirements

-   Python 3.10+ (3.11 recommended)
-   `requirements.txt` includes runtime dependencies (FastAPI, uvicorn, Google auth packages)

## Installation

Recommended: create and activate a virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

The backend uses Google OAuth2 to access calendars. Place `credentials.json` (from Google Cloud Console) in the repo root; the app will create `token.json` after the first successful OAuth flow.

1. Create OAuth credentials (Desktop or Web application) in Google Cloud Console and enable the Calendar API.
2. Download `credentials.json` and place it in the backend repo root (do not commit it).

Secrets like client IDs and refresh tokens are stored in `token.json` locally. For deployments, consider using environment secrets or a secrets manager.

## Running the server

Run locally during development with uvicorn:

```bash
uvicorn main:app --reload --port 8000
```

The server will expose a live OpenAPI docs UI at `http://localhost:8000/docs` where you can try the endpoints interactively.

## API overview

See the live docs at `/docs` or `/redoc` for full interactive API docs. Key endpoints include:

-   `POST /find_slots` — Accepts participants, meeting length and range, returns available time slots.
-   `GET /health` — Simple healthcheck.

Example request body for `POST /find_slots`:

```json
{
    "participants": ["alice@example.com", "bob@example.com"],
    "slot_length": 60,
    "weeks": 2
}
```

The response is JSON with an array of slot objects (UTC + local representations where applicable).

## Development & testing

-   A small test script (`test_slots.py`) is included for local validation of the scheduling logic.
-   To run unit tests (once added) run:

```bash
pytest
```

## Customization

-   Change `WORK_START_HOUR` and `WORK_END_HOUR` in `main.py` to customize working hours.
-   The API currently returns full-length meeting slots only. If you want to support partial/truncated slots, we can add an option in the API payload.

## Troubleshooting

-   If the server fails to start, ensure dependencies from `requirements.txt` are installed and that `uvicorn` is available.
-   Authentication errors: verify `credentials.json` and Google Calendar API enablement.

## Frontend

This repo is the backend only. The user-facing GUI is implemented in a separate frontend repository (link/name). The frontend calls the backend API to display available slots and schedule meetings.

If you want, I can add a README section linking to the frontend repo, or add a small integration test that performs a mock request from the frontend.

## Contributing

Contributions are welcome. Please open issues or PRs and include tests and documentation changes.

## License

MIT — see `LICENSE` if present.
