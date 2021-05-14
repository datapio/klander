from jsonpath_ng import parse
import operator


match_operators = {
    '$lt': operator.lt,
    '$lte': operator.le,
    '$eq': operator.eq,
    '$ne': operator.ne,
    '$gte': operator.ge,
    '$gt': operator.gt,
    '$in': lambda a, b: a in b,
    '$nin': lambda a, b: a not in b
}


def match_pattern(resource, pattern):
    if 'oneOf' in pattern:
        return match_one_of(resource, pattern['oneOf'])

    elif 'allOf' in pattern:
        return match_all_of(resource, pattern['allOf'])

    else:
        return match_field(resource, pattern)


def match_one_of(resource, patterns):
    return any([
        match_pattern(resource, pattern)
        for pattern in patterns
    ])


def match_all_of(resource, patterns):
    return all([
        match_pattern(resource, pattern)
        for pattern in patterns
    ])


def match_field(resource, pattern):
    field_path = parse(pattern['field'])
    operator_name, expected_value = pattern['where']
    operator = match_operators[operator_name]

    values = field_path.find(resource)

    return all([
        operator(contextual_data.value, expected_value)
        for contextual_data in values
    ])
