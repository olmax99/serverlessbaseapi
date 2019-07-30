import json
from models import PermitsModel

Permits = PermitsModel('eu-central-1', 'https://dynamodb.eu-central-1.amazonaws.com')


# A function to format the response
def respond(err, res=None, statusCode='200'):
    return {
        'statusCode': '400' if err else statusCode,
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


# A function to query permits by partition key (application_number)
def get_items(application_number):
    items = []
    app_num = '#' + str(application_number)

    for item in Permits.query(app_num):
        items.append(dict(item))

    return items


# Function executed when API is called and returns results
def lambda_handler(event, context):
    httpMethod = event['requestContext']['httpMethod']
    application_number = event['pathParameters']['proxy']

    # Only allow POST method
    if httpMethod != 'POST':
        return respond(None, {'message': httpMethod}, '405')

    try:
        items = get_items(application_number)
        return respond(None, items)

    except Exception as e:
        return respond(e)
