import requests
import ndjson as nd
import json
from datetime import datetime, timedelta
import time
import random


def chance(probability):
    return random.random() < probability


def generate_random_time_interval():
    hours = random.randint(3, 24)
    minutes = random.randint(0, 60)
    seconds = random.randint(0, 60)
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)


def complete_step3(data):
    previous_time = datetime.strptime(
        data['time_collected'], '%Y-%m-%d %H:%M:%S.%f')
    new_time = previous_time + generate_random_time_interval()
    step3 = {
        'event_ts': new_time.isoformat(),
        'order_id': data['order_id'],
        'driver_id': data['driver_id'],
        'time_ordered': data['time_ordered'],
        'time_collected': data['time_collected'],
        'time_at_depot': new_time.isoformat(),
        'time_with_driver': None,
        'time_delivered': None
    }
    return step3


def complete_step4(data):
    previous_time = datetime.strptime(
        data['time_at_depot'], '%Y-%m-%d %H:%M:%S.%f')
    new_time = previous_time + generate_random_time_interval()
    step4 = {
        'event_ts': new_time.isoformat(),
        'order_id': data['order_id'],
        'driver_id': data['driver_id'],
        'time_ordered': data['time_ordered'],
        'time_collected': data['time_collected'],
        'time_at_depot': data['time_at_depot'],
        'time_with_driver': new_time.isoformat(),
        'time_delivered': None
    }
    return step4


def complete_step5(data):
    previous_time = datetime.strptime(
        data['time_with_driver'], '%Y-%m-%d %H:%M:%S.%f')
    new_time = previous_time + generate_random_time_interval()
    step5 = {
        'event_ts': new_time.isoformat(),
        'order_id': data['order_id'],
        'driver_id': data['driver_id'],
        'time_ordered': data['time_ordered'],
        'time_collected': data['time_collected'],
        'time_at_depot': data['time_at_depot'],
        'time_with_driver': data['time_with_driver'],
        'time_delivered': new_time.isoformat()
    }
    return step5


def get_random_drivers(amount):
    params = {
        'token': 'p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICI1MmQxNjgzYS0xNDFmLTRjMDEtOGE3NS00MzkzODU0NmI4YTMifQ.H9DCLMYogwaj00pDN800pZOOVRMU4Pjc74kespmipL0',
        'limit': amount
    }

    url = f'https://api.tinybird.co/v0/pipes/random_driver_id.json'
    r = requests.get(url, params=params)
    if (r.status_code == 200):
        return r.json()['data']
    return None


def recover_state():
    params = {
        'token': 'p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICI4NjZhZjM4My0yZDdhLTQyMTQtYTM2NS0wNDZlNWQ0YTI1YzcifQ.T4jVJGdu0M5s2hzD74Ah2RxSt-84rGCJVDPqrBviIXU'
    }

    url = f'https://api.tinybird.co/v0/pipes/get_state_last_processed_time.json'
    response = requests.get(url, params=params)
    if (response.status_code == 200):
        return response.json()['data'][0]['time']
    return None


def send_state(time):
    data = json.dumps({
        'time': time,
    })

    r = requests.post('https://api.tinybird.co/v0/events',
                      params={
                          'name': 'state_last_processed_time',
                          'token': 'p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICI0NzQzZWRkYy02MzA4LTQ1MDUtOTc1YS1lZmIzMjQ1M2ZjNGYifQ.fCQZ6HYusIX9IfS3YRTLZOjxbwi9GSjyTA7uS6WoCB4',
                      },
                      data=data)

    if (r.status_code == 202):
        return True
    return False


def get_latest_orders(time):
    params = {
        'token': 'p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICI4ZjdkOTA4MC0wZjliLTQyZTYtYjcyNC04ZWY0ZWJjNjgxNjgifQ.l_xAFww7h8_rDzbRH5HHewNLWjgIBbCkXWTPopY26zo',
        'time_from': time
    }

    url = f'https://api.tinybird.co/v0/pipes/get_orders_since_time.json'
    r = requests.get(url, params=params)
    if (r.status_code == 200):
        return r.json()['data']
    return []


def send_parcel_events(orders):
    nd_data = nd.dumps(orders)
    r = requests.post('https://api.tinybird.co/v0/events',
                      params={
                          'name': 'parcel_tracking_events',
                          'token': 'p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICI0NzQzZWRkYy02MzA4LTQ1MDUtOTc1YS1lZmIzMjQ1M2ZjNGYifQ.fCQZ6HYusIX9IfS3YRTLZOjxbwi9GSjyTA7uS6WoCB4',
                      },
                      data=nd_data)


def process_new_orders(orders):
    drivers = get_random_drivers(len(orders)+10)
    batch = []
    for order in orders:
        if (chance(0.3)):
            continue
        driver_id = drivers.pop(0)
        order_time = datetime.strptime(
            order['time_ordered'], '%Y-%m-%d %H:%M:%S.%f')
        time_collected = order_time - generate_random_time_interval()
        next_step = {
            'event_ts': datetime.utcnow().isoformat(),
            'driver_id': driver_id['id'],
            'order_id': order['order_id'],
            'time_ordered': order['time_ordered'],
            'time_collected': time_collected.isoformat(),
            'time_at_depot': None,
            'time_with_driver': None,
            'time_delivered': None
        }
        batch.append(next_step)
    print(f'Sending {len(batch)} collected events.')
    send_parcel_events(batch)


def get_latest_events(amount):
    params = {
        'token': 'p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICJmZTliMGFkNC0zNWQzLTQwYWUtODA5YS1lNzgzNjRhNjlmZTEifQ.ugk1hgNlYURA6VarxYpk1gVu9sinrs-F4lN39IW6Y00',
        'limit': amount
    }

    url = f'https://api.tinybird.co/v0/pipes/get_incomplete_parcel_journies.json'
    r = requests.get(url, params=params)
    if (r.status_code == 200):
        return r.json()['data']
    return []


def process_new_events(events):
    batch = []
    for event in events:
        if (chance(0.3)):
            continue
        if event['time_at_depot'] == None:
            batch.append(complete_step3(event))
        elif event['time_with_driver'] == None:
            batch.append(complete_step4(event))
        elif event['time_delivered'] == None:
            batch.append(complete_step5(event))
    print(f'Sending {len(batch)} updated events.')
    send_parcel_events(batch)
    return


previous_time = recover_state()

if (not previous_time):
    now = datetime.utcnow()
    one_hour = timedelta(hours=1, minutes=0, seconds=0)
    previous_time = (now - one_hour).isoformat()

orders = []
while True:
    # Process new orders
    orders = get_latest_orders(previous_time)
    print(f'Got {len(orders)} new orders.')
    if (len(orders) > 0):
        process_new_orders(orders)
        last_seen_time = orders[-1]['time_ordered']
        send_state(last_seen_time)
        previous_time = last_seen_time
    # Process new tracking events
    events = get_latest_events(random.randint(200, 500))
    print(f'Got {len(events)} events.')
    if (len(events) > 0):
        process_new_events(events)
    time.sleep(1)
