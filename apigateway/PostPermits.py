import decimal
import json
import os

import boto3

from endpoints.permits import all_permits, get_permit


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


# A function to format the response
def respond(err, res=None, statusCode='200'):
    # if not custom_res:
        return {
            'statusCode': '400' if err else statusCode,
            'body': err.message if err else json.dumps(res, cls=DecimalEncoder),
            'headers': {
                'Content-Type': 'application/json',
            },
        }


# Function executed when API is called and returns results
def lambda_handler(event, context):
    http_method = event['requestContext']['httpMethod']
    proxy_in = event['pathParameters']['proxy']

    dynamo_table = os.environ['DYNAMOTABLE']

    # Only allow POST method
    if http_method != 'POST':
        return respond(None, {'message': http_method}, '405')

    if proxy_in.isnumeric():
        application_number = proxy_in
        try:
            items = get_permit(application_number)
            return respond(None, items)
        except Exception as e:
            return respond(e)

    if proxy_in == 'all-permits-json':
        dynamodb = boto3.resource('dynamodb')
        permits_table = dynamodb.Table(dynamo_table)
        try:
            items = all_permits(permits_table)
            return respond(None, items)
        except Exception as e:
            return respond(e)

