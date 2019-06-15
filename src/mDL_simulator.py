#! /bin/python

import sys
import json
from mDL_transaction import mDL_transaction

DATA = None

if len(sys.argv) > 1:
    if sys.argv[1] in ['--help', '-h']:
        print('Usage: mDL_simulator [FILE]')
        sys.exit()
    with open(sys.argv[1], "r") as fd:
        DATA = json.load(fd)

MDLT = mDL_transaction(DATA)
MDLT.open()
print()
MDLT.request_additional_data(['61', '62'])
print()
print(MDLT.transfer_data(['61', '62']))
