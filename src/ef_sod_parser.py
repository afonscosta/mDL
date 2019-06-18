from pyasn1.type.univ import Integer, Sequence, OctetString, SequenceOf
from pyasn1.type.namedtype import NamedType, NamedTypes
from pyasn1.type.char import UniversalString

class Data(Sequence):
    componentType = NamedTypes(
        NamedType('dataGroupNumber', Integer()),
        NamedType('dataGroupHashValue', OctetString())
    )

class DataGroupHash(SequenceOf):
    componentType = NamedTypes(
        Data()
    )

class Record(Sequence):
    componentType = NamedTypes(
        NamedType('digestAlgorithm', UniversalString()),
        NamedType('signatureAlgorithm', UniversalString()),
        NamedType('certificate', OctetString()),
        NamedType('signature', OctetString()),
        DataGroupHash()
    )

record = Record()
record['digestAlgorithm'] = 'id-sha256'
record['signatureAlgorithm'] = 'id-pk-RSA-PKCS1-v1_5-SHA256'
record['certificate'] = b'43a541'
record['signature'] = b'468a4b'
record['DataGroupHash'] = [{
    'dataGroupNumber': 1,
    'dataGroupHashValue': b'a2354'
}]

print(record)