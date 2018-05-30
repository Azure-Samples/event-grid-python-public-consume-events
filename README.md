---
services: event-grid
platforms: python
author: kalyanaj, lmazuel
---

# Microsoft Azure Event Grid Publish/Consume Samples for Python

This contains Python samples for publishing events to Azure Event Grid and consuming events from Azure Event Grid. It also contains a set of management samples that demonstrates how to manage topics and event subscriptions.

## Features

These samples demonstrates the following features:

Data Plane:

* How to publish events to Azure Event Grid.
* How to consume events delivered by Azure Event Grid.

The above two samples use the Event Grid data plane SDK [azure-eventgrid](https://pypi.org/project/azure-eventgrid/).

Management Plane:

* How to create a topic and an event subscription to a topic.
* How to create an event subscription to a Storage account.
* How to create an event subscription to an Azure subscription / Resource Group.

The above three samples use the Event Grid management plane SDK [azure-mgmt-eventgrid](https://pypi.org/project/azure-mgmt-eventgrid/)

## Getting Started

### Prerequisites

- Python 2.7, 3.4 or higher.
- [Pipenv](https://docs.pipenv.org/). If you don't have it, follow the [pipenv installation tutorial](https://docs.pipenv.org/#install-pipenv-today).


### Quickstart

1. git clone https://github.com/Azure-Samples/event-grid-python-public-consume-events.git
2. cd event-grid-python-public-consume-events
3. pipenv install
4. For Management only, rename the file `env_template` to `.env` and update the correct values inside with your
   subscription ID and [Azure Service Principal credentials](https://docs.microsoft.com/azure/azure-resource-manager/resource-group-create-service-principal-portal).

## Running the samples

# Management

`create_eg_topics_and_event_subscriptions.py` will create an EventGrid on Azure, a Topic, and a EventSubscription. 

In order for this sample to work, you will need to have a valid `.env` file (see previous section).

Run the sample : `pipenv run create_eg_topics_and_event_subscriptions.py`

# Data plane

## Resources

- https://docs.microsoft.com/azure/event-grid/overview
- https://docs.microsoft.com/python/api/overview/azure/event-grid
