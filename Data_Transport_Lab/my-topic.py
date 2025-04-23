from google.cloud import pubsub_v1
import json
import timeit
import urllib
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
import json
import datetime
import os
url = 'https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id='


# TODO(developer)
project_id = "data-eng-scalzone"
topic_id = "my-topic"
# with open('vehicles.txt', 'r') as cars: vehicles = [bus.strip() for bus in cars.readlines()]


# publisher = pubsub_v1.PublisherClient()
# # # The `topic_path` method creates a fully qualified identifier
# # # in the form `projects/{project_id}/topics/{topic_id}`
# # topic_path = publisher.topic_path(project_id, topic_id)
# counter = 0
# with open('all_bus_data.json', 'r') as f:
#     data = json.load(f)
# print(data)
# start = timeit.default_timer()
# for item in data:
#     data_str = json.dumps(item)
#     # Data must be a bytestring
#     data = data_str.encode("utf-8")
#     # When you publish a message, the client returns a future.
#     future = publisher.publish(topic_path, data)
#     print(future.result())
#     counter += 1

# print(f"Sent {counter} messages.")
# stop = timeit.default_timer()
# print('Time: ', stop - start)  


# print(f"Published messages to {topic_path}.")

# with open('vehicles.txt', 'r') as cars: vehicles = [bus.strip() for bus in cars.readlines()]

vehicles = [2902]

# Retrieve data for each bus

f = open(f'all_bus_data.json', 'w')
all_data = []
for bus in vehicles:
    bus = str(bus)
    print(f'GET: Bus {bus}')
    try:
        path = url+bus
        print(path)
        req = urllib.request.urlopen(url + bus)
        data = json.loads(req.read())
        all_data.append(data)
        
          #with open(f'bc_sample_{bus}.json', 'w') as f: json.dump(data, f, indent=4) # Save bus data as JSON file
        # json.dump(data, f, indent=4) # Save bus data as JSON file
    except Exception as e: print(e, bus)
    except HTTPError as e: print(e, bus)
    except URLError as e: print(e, bus)

print(all_data[0][0])
to_json
for i in range(10):
    print(all_data[0][i])
json.dump(all_data[0], f, indent=4)
    
  
# json.dump(all_data, f, indent=4)


# for bus in vehicles:
#     bus = str(bus)
#     # with open(f'bc_sample_{bus}.json', 'r') as f: data = json.load(f)
#     for item in data:
#         data_str = json.dumps(item)
#         # Data must be a bytestring
#         data = data_str.encode("utf-8")
#         # When you publish a message, the client returns a future.
#         future = publisher.publish(topic_path, data)
#         print(future.result())
#         counter += 1




# for n in range(1, 10):
#     data_str = f"Message number {n}"
#     # Data must be a bytestring
#     data = data_str.encode("utf-8")
#     # When you publish a message, the client returns a future.
#     future = publisher.publish(topic_path, data)
#     print(future.result())

# print(f"Published messages to {topic_path}.")


# import urllib
# from urllib.error import HTTPError, URLError
# from urllib.request import urlopen
# import json
# import datetime
# import os
# url = 'https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id='

# Read in the bus list from file
# with open('vehicles.txt', 'r') as cars: vehicles = [bus.strip() for bus in cars.readlines()]


# # # Create a directory to store the day's data
# # date = datetime.datetime.now()
# # if not os.path.exists(f'data/{date.year}/{date.month}/{date.day}'): os.makedirs(f'data/{date.year}/{date.month}/{date.day}')
# # if not os.path.exists(f'data/error/{date.year}/{date.month}'): os.makedirs(f'data/error/{date.year}/{date.month}')

# # # Create a function to log which busses failed to retrieve data
# # def log_print(error, bus):
# #     """Prints the error to console and logs the bus to a file."""
# #     print(error)
# #     with open(f'data/error/{date.year}/{date.month}/{date.day}.txt', 'a') as f: f.write(bus + '\n')

# Retrieve data for each bus
# f = open(f'all_bus_data.json', 'w')
# for bus in vehicles:
#     bus = str(bus)
#     print(f'GET: Bus {bus}')
#     try:
#         path = url+bus
#         print(path)
#         req = urllib.request.urlopen(url + bus)
#         data = json.loads(req.read())
#         # print(data)
          # #with open(f'bc_sample_{bus}.json', 'w') as f: json.dump(data, f, indent=4) # Save bus data as JSON file
#         json.dump(data, f, indent=4) # Save bus data as JSON file
#     except Exception as e: print(e, bus)
#     except HTTPError as e: print(e, bus)
#     except URLError as e: print(e, bus)