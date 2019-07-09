import datetime
import uuid

from msrest.authentication import TopicCredentials
from azure.eventgrid import EventGridClient
from azure.eventgrid.models import EventGridEvent

# If you wish to debug
# import logging
# logging.basicConfig(level=logging.DEBUG)

# Enter values for <topic-name> and <region>
TOPIC_ENDPOINT = "<topic-name>.<region>-1.eventgrid.azure.net"

# Enter value for <topic-key>
EVENT_GRID_KEY = '<topic-key>'


def build_events_list():
    # type: () -> List[EventGridEvent]
    result = []
    for i in range(1):
        result.append(EventGridEvent(
            id=uuid.uuid4(),
            subject="My subject {}".format(i),
            data={
                'key': 'I accept any kind of data here, this is a free dictionary'
            },
            event_type='PersonalEventType',
            event_time=datetime.datetime.now(),
            data_version=2.0
        ))
    return result


def run_example():

    credentials = TopicCredentials(
        EVENT_GRID_KEY
    )
    event_grid_client = EventGridClient(credentials)
    event_grid_client.publish_events(
        TOPIC_ENDPOINT,
        events=build_events_list()
    )
    print("Published events to Event Grid.")


if __name__ == "__main__":
    run_example()
()
