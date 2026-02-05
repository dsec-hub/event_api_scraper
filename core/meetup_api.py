import requests
from datetime import datetime, timedelta, date
from core.organizer import print_event_details_meetup



class Meetup():
    def __init__(self, num_events_to_scrape: int ,date_range_to_scrape: int,event_category_id: int):
        self.date_today = datetime.today().strftime('%Y-%m-%d')
        self.num_events_to_scrape = num_events_to_scrape 
        self.events_date_range = date_range_to_scrape
        self.events_category = event_category_id




    def get_date_offset(self, days: int) -> str:
        return (date.today() + timedelta(days=days)).isoformat()


    
    def call_meetup_api(self):
        end_date = self.get_date_offset(self.events_date_range)
        url = "https://www.meetup.com/gql2"

        payload = {
            "operationName": "recommendedEventsWithSeries",
            "variables": {
                "first": self.num_events_to_scrape,
                "lat": -37.8136,    #lat and long of melbourne city
                "lon": 144.9631,
                "topicCategoryId": f"{self.events_category}",
                "startDateRange": f"{self.date_today}T00:00:00+11:00",
                "endDateRange": f"{end_date}T23:59:59+11:00",
                "seriesStartDate": f"{self.date_today}",
                "sortField": "RELEVANCE" #RELEVANCE is the only field 


            },
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "cf6348a7edb376af58158519e78130eb8beced0aaaed60ab379e82f25fd52eea"
                }
            }
        }

        headers = {
                "Accept-Encoding": "gzip, deflate, br, zstd",
        }

        response = requests.post(url, json=payload, headers=headers)
        api_data = response.json()
        return print_event_details_meetup(api_data)
         


