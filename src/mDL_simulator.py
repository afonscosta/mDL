#! /bin/python

import sys
import json
from mDL_transaction import mDL_transaction
from data_groups import dg1
from data_groups import dg6
from data_groups import dg10

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

def calculate_digests(groups):
    digests = {}
    for id, group in groups.items():
        digests[id] = group.hash('id-sha256')
    return digests

def verify_signature(digests, signature, algorithm):
    signature = None

    with open("certificates/certificate.der", "rb") as f:
        cert = crypto.load_certificate(crypto.FILETYPE_ASN1, f.read())

    public_key = cert.public_key()

    digest = ''.join(digests.values())

    if algorithm == 'id-pk-RSA-PKCS1-v1_5-SHA256':
        return public_key.verify(
            signature,
            digest.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    elif algorithm == 'id-pk-RSA-PSS-v1_5-SHA256':
        return public_key.verify(
            signature,
            digest.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    else: 
        raise Exception('ERROR: Signature algorithm not implemented.')

MDLT = mDL_transaction(DATA)
MDLT.open()
print()
MDLT.request_additional_data(['61', '62'])
print()
transfer_data = MDLT.transfer_data(['61', '62'])
print('DATA:',transfer_data)
print()
transfer_signature = MDLT.transfer_signature()
print('SIGNATURE:',transfer_signature)
print()
transfer_digests = MDLT.transfer_digests()
print('DIGESTS:',transfer_digests)
dg1 = dg1.DG1(transfer_data[1])
#dg6 = dg6.DG6(transfer_data[6])
dg10 = dg10.DG10(transfer_data[10])
dgs = {
    1: dg1,
    #6: dg6,
    10: dg10
}
digests = calculate_digests(dgs)
print()
print(digests)
print('DIGESTS VALIDATION:',digests[1] == transfer_digests[1] and digests[10] == transfer_digests[10])
print('SIGNATURE VALIDATION:',verify_signature(transfer_digests,transfer_signature), 'id-pk-RSA-PKCS1-v1_5-SHA256')