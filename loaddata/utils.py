from datetime import datetime
from time import sleep


# Function to adjust table capacity to handle high capacity loads
# and reset capacity after records have been loaded
def adjustCapacity(conn, table, read_capacity=5, write_capacity=5):
    conn.update_table(table, read_capacity_units=read_capacity, write_capacity_units=write_capacity)


# Handle unicode characters in Description field
def clean_unicode(unic):
    return unic.encode('utf-8').strip()


# Set number fields to 0 if blank
def clean_int(num):
    if num is None or num == '':
        return int(0)
    else:
        return int(num)

# TODO: add def clean_date that accounts for empty date cells.


# Merge multiple fields to create and address column
def clean_address(rec):
    st_num = str(rec['STREET_NUMBER']).capitalize()
    st_name = str(rec['AVS_STREET_NAME']).capitalize()
    st_sfx = str(rec['AVS_STREET_SFX']).capitalize()
    unit = str(rec['UNIT']).capitalize()
    inputs = [st_num, st_name, st_sfx, unit, 'San Francisco, CA']

    return ' '.join([x for x in inputs if x != 'None'])


# Create a new dict from the excel records with desired fields
def clean_record(rec):
    update = dict()
    update['application_number'] = str(rec['APPLICATION #'])
    update['status'] = str(rec['STATUS']).lower()
    update['status_date'] = rec['STATUS_DATE']
    update['file_date'] = rec['FILE_DATE']
    update['expiration_date'] = rec['EXPIRATION_DATE']
    update['estimated_cost'] = clean_int(rec['ESTIMATED COST'])
    update['revised_cost'] = clean_int(rec['REVISED COST'])
    update['existing_use'] = str(rec['EXISTING USE']).lower()
    update['proposed_use'] = str(rec['PROPOSED USE']).lower()
    update['description'] = clean_unicode(rec['DESCRIPTION'])
    update['address'] = clean_address(rec)

    return update


# Clean the excel record and create a Permit Model with the record data
# load_date removed from positional arguments
def create_permit(record, record_id, model):
    rec = clean_record(record)

    permit = model(rec['application_number'], record_id)
    permit.status = rec['status']
    permit.status_date = datetime.combine(rec['status_date'], datetime.min.time())
    permit.file_date = datetime.combine(rec['file_date'], datetime.min.time())
    permit.expiration_date = datetime.combine(rec['expiration_date'], datetime.min.time())
    permit.estimated_cost = rec['estimated_cost']
    permit.revised_cost = rec['revised_cost']
    permit.existing_use = rec['existing_use']
    permit.proposed_use = rec['proposed_use']
    permit.description = rec['description']
    permit.address = rec['address']
    # permit.load_date = load_date

    return permit


# Iterate and write the records from excel to dynamodb
def write_records(records, create_record, model):
    # load_date = datetime.date.today()

    with model.batch_write() as batch:
        for index, record in enumerate(records):
            try:
                model_record = create_record(record, index, model)
                batch.save(model_record)
                sleep(0.025)

            except Exception as e:
                print 'write_records: ', index, e
                continue
