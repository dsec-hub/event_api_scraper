from pydantic import BaseModel
from fastapi import FastAPI
from core.meetup_api import Meetup
from core.luma_api import Luma
from fastapi.responses import ORJSONResponse

app = FastAPI(default_response_class=ORJSONResponse)


class EventQueryMeetup(BaseModel):
    num_events_to_scrape: int
    date_range_to_scrape: int
    event_category_id: int

class EventQueryLuma(BaseModel):
    events_category: str
    events_to_scrape: int

@app.post("/meetup")
def query_meetup_events(event_query: EventQueryMeetup):
    meetup = Meetup(event_query.num_events_to_scrape,
                    event_query.date_range_to_scrape,
                    event_query.event_category_id)
    return meetup.call_meetup_api()

@app.post("/luma")
def query_luma_events(event_query: EventQueryLuma):
    luma = Luma(event_query.events_category,
                    event_query.events_to_scrape)
    return luma.call_luma_api()
