import pandas as pd

def print_event_details_meetup(data):

    df = pd.json_normalize(data['data'], ['result','edges'])

    title = df['node.title']
    price = df['node.feeSettings']
    organizers = df['node.group.name']
    datetime = df['node.dateTime']
    address = df['node.venue.address']
    city = df['node.venue.city']
    country = df['node.venue.country']
    name = df['node.venue.name']
    rating = df['node.group.stats.eventRatings.average']
    event_details_data = {
        'Title': title,
        'Date/Time': datetime,
        'Price': price,
        'organizers': organizers,
        'location': country + ' ' + city + ' ' + address + ' ' + name,
        'rating': rating 
    } 
    event_details_df = pd.DataFrame(event_details_data)
    return event_details_df.to_dict(orient='records')



def print_event_details_luma(data):

    df = pd.json_normalize(data['entries'])

    title = df['event.name']
    price = df["ticket_info.price.cents"]
    
    organizers = df['hosts'].str[0].str['name']
    datetime = pd.to_datetime(df['event.start_at'], utc=True).dt.tz_convert("Australia/Melbourne")

    latitude = df['event.coordinate.latitude']
    longitude = df['event.coordinate.longitude']

    address = df['event.geo_address_info.city_state']
    full_address = df['event.geo_address_info.full_address'].combine_first(address)
    event_details_data = {
        'Title': title,
        'Date/Time': datetime,
        'Price': price,
        'organizers': organizers,
        'map coordinates': latitude.astype(str) + "," + longitude.astype(str),
        'location': full_address
    } 
    event_details_df = pd.DataFrame(event_details_data)

    return event_details_df.to_dict(orient='records')

