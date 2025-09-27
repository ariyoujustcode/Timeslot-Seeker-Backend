# Timeslot Seeker — CLI Tool

A small, focused command-line tool to find common free meeting slots across multiple Google Calendar accounts. It queries the Google Calendar Free/Busy API, merges busy intervals across participants, and returns available meeting times restricted to working hours (default 9:00–17:00 local time) on weekdays.

This repository contains a lightweight Python CLI (`main.py`) intended for local use by teams who share Google Calendars and want to quickly discover overlapping free windows for meetings.

## Features

-   Query multiple Google Calendar accounts using the Free/Busy API
-   Merge overlapping busy intervals across participants
-   Respect configurable working hours (defaults to 9:00–17:00 local)
-   Only returns full meeting slots (30 or 60 minutes) that are fully inside work hours
-   Skip weekends

## Table of contents

-   [Requirements](#requirements)
-   [Installation](#installation)
-   [Configuration](#configuration)
-   [Usage](#usage)
-   [Examples](#examples)
-   [Testing](#testing)
-   [Customization](#customization)
-   [Troubleshooting](#troubleshooting)
-   [Contributing](#contributing)
-   [License](#license)

## Requirements

-   Python 3.10+ (3.11 recommended)
-   When using Google Calendar integration: install the Google auth and API libraries (see below)

Optional dev/test tools:

-   pytest (for running tests)

## Installation

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install runtime dependencies (when you want to use Google Calendar integration):

```bash
pip install --upgrade pip
pip install google-auth google-auth-oauthlib google-api-python-client tabulate
```

3. (Optional) Install dev/test dependencies:

```bash
pip install pytest
```

## Configuration

This tool uses OAuth2 to access Google Calendar data. You need a `credentials.json` from the Google Cloud Console and the project must have the Google Calendar API enabled.

1. Create OAuth credentials (Desktop app) in the Google Cloud Console.
2. Download the `credentials.json` file and place it in this repository root (this file is listed in `.gitignore` — do not commit it).
3. On first run, the tool will open a browser window to authorize and will store tokens in `token.json` (also ignored).

Scope used: `https://www.googleapis.com/auth/calendar.readonly`

## Usage

Run the CLI with Python:

```bash
python3 main.py
```

The program will prompt you for:

-   Participant emails (comma-separated) — these can be any calendar IDs accessible to the authorized account(s)
-   Meeting length (30 or 60 minutes)
-   Time period (1–4 weeks)

The output is a tabulated list of dates, day names, and time ranges (local timezone), filtered to weekdays and the configured work hours.

### Note on running without Google credentials

If you don't have the Google libraries or credentials installed, `main.py` contains a small simulation mode that can be used to validate slot-clipping behavior locally. When prompted whether to run the full program, answer `n` to run the simulation.

## Examples

Typical session:

```
Enter participant emails, separated by commas: alice@example.com, bob@example.com
Enter meeting length (30 or 60 minutes): 60
Enter time period (1, 2, 3, or 4 weeks): 2

Finding available meeting slots...

+------------+------------+---------------------+
| Date       | Day        | Time                |
+------------+------------+---------------------+
| 09/30/25   | Tuesday    | 02:00 PM - 03:00 PM |
| 10/01/25   | Wednesday  | 09:00 AM - 10:00 AM |
+------------+------------+---------------------+
```

## Testing

There is a small test script `test_slots.py` that simulates a free interval crossing the 17:00 boundary to ensure no returned meeting slot extends past the working day. Run it directly:

```bash
python3 test_slots.py
```

For full unit-test support, I can add pytest-based tests on request.

## Customization

-   `WORK_START_HOUR` and `WORK_END_HOUR` are defined at the top of `main.py`. Adjust them to change working hours.
-   The script currently returns only full-length meeting slots (30 or 60 minutes). If you want truncated or partial slots (e.g., 45-minute from 16:15–17:00), I can add that behavior.

## Troubleshooting

-   Missing Google libraries error: install the dependencies listed in the [Installation](#installation) section.
-   Authentication issues: make sure `credentials.json` matches a desktop OAuth client and Calendar API is enabled in the Google Cloud Console.
-   Timezone oddities: the tool converts calendar times to UTC internally and evaluates work hours in the local timezone — if you need a fixed timezone, I can add a configuration parameter for that.

## Contributing

Contributions, issues, and feature requests are welcome. If you'd like to contribute:

1. Fork the repo
2. Create a feature branch
3. Open a PR with a clear description and tests for new behavior

## License

This project is provided under the MIT license. See `LICENSE` for details (if present).

---

If you'd like, I can:

-   Add a `requirements.txt` or `pyproject.toml` for reproducible installs
-   Add pytest test cases and a GitHub Actions workflow to run tests on PRs
-   Add more detailed examples or a quick-start script to automate OAuth token creation

Tell me which of the above you'd like next and I will add it.
