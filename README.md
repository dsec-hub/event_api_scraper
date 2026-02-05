# event_api_scraper

Scrapes event listings from **Luma** and **Meetup** and returns a normalized JSON list via a small **FastAPI** service.

> Note: This project depends on third-party endpoints (Meetup’s GraphQL + Luma’s API). They may change or rate-limit without notice. Use responsibly and respect each provider’s Terms of Service.

---

## Contents

- [Features](#features)
- [Project structure](#project-structure)
- [Requirements](#requirements)
- [Setup](#setup)
- [Run the API](#run-the-api)
- [API reference](#api-reference)
  - [POST /meetup](#post-meetup)
  - [POST /luma](#post-luma)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **FastAPI** HTTP service
- Two providers:
  - **Meetup** (GraphQL recommended events query)
  - **Luma** (discover paginated events)
- Normalizes provider responses into a consistent “event list” shape
- Defaults to **Melbourne CBD** coordinates (easy to change)

---

## Project structure

~~~text
event_api_scraper/
├── core/
│   ├── luma_api.py
│   ├── meetup_api.py
│   └── organizer.py
├── .gitignore
├── README.md
└── main.py
~~~

---

## Requirements

- Python **3.10+** recommended
- Packages used by the current code:
  - `fastapi`
  - `uvicorn[standard]`
  - `requests`
  - `pandas`
  - `orjson`
  - `pydantic`

---

## Setup

~~~bash
git clone https://github.com/dsec-hub/event_api_scraper.git
cd event_api_scraper

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -U pip
pip install fastapi uvicorn[standard] requests pandas orjson pydantic
~~~

---

## Run the API

~~~bash
uvicorn main:app --reload
~~~

Open:
- API base: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## API reference

### POST /meetup

Fetch events from Meetup using a persisted GraphQL query (recommended events).
As of now here are the category ids and following category:

**Category IDs**
~~~json
{
  "New Groups": 999,
  "Social Activites": 652,
  "Hobbies & Passion": 571,
  "Sports & Fitness": 482,
  "Travel & Outdoor": 684,
  "Career & Business": 405,
  "Technology":546,
  "Community & Environment": 604,
  "Identity & Language": 622,
  "Games": 535,
  "Dancing": 612,
  "Support & Coaching": 449,
  "Music": 395,
  "Health & WellBeing": 511,
  "Art & Culture": 521,
  "Science & Education": 436,
  "Pets & Animals": 701,
  "Religion & Spirtuality": 593,
  "Writing": 467,
  "Parents & Family": 673,
  "Movement & Politics": 642
}
~~~


**Request body**
~~~json
{
  "num_events_to_scrape": 20,
  "date_range_to_scrape": 14,
  "event_category_id": 546
}
~~~

**Fields**
- `num_events_to_scrape` — number of results requested from Meetup
- `date_range_to_scrape` — number of days into the future to include
- `event_category_id` — Meetup topic category id

**Example**
~~~bash
curl -X POST "http://127.0.0.1:8000/meetup" \
  -H "Content-Type: application/json" \
  -d '{
    "num_events_to_scrape": 10,
    "date_range_to_scrape": 30,
    "event_category_id": 546
  }'
~~~

**Response (example shape)**
~~~json
[
  {
    "Title": "Example Meetup Event",
    "Date/Time": "2026-02-20T07:00:00+11:00",
    "Price": null,
    "organizers": "Example Group",
    "location": "AU Melbourne 123 Example St Example Venue",
    "rating": 4.6
  }
]
~~~

**Notes**
- `Price` is currently the raw `feeSettings` object from the Meetup payload (often `null` or a nested structure).
- `location` is built by concatenating: `country + city + address + venue name`.

---

### POST /luma

Fetch events from Luma’s discover endpoint.

**Request body**
~~~json
{
  "events_category": "tech",
  "events_to_scrape": 20
}
~~~

**Fields**
- `events_category` — Luma category slug (e.g. `tech`)
- `events_to_scrape` — number of results requested from Luma

**Example**
~~~bash
curl -X POST "http://127.0.0.1:8000/luma" \
  -H "Content-Type: application/json" \
  -d '{
    "events_category": "tech",
    "events_to_scrape": 10
  }'
~~~

**Response (example shape)**
~~~json
[
  {
    "Title": "Example Luma Event",
    "Date/Time": "2026-02-20T18:00:00+11:00",
    "Price": 0,
    "organizers": "Example Host",
    "map coordinates": "-37.8136,144.9631",
    "location": "Melbourne VIC, Australia"
  }
]
~~~

**Notes**
- `Price` is currently `ticket_info.price.cents` (an integer amount in cents, when present).
- Dates are parsed as UTC then converted to `Australia/Melbourne`.

---

## Configuration

### Change the search location (lat/lon)

Both providers are currently hardcoded to Melbourne CBD:
- Meetup: `lat=-37.8136`, `lon=144.9631` in `core/meetup_api.py`
- Luma: `latitude=-37.8136`, `longitude=144.9631` in `core/luma_api.py`

To make this configurable, a common next step is:
- add env vars (e.g. `EVENT_LAT`, `EVENT_LON`)
- read them in `main.py` and pass them into each provider class

---

## Troubleshooting

- **Empty results**
  - Provider may be rate-limiting or returning no events for that category/date range.
  - Try lowering `num_events_to_scrape` / `events_to_scrape` and widening the date range.

- **500 errors**
  - External payload shape may have changed.
  - Add basic logging around `response.status_code` and `response.text` in provider calls.

- **Inconsistent “Price”**
  - Meetup and Luma represent pricing differently; currently this service returns “raw-ish” provider values.
  - If you need a unified price model, normalize to:
    - `currency`, `amount`, `is_free`, `pricing_notes`

---

## Contributing

PRs welcome. If you add a new provider:
- keep provider-specific logic in `core/<provider>_api.py`
- add a normalizer in `core/organizer.py`
- expose it via a route in `main.py`

---

## License

MIT License