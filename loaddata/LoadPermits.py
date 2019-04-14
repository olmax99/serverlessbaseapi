import boto3
import urllib
import pyexcel as pe
from pynamodb.connection import Connection

# database permit model
from models import PermitsModel

# Our created utils
from utils import (write_records, create_permit, adjustCapacity)


s3 = boto3.client('s3')
Permits = PermitsModel('eu-central-1', 'https://dynamodb.eu-central-1.amazonaws.com')
conn = Connection(region='eu-central-1', host='https://dynamodb.eu-central-1.amazonaws.com')


def lambda_handler(event, context):
    # set temp file
    # '/tmp' is directory to write to inside Lambda function container
    report_file = '/tmp/report.xlsx'

    # Get bucket and key from PUT event
    bucket = event['Records'][0]['s3']['bucket']['name'].encode('utf8')
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))

    # Create DynamoDB table if it does not exist
    if not Permits.exists():
        Permits.create_table(wait=True)

    try:
        # Download excel file of permits
        with open(report_file, 'wb') as report:
            s3.download_fileobj(bucket, key, report)

        # expand table capacity during load
        adjustCapacity(conn, 'permits-27-sam', 50, 50)

        # parse records
        records = pe.iget_records(file_name=report_file)

        # write records to 'permits' table
        write_records(records, create_permit, Permits)

        # decrease table capacity after load
        adjustCapacity(conn, 'permits-27-sam', 5, 5)

    except Exception as e:
        adjustCapacity(conn, 'permits-27-sam', 5, 5)
        print 'handler error: ', e

    finally:
        return "load complete"
