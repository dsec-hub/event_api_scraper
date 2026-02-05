import requests
from core.organizer import print_event_details_luma


class Luma():

    def __init__(self, events_category: str, num_events_to_scrape: int):
        self.events_category = events_category
        self.events_to_scrape = num_events_to_scrape


    def call_luma_api(self):
        url = "https://api2.luma.com/discover/get-paginated-events"
        
        querystring = {"latitude":"-37.8136",
                    "longitude":"144.9631",
                    "pagination_limit":f"{self.events_to_scrape}",
                    "slug":f"{self.events_category}"}


        headers = {
            "Accept-Encoding": "gzip, deflate, br, zstd"
        }

        response = requests.get(url, headers=headers, params=querystring)
        api_data = response.json()
        return print_event_details_luma(api_data)
