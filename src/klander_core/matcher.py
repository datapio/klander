"""
Pattern matching for Kubernetes resources.
"""

from typing import TypedDict, List, Tuple, Union, Any, cast
from .kubectl import Resource

from jsonpath_ng import parse
import operator


Pattern = Union['PatternOneOf', 'PatternAllOf', 'PatternField']
PatternOneOf = TypedDict('PatternOneOf', oneOf=List[Pattern])
PatternAllOf = TypedDict('PatternAllOf', allOf=List[Pattern])
PatternField = TypedDict('PatternField', field=str, where=Tuple[str, Any])


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


def match_pattern(resource: Resource, pattern: Pattern) -> bool:
    """
    :param resource: Resource to match
    :param pattern: Pattern the resource should respect
    :return: True if the resource matched, False otherwise
    """

    if 'oneOf' in pattern:
        pattern = cast(PatternOneOf, pattern)
        return match_one_of(resource, pattern['oneOf'])

    elif 'allOf' in pattern:
        pattern = cast(PatternAllOf, pattern)
        return match_all_of(resource, pattern['allOf'])

    else:
        pattern = cast(PatternField, pattern)
        return match_field(resource, pattern)


def match_one_of(resource: Resource, patterns: List[Pattern]) -> bool:
    """
    :param resource: Resource to match
    :param pattern: Patterns the resource should respect
    :return: True if the resource matched at least one pattern, False otherwise
    """

    return any(
        match_pattern(resource, pattern)
        for pattern in patterns
    )


def match_all_of(resource: Resource, patterns: List[Pattern]) -> bool:
    """
    :param resource: Resource to match
    :param pattern: Patterns the resource should respect
    :return: True if the resource matched all patterns, False otherwise
    """

    return all(
        match_pattern(resource, pattern)
        for pattern in patterns
    )


def match_field(resource: Resource, pattern: PatternField) -> bool:
    """
    :param resource: Resource to match
    :param pattern: Pattern the resource should respect
    :return: True if the resource matched, False otherwise
    """

    field_path = parse(pattern['field'])
    operator_name, expected_value = pattern['where']
    operator_fn = match_operators[operator_name]

    values = field_path.find(resource)

    return all(
        operator_fn(contextual_data.value, expected_value)
        for contextual_data in values
    )
