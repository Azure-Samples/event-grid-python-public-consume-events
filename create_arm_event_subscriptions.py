import os
from haikunator import Haikunator

from azure.common.credentials import ServicePrincipalCredentials

from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.eventgrid import EventGridManagementClient
from azure.mgmt.eventgrid.models import Topic, EventSubscriptionFilter, EventSubscription, StorageQueueEventSubscriptionDestination

# If you wish to debug
# import logging
# logging.basicConfig(level=logging.DEBUG)

_haikunator = Haikunator()

# Resource

LOCATION = 'westus'
GROUP_NAME = 'event-grid-python-sample-rg'

# Event grid

# Using a random topic name. Optionally, replace this with a topic name of your choice.
TOPIC_NAME = "topicsample-" + _haikunator.haikunate(delimiter='')

# In this sample, we will be demonstrating using a storage queue as the destination for the event subscription.
# This should be in the format /subscriptions/id/resourceGroups/rg/providers/Microsoft.Storage/storageAccounts/account1
# More info on Storage queue as an event handler is at https://docs.microsoft.com/en-us/azure/event-grid/event-handlers#queue-storage
STORAGE_ACOUNT_RESOURCE_ID = 'replace-with-your-storage-account-resource-id'
QUEUE_NAME = 'replace-with-your-queue-name-under-the-above-storage-account'

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

    # Creating an event subscription to storage account {StorageAccountResourceId} with destination as {HybridConnectionResourceId}
    print('\nCreating an event subscription to storage account {} with destination as {}'.format(STORAGE_ACOUNT_RESOURCE_ID, QUEUE_NAME))

    # Scope could be any ARM resource ID that supports EventGrid
    # https://docs.microsoft.com/azure/event-grid/event-sources
    scope = "/subscriptions/{}".format(subscription_id)
    event_subscription_name = 'EventSubscription1'
    destination = StorageQueueEventSubscriptionDestination(
        resource_id=STORAGE_ACOUNT_RESOURCE_ID,
        queue_name=QUEUE_NAME
    )
    filter = EventSubscriptionFilter(
        # By default, "All" event types are included
        is_subject_case_sensitive=False,
        subject_begins_with='',
        subject_ends_with=''
    )

    event_subscription_info = EventSubscription(destination=destination, filter=filter)

    event_subscription_async_poller = event_grid_client.event_subscriptions.create_or_update(
        scope,
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
        scope,
        event_subscription_name
    )
    delete_async_operation.wait()
    print("\nDeleted: {}".format(event_subscription_name))

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