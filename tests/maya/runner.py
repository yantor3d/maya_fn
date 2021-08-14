"""Maya test runner."""

import pytest 
import os
import sys 


def main(*argv):
    """Run the Maya tests."""

    args = [
        '--cov=src',
        '--cov-report term-missing',
        '-p no:warnings',
        '-p no:cacheprovider',
        '-xv',
        '--cov=src -p no:cacheprovider'
    ] + list(argv)

    if not os.path.exists(args[-1]):
        args.append('./tests/maya/')

    pytest.main(list(argv))


if __name__ == '__main__':
    main(*sys.argv[1:])