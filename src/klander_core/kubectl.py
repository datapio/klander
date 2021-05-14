from tempfile import TemporaryFile
import subprocess
import json


def get(api_version, kind, namespace=None, name=None):
    cmd = _build_cmd(
        'get',
        api_version,
        kind,
        namespace,
        name
    )

    return json.loads(_run(cmd))


def delete(resource):
    cmd = _build_cmd(
        'delete',
        resource['apiVersion'],
        resource['kind'],
        resource['metadata'].get('namespace'),
        resource['metadata']['name']
    )

    return _run(cmd, output='name')


def patch(resource, patch):
    cmd = _build_cmd(
        'patch',
        resource['apiVersion'],
        resource['kind'],
        resource['metadata'].get('namespace'),
        resource['metadata']['name']
    )
    cmd += ['-p', json.dumps(patch)]
    return json.loads(_run(cmd))


def _build_cmd(action, api_version, kind, namespace, name, output='json'):
    resource_type = _get_resource_type(api_version, kind)

    cmd = ['kubectl', action, '-o', output, resource_type]

    if namespace == '*':
        cmd.append('-A')

    elif namespace is not None:
        cmd += ['-n', namespace]

    if name is not None:
        cmd.append(name)

    return cmd


def _get_resource_type(api_version, kind):
    if '/' in api_version:
        api_group, version = api_version.split('/')
        return f'{kind}.{version}.{api_group}'.lower()

    else:
        return kind.lower()


def _run(cmd):
    with TemporaryFile('rb+') as outf:
        proc = subprocess.Popen(
            cmd,
            stdout=outf,
            stderr=subprocess.STDOUT
        )
        code = proc.wait()
        outf.seek(0)

        if code != 0:
            output = outf.read().decode('utf-8')
            raise RuntimeError(output)

        return outf.read()
