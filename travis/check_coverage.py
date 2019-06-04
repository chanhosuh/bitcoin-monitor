#!/usr/bin/env python
"""
slight adapted and cleaned-up from
https://gist.github.com/tomgross/6f7226d03a52483fbda0eae8e9a6f906

This script checks the coverage and test if it keeps at least the same.
"""

import os.path
import sys


def main():
    """ exit with failure if coverage has decreased since last run """
    coverage_report = sys.stdin.read()
    if 'TOTAL' not in coverage_report:
        print('No coverage data found in stdin. -> FAILING')
        print(coverage_report)
        sys.exit(1)
    coverage_value = get_coverage_value(coverage_report)
    filepath = 'travis/cache/coverage_value.txt'
    if os.path.isfile(filepath):
        with open(filepath, 'r') as f:
            try:
                old_coverage_value = int(f.read())
            except ValueError:   # no int found
                print('Bad value for previous coverage value.')
                exit_status = 0
            else:
                exit_status = int(coverage_value < old_coverage_value)
                if exit_status:
                    print(
                        'Coverage decreased by {}%, from {}% to {}%'.format(
                            old_coverage_value - coverage_value,
                            old_coverage_value,
                            coverage_value,
                        )
                    )
    else:
        # no old file found, so we can't compare. Assume this is ok
        print('No previous coverage value found.')
        exit_status = 0

    with open(filepath, 'w') as f:
        f.write(str(coverage_value))

    sys.exit(exit_status)


def get_coverage_value(coverage_report):
    """
    extract coverage from last line:
    TOTAL                                        116     22    81%
    """
    coverage_value = coverage_report.split()[-1].rstrip('%')
    coverage_value = int(coverage_value)
    return coverage_value


if __name__ == '__main__':
    main()
