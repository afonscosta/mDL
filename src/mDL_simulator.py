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
        for bt in DATA['dg6']['biometric_templates']:
            FILENAME = bt['bdb']
            with open(FILENAME, "rb") as fd:
                IMAGE = fd.read()
                bt['bdb'] = IMAGE

MDLT = mDL_transaction(DATA)
MDLT.open()
print()
MDLT.request_additional_data(['61', '62'])
print()
print('DATA:',MDLT.transfer_data(['61', '62']))
print()
print('SIGNATURE:',MDLT.transfer_signature())
print()
print('DIGESTS:',MDLT.transfer_digests())