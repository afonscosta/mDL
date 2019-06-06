from mDL import mDL
from mDL_transaction import mDL_transaction

with open("face-image.jpg", "rb") as fd:
    image_bytes = fd.read()

DATA = {
    'dg1': {
        'family_name': 'Smithe Williams',
        'name': 'Alexander George Thomas',
        'date_of_birth': '19700301',
        'date_of_issue': '20020915',
        'date_of_expiry': '20070930',
        'issuing_country': 'JPN',
        'issuing_authority': 'HOKKAIDO PREFECTURAL POLICE ASAHIKAWA AREA SAFETY PUBLIC',
        'license_number': 'A290654395164273X',
        'number_of_entries': 1,
        'categories_of_vehicles': [
            'C1;20000315;20100314;S01;<=;38303030',
            'C1;20000315;20100314;S01;<=;38303030'
        ]
    },
    'dg6': {
        'biometric_templates': [
            {
                'version': 257,
                'bdb_owner': 257,
                'bdb_type': 8,
                'bdb': image_bytes[:64000]
            },
            {
                'version': 257,
                'bdb_owner': 257,
                'bdb_type': 8,
                'bdb': image_bytes[64000:65000]
            }
        ],
        'number_of_entries': 1
    },
    'dg10': {
        'version': '1',
        'last_update': '20130115000000',
        'expiration_date': '20130314235959',
        'next_update': '20130122000000',
        'management_info': 'info'
    },
    'ef_groupAccess': {
        1: '61',
        10: '62'
    },
    'ef_com': {
        'version': '0100',
        'tag_list': ['61', '75', '62']
    }
}

# mdl = mDL(DATA)
# mdl.save()

# mdl_loaded = mDL()
# # mdl_loaded.set_permissions({
# #     '1': '61',
# #     '6': '75',
# #     '10': '62'
# # })
# print('- All DG1:', mdl_loaded.dg1, sep="\n")
# print('\n- All DG6:', mdl_loaded.dg6, sep="\n")
# print('\n- All DG10:', mdl_loaded.dg10, sep="\n")
# print('\n- All COM:', mdl_loaded.ef_com, sep="\n")
# print('\n- All GroupAccess:', mdl_loaded.ef_groupAccess, sep="\n")
# print('\n- Allowed:', mdl_loaded.get_data([1, 6, 10]), sep="\n")
# print('\n- Allowed HEX:', mdl_loaded.get_data_hex([1, 6, 10]), sep="\n")

MDLT = mDL_transaction(DATA)
MDLT.open()
print('\n')
MDLT.request_additional_data(['61', '62'])
print('\n')
print(MDLT.transfer_data(['61', '62']))
