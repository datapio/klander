from klander_core.reconciler import get_resources, Reconciler

import sys


def main():
    try:
        for cr in get_resources():
            reconciler = Reconciler(cr)
            reconciler.reconcile(
                reconciler.match(
                    reconciler.observe()
                )
            )

    except Exception as err:
        print('Unhandled exception:', err, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
