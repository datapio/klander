# pylint: disable=broad-except

"""
klander CLI.
"""

from klander_core.reconciler import get_resources, Reconciler

import sys


def main():
    """
    Fetch the StateReconciler resources and run the reconciliation process for
    each of them:

      - fetch the observed resources
      - get the non compliant resources
      - execute the required action for non-compliant resources
    """

    try:
        for spec in get_resources():
            reconciler = Reconciler(spec)
            observed_resources = reconciler.observe()
            non_compliant_resources = reconciler.match(observed_resources)
            reconciler.reconcile(non_compliant_resources)

    except Exception as err:
        print('Unhandled exception:', err, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
