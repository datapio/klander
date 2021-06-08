import jsonschema


def validate(resource, schema):
    try:
        jsonschema.validate(resource, schema)

    except jsonschema.exceptions.ValidationError as err:
        return False

    else:
        return True
