from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

import timeit

start = timeit.default_timer()

COUNT = 0
def increment():
    global COUNT
    COUNT += 1
    if COUNT % 10000 == 0: print(f"Received {COUNT} messages.")
    

# TODO(developer)
project_id = "data-eng-scalzone"
subscription_id = "my-sub"
# Number of seconds the subscriber should listen for messages
timeout = 10.0

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    # print(f"Received {message}.")
    increment()
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.
        
print(f"Received {COUNT} messages.")
stop = timeit.default_timer()
print('Time: ', stop - start)  