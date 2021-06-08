patterns = [
    (
        dict(foo='bar'),
        dict(field='foo', where=['$eq', 'bar']),
        True
    ),
    (
        dict(foo='bar'),
        dict(field='foo', where=['$eq', 'baz']),
        False
    ),
    (
        dict(foo='bar'),
        dict(field='foo', where=['$ne', 'bar']),
        False
    ),
    (
        dict(foo='bar'),
        dict(field='foo', where=['$ne', 'baz']),
        True
    ),
    (
        dict(foo=42),
        dict(field='foo', where=['$gt', 41]),
        True
    ),
    (
        dict(foo=42),
        dict(field='foo', where=['$gt', 42]),
        False
    ),
    (
        dict(foo=42),
        dict(field='foo', where=['$gt', 43]),
        False
    ),
    (
        dict(foo=42),
        dict(field='foo', where=['$gte', 41]),
        True
    ),
    (
        dict(foo=42),
        dict(field='foo', where=['$gte', 42]),
        True
    ),
    (
        dict(foo=42),
        dict(field='foo', where=['$gte', 43]),
        False
    ),
    (
        dict(foo=42),
        dict(field='foo', where=['$lt', 43]),
        True
    ),
    (
        dict(foo=42),
        dict(field='foo', where=['$lt', 42]),
        False
    ),
    (
        dict(foo=42),
        dict(field='foo', where=['$lt', 41]),
        False
    ),
    (
        dict(foo=42),
        dict(field='foo', where=['$lte', 43]),
        True
    ),
    (
        dict(foo=42),
        dict(field='foo', where=['$lte', 42]),
        True
    ),
    (
        dict(foo=42),
        dict(field='foo', where=['$lte', 41]),
        False
    ),
    (
        dict(foo='bar'),
        dict(field='foo', where=['$in', ['bar', 'baz']]),
        True
    ),
    (
        dict(foo='bar'),
        dict(field='foo', where=['$in', ['baz', 'biz']]),
        False
    ),
    (
        dict(foo='bar'),
        dict(field='foo', where=['$nin', ['bar', 'baz']]),
        False
    ),
    (
        dict(foo='bar'),
        dict(field='foo', where=['$nin', ['baz', 'biz']]),
        True
    ),
    (
        dict(foo=dict(bar='baz')),
        dict(field='foo.bar', where=['$eq', 'baz']),
        True
    ),
    (
        dict(foo=[dict(bar='baz'), dict(bar='biz')]),
        dict(field='foo[*].bar', where=['$in', ['baz', 'biz']]),
        True
    ),
    (
        dict(foo=[dict(bar='baz'), dict(bar='biz')]),
        dict(field='foo[*].bar', where=['$eq', 'baz']),
        False
    ),
    (
        dict(foo=23, bar=42),
        dict(oneOf=[
            dict(field='foo', where=['$eq', 42]),
            dict(field='bar', where=['$eq', 42])
        ]),
        True
    ),
    (
        dict(foo=23, bar=23),
        dict(oneOf=[
            dict(field='foo', where=['$eq', 42]),
            dict(field='bar', where=['$eq', 42])
        ]),
        False
    ),
    (
        dict(foo=42, bar=42),
        dict(allOf=[
            dict(field='foo', where=['$eq', 42]),
            dict(field='bar', where=['$eq', 42])
        ]),
        True
    ),
    (
        dict(foo=42, bar=23),
        dict(allOf=[
            dict(field='foo', where=['$eq', 42]),
            dict(field='bar', where=['$eq', 42])
        ]),
        False
    )
]
