from google.cloud import pubsub_v1
import json
import timeit
import urllib
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
import json
import datetime
import os
import timeit

url = 'https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id='

project_id = "data-eng-scalzone"
topic_id = "my-topic"

publisher = pubsub_v1.PublisherClient()
# The `topic_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/topics/{topic_id}`
topic_path = publisher.topic_path(project_id, topic_id)

# Read in the bus list from file
with open('vehicles.txt', 'r') as cars: vehicles = [bus.strip() for bus in cars.readlines()]

# Create a directory to store the day's data
date = datetime.datetime.now()
# if not os.path.exists(f'data/{date.year}/{date.month}/{date.day}'): os.makedirs(f'data/{date.year}/{date.month}/{date.day}')
if not os.path.exists(f'data/error/{date.year}/{date.month}'): os.makedirs(f'data/error/{date.year}/{date.month}')

# Create a function to log which busses failed to retrieve data
def log_print(error, bus):
    """Prints the error to console and logs the bus to a file."""
    print(error)
    with open(f'data/error/{date.year}/{date.month}/{date.day}.txt', 'a') as f: f.write(bus + '\n')

counter = 0
buses = 0
start = timeit.default_timer()
# Retrieve data for each bus
for bus in vehicles:
    if buses < 100:
        buses += 1
        print(f'GET: Bus {bus}')
        try:
            req = urllib.request.urlopen(url + bus)
            data = json.loads(req.read())
            for item in data:
                data_str = json.dumps(item)
                # Data must be a bytestring
                data = data_str.encode("utf-8")
                # When you publish a message, the client returns a future.
                future = publisher.publish(topic_path, data)
                counter += 1
                if counter % 10000 == 0: print(f"Sent {counter} messages.")
                # print(future.result())
            # with open(f'data/{date.year}/{date.month}/{date.day}/{bus}.json', 'w') as f: json.dump(data, f, indent=4) # Save bus data as JSON file
        except Exception as e: log_print(e, bus)
        except HTTPError as e: log_print(e, bus)
        except URLError as e: log_print(e, bus)
    
 
print(f"Sent {counter} messages.")
stop = timeit.default_timer()
print('Time: ', stop - start) 


# for n in range(1, 10):
#     data_str = f"Message number {n}"
#     # Data must be a bytestring
#     data = data_str.encode("utf-8")
#     # When you publish a message, the client returns a future.
#     future = publisher.publish(topic_path, data)
#     print(future.result())

# print(f"Published messages to {topic_path}.")