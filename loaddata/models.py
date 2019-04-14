from pynamodb.models import Model
from pynamodb.attributes import (UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute)


# This function creates a new class to create permits
# to load into the DynamoDB permits table

def PermitsModel(db_region='', db_host='http://localhost:8000'):

    # See the docs on creating a model
    # http://pynamodb.readthedocs.io/en/latest/tutorial.html

    class PermitClass(Model):
        class Meta:
            table_name = 'permits-27-sam'
            read_capacity_units = 5
            write_capacity_units = 5
            region = db_region
            host = db_host

        # set the partion key
        application_number = UnicodeAttribute(hash_key=True)

        # set the sort key
        record_id = NumberAttribute(range_key=True)

        # define other expected attributes
        # UTCDateTimeAttribute into a UnicodeAttribute
        status = UnicodeAttribute(default='issued')
        status_date = UTCDateTimeAttribute(null=True)
        file_date = UTCDateTimeAttribute(null=True)
        expiration_date = UTCDateTimeAttribute(null=True)
        estimated_cost = NumberAttribute(default=0, null=True)
        revised_cost = NumberAttribute(default=0, null=True)
        existing_use = UnicodeAttribute(null=True)
        proposed_use = UnicodeAttribute(null=True)
        description = UnicodeAttribute(null=True)
        address = UnicodeAttribute(null=True)
        # load_date = UTCDateTimeAttribute(null=the_time_now)

    return PermitClass
