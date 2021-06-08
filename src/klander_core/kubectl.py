"""
Shell out to `kubectl` CLI.
"""

from typing import Any, Dict, List, Optional, Union, NewType
import subprocess
import tempfile
import json


Resource = NewType('Resource', Dict[str, Any])
PartialResource = NewType('PartialResource', Dict[str, Any])


def get(
    api_version: str,
    kind: str,
    namespace: Optional[str] = None,
    name: Optional[str] = None
) -> Resource:
    """
    Get one or more Kubernetes resources.

    For clustered resources, no namespace is required.

    For namespaced resources, if no namespace is specified, it will default to
    the one specified in your KUBECONFIG.

    If no name is specified, a list of resources will be returned, a single
    resource will be returned otherwise.

    If namespace equals to `*`, it will returns the resources in all
    namespaces.

    When returning a list of resources, it is returned as a Kubernetes
    Collection Resource. The list of resources is within the `items` field of
    the collection.

    :param api_version: Kubernetes Resource API version (example: `batch/v1`)
    :param kind: Kubernetes Resource kind (example: `Job`)
    :param namespace: Kubernetes Resource namespace, defaults to None
    :param name: Kubernetes Resource name, defaults to None
    :return: List of Kubernetes Resource or single resource

    :raises RuntimeError: An error occured while running `kubectl`
    """

    cmd = _build_cmd(
        'get',
        api_version,
        kind,
        namespace,
        name
    )

    return json.loads(_run(cmd))


def delete(resource: Resource) -> str:
    """
    Delete a Kubernetes resource.

    :param resource: The Kubernetes resource to remove
    :return: The name of the deleted resource

    :raises RuntimeError: An error occured while running `kubectl`
    """

    cmd = _build_cmd(
        'delete',
        resource['apiVersion'],
        resource['kind'],
        resource['metadata'].get('namespace'),
        resource['metadata']['name'],
        output='name'
    )

    return _run(cmd).decode('utf-8').strip()


def update(resource: Resource, patch: PartialResource) -> Resource:
    """
    Updates a Kubernetes resource.

    :param resource: The Kubernetes resource to update
    :param patch: The modifications to apply
    :return: The patched resource

    :raises RuntimeError: An error occured while running `kubectl`
    """

    cmd = _build_cmd(
        'patch',
        resource['apiVersion'],
        resource['kind'],
        resource['metadata'].get('namespace'),
        resource['metadata']['name']
    )
    cmd += ['-p', json.dumps(patch)]
    return json.loads(_run(cmd))


def _build_cmd(
    action: str,
    api_version: str,
    kind: str,
    namespace: Union[str, None],
    name: Union[str, None],
    output: str = 'json'
) -> List[str]:
    """
    Generate the arguments array to run the `kubectl` CLI in a subprocess.

    If namespace equals to `*`, then the action will be executed an all
    Kubernetes namespaces.

    If namespace is None, it will use the default namespace from the
    KUBECONFIG if necessary (useless for clustered resources).

    :param action: `kubectl` command to run
    :param api_version: Kubernetes Resource API version (example: `batch/v1`)
    :param kind: Kubernetes Resource kind (example: `Job`)
    :param namespace: Kubernetes Resource namespace
    :param name: Kubernetes Resource name
    :param output: Output format of the `kubectl` command, defaults to "json"
    :return: Argument list for the subprocess
    """

    resource_type = _get_resource_type(api_version, kind)

    cmd = ['kubectl', action, '-o', output, resource_type]

    if namespace == '*':
        cmd.append('-A')

    elif namespace is not None:
        cmd += ['-n', namespace]

    if name is not None:
        cmd.append(name)

    return cmd


def _get_resource_type(api_version: str, kind: str) -> str:
    """
    >>> _get_resource_type("v1", "Pod")
    "pod"
    >>> _get_resource_type("batch/v1", "Job")
    "job.v1.batch"
    """

    if '/' in api_version:
        api_group, version = api_version.split('/')
        return f'{kind}.{version}.{api_group}'.lower()

    else:
        return kind.lower()


def _run(cmd: List[str]) -> str:
    """
    Run a `kubectl` command in a subprocess and capture its output.

    It uses a temporary file to capture the output to avoid deadlocks when the
    `kubectl` output is too big.

    :param cmd: Argument list to execute in a subprocess
    :return: Command's output

    :raises RuntimeError: The command exited with a non-zero exit code
    """

    with tempfile.TemporaryFile('rb+') as outf:
        # pylint: disable=consider-using-with
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
