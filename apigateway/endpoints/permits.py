
import decimal
import json

from models.permits import PermitsModel

Permits = PermitsModel('eu-central-1', 'https://dynamodb.eu-central-1.amazonaws.com')


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def get_permit(application_number):
    """
    A function to query permits by partition key (application_number)
    :param application_number:
    :return:
    """
    items = []
    app_num = '#' + str(application_number)

    for item in Permits.query(app_num):
        items.append(dict(item))

    return items


def all_permits(target_dynamo_table):
    """
    Simply return all data from DynamoDb Table
    :param target_dynamo_table:
    :return:
    """
    response = target_dynamo_table.scan()
    data = response['Items']

    while response.get('LastEvaluatedKey', False):
        response = target_dynamo_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return json.dumps(data, cls=DecimalEncoder)