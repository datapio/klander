commands = [
    (
        ['get', 'v1', 'Pod', '*', None],
        {},
        ['kubectl', 'get', '-o', 'json', 'pod', '-A']
    ),
    (
        ['get', 'batch/v1', 'Job', '*', None],
        {},
        ['kubectl', 'get', '-o', 'json', 'job.v1.batch', '-A']
    ),
    (
        ['get', 'v1', 'Pod', 'default', None],
        {},
        ['kubectl', 'get', '-o', 'json', 'pod', '-n', 'default']
    ),
    (
        ['get', 'v1', 'Pod', None, None],
        {},
        ['kubectl', 'get', '-o', 'json', 'pod']
    ),
    (
        ['get', 'v1', 'Pod', None, 'example'],
        {},
        ['kubectl', 'get', '-o', 'json', 'pod', 'example']
    ),
    (
        ['get', 'v1', 'Pod', None, None],
        dict(output='name'),
        ['kubectl', 'get', '-o', 'name', 'pod']
    )
]
