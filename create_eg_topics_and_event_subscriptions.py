import logging
import os
import time
import uuid
from haikunator import Haikunator

from azure.common.credentials import ServicePrincipalCredentials

from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.eventgrid import EventGridManagementClient
from azure.mgmt.eventgrid.models import Topic, EventSubscriptionFilter, EventSubscription, EventSubscriptionDestination, WebHookEventSubscriptionDestination

# If you wish to debug
# logging.basicConfig(level=logging.DEBUG)

_haikunator = Haikunator()

# Resource

LOCATION = 'westus'
GROUP_NAME = 'event-grid-python-sample-rg'

# Event grid

# Using a random topic name. Optionally, replace this with a topic name of your choice.
TOPIC_NAME = "topicsample-" + _haikunator.haikunate(delimiter='')

# Replace the endpoint URL with the URL of your Azure function, or whatever endpoint you want to sent the event.
# See the EventGridConsumer sample for a sample of an Azure function that can handle EventGridEvents
# Publish the EventGridConsumer sample as an Azure function and use the URL of that function for the below.
#
# Your endpoint will be validated, see https://aka.ms/esvalidation for details
ENDPOINT_URL = "replace with your Azure function-URL that support validation"


# To run the sample, you must first create an Azure service principal. To create the service principal, follow one of these guides:
# Azure Portal: https://azure.microsoft.com/documentation/articles/resource-group-create-service-principal-portal/)
# PowerShell: https://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal/
# Azure CLI: https://azure.microsoft.com/documentation/articles/resource-group-authenticate-service-principal-cli/
#
# This script expects that the following environment vars are set:
#
# AZURE_TENANT_ID: with your Azure Active Directory tenant id or domain
# AZURE_CLIENT_ID: with your Azure Active Directory Application Client ID
# AZURE_CLIENT_SECRET: with your Azure Active Directory Application Secret
# AZURE_SUBSCRIPTION_ID: with your Azure Subscription Id
#
def run_example():
    """Resource Group management example."""
    #
    # Create the Resource Manager Client with an Application (service principal) token provider
    #
    subscription_id = os.environ.get(
        'AZURE_SUBSCRIPTION_ID',
        '11111111-1111-1111-1111-111111111111') # your Azure Subscription Id
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    resource_client = ResourceManagementClient(credentials, subscription_id)
    event_grid_client = EventGridManagementClient(credentials, subscription_id)

    # Create Resource group
    print('\nCreating a Resource Group...')
    resource_group = resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {'location': LOCATION}
    )
    print_item(resource_group)

    # Create EventGrid topic
    print('\nCreating an EventGrid topic...')
    topic_result_async_poller = event_grid_client.topics.create_or_update(
        resource_group.name,
        TOPIC_NAME,
        location=resource_group.location,
        tags={'key1': 'value1', 'key2': 'value2'},
    )
    # Blocking call for the Topic to be created
    topic = topic_result_async_poller.result()  # type: Topic
    print_item(topic)

    # Get the keys for the topic
    print('\nGetting the topic keys...')
    keys = event_grid_client.topics.list_shared_access_keys(  # type: TopicSharedAccessKeys
        resource_group.name,
        topic.name
    )
    print('The key1 value of topic {} is: {}'.format(topic.name, keys.key1))

    # Create an event subscription
    print('\nCreating an event subscription')
    event_subscription_name = 'EventSubscription1'
    destination = WebHookEventSubscriptionDestination(
        endpoint_url=ENDPOINT_URL
    )
    filter = EventSubscriptionFilter(
        # By default, "All" event types are included
        is_subject_case_sensitive=False,
        subject_begins_with='',
        subject_ends_with=''
    )

    event_subscription_info = EventSubscription(destination=destination, filter=filter)

    event_subscription_async_poller = event_grid_client.event_subscriptions.create_or_update(
        topic.id,
        event_subscription_name,
        event_subscription_info,
    )
    # Blocking call for the EventSubscription to be created
    event_subscription = event_subscription_async_poller.result()  # type: EventSubscription
    print_item(event_subscription)

    input("Press enter to delete all created resources.")

    # Delete the EventSubscription
    print('\nDeleting the event subscription')
    delete_async_operation = event_grid_client.event_subscriptions.delete(
        topic.id,
        event_subscription_name
    )
    delete_async_operation.wait()
    print("\nDeleted: {}".format(event_subscription_name))

    # Delete the topic
    print('\nDeleting the topic')
    delete_async_operation = event_grid_client.topics.delete(
        resource_group.name,
        topic.name
    )
    delete_async_operation.wait()
    print("\nDeleted: {}".format(topic.name))

    # Delete Resource group and everything in it
    print('\nDelete Resource Group')
    delete_async_operation = resource_client.resource_groups.delete(GROUP_NAME)
    delete_async_operation.wait()
    print("\nDeleted: {}".format(GROUP_NAME))

def print_item(group):
    """Print a ResourceGroup instance."""
    print("\tName: {}".format(group.name))
    print("\tId: {}".format(group.id))
    if hasattr(group, 'location'):
        print("\tLocation: {}".format(group.location))
    print_properties(getattr(group, 'properties', None))

def print_properties(props):
    """Print a ResourceGroup propertyies instance."""
    if props and hasattr(props, 'provisioning_state'):
        print("\tProperties:")
        print("\t\tProvisioning State: {}".format(props.provisioning_state))
    print("\n\n")

if __name__ == "__main__":
    run_example()