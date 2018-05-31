        credentials = TopicCredentials(
            self.settings.EVENT_GRID_KEY
        )
        event_grid_client = EventGridClient(credentials)
        event_grid_client.publish_events(
            "lmazuel-eventgrid-test.westus2-1.eventgrid.azure.net",
            events=[{
                'id' : "dbf93d79-3859-4cac-8055-51e3b6b54bea",
                'subject' : "My subject",
                'data': {
                    'key': 'I accept any kind of data here'
                },
                'event_type': 'PersonalEventType',
                'event_time': datetime(2018, 1, 30),
                'data_version': 1
            }]
        )