import os
import json

# This code is designed for Python Function to pass event subscription validation as described here:
# https://aka.ms/esvalidation

postreqdata = json.loads(open(os.environ['req']).read())
response = open(os.environ['res'], 'w')
for event in postreqdata:
    if event['eventType'] == "Microsoft.EventGrid.SubscriptionValidationEvent":
        validation_code = event['data']['validationCode']
        answer_payload = {
            "validationResponse": validation_code
        }
        response.write(json.dumps(answer_payload))
        break
response.close()