from pyasn1.type.univ import Integer, Sequence, OctetString, SequenceOf
from pyasn1.type.namedtype import NamedType, NamedTypes
from pyasn1.type.char import UniversalString

class Data(Sequence):
    componentType = NamedTypes(
        NamedType('dataGroupNumber', Integer()),
        NamedType('dataGroupHashValue', OctetString())
    )

class DataGroupHash(SequenceOf):
    componentType = Data()

class Record(Sequence):
    componentType = NamedTypes(
        NamedType('digestAlgorithm', UniversalString()),
        NamedType('signatureAlgorithm', UniversalString()),
        NamedType('certificate', OctetString()),
        NamedType('signature', OctetString()),
        NamedType('dataGroupHash', DataGroupHash())
    )

record = Record()
record['digestAlgorithm'] = 'id-sha256'
record['signatureAlgorithm'] = 'id-pk-RSA-PKCS1-v1_5-SHA256'
record['certificate'] = b'43a541'
record['signature'] = b'468a4b'
data1 = Data()
data1['dataGroupNumber'] = 1
data1['dataGroupHashValue'] = b'11111'
data2 = Data()
data2['dataGroupNumber'] = 2
data2['dataGroupHashValue'] = b'22222'
dataGroupHash = DataGroupHash()
dataGroupHash.setComponentByPosition(0, data1)
dataGroupHash.setComponentByPosition(1, data2)
record['dataGroupHash'] = dataGroupHash

print(record)
