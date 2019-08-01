import os
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute
)


def PermitsModel(db_region='', db_host='http://localhost:8000'):

    dynamo_table = os.environ['DYNAMOTABLE']

    class PermitClass(Model):
        class Meta:
            table_name = dynamo_table
            read_capacity_units = 5
            write_capacity_units = 5
            region = db_region
            host = db_host

        record_id = NumberAttribute(range_key=True)
        application_number = UnicodeAttribute(hash_key=True)
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
        # load_date = UTCDateTimeAttribute(null=True)

        # Unresolved Attribute reference caused by dated pynamodb library:
        # try method _get_attributes
        def __iter__(self):
            for name, attr in self._get_attributes().items():
                yield name, attr.serialize(getattr(self, name))

    return PermitClass
