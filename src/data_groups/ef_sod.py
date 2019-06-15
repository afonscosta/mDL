from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from . import dg1.DG1
from . import dg6.DG6 
from . import dg10.DG10
from . import ef_com.EF_COM
from . import ef_groupAccess.EF_GroupAccess

SHA256 = "AlgorithmIdentifier  ::=  {\nalgorithm id-sha256,\nparameters nullParameters  }"

class EF_SOD:

    def __init__(self, data):
        if isinstance(data, str):
            data = self.load(data)


    def save(self, filename):
        with open(filename, 'w+') as fp:
            data = "SignedData ::= SEQUENCE {\n"
            data.append("certificates [0] IMPLICIT " + self.certificates + " OPTIONAL,\n")
            data.append("DigestAlgorithm ::= " + self.digest_algorithm + "\n")
            data.append("DataGroupHash ::= SEQUENCE {\n")
            data.append("dataGroupNumber DataGroupNumber,\n")
            data.append("dataGroupHashValue OCTET STRING }\n")
            data.append("dataGroup1 (1),\n")
            data.append("dataGroup2 (2),\n")
            data.append("dataGroup3 (3),\n")
            data.append("dataGroup4 (4),\n")
            data.append("dataGroup5 (5),\n")
            data.append("dataGroup6 (6),\n")
            data.append("dataGroup7 (7),\n")
            data.append("dataGroup8 (8),\n")
            data.append("dataGroup9 (9),\n")
            data.append("dataGroup10 (10),\n")
            data.append("dataGroup11 (11),\n")
            data.append("dataGroup12 (12),\n")
            data.append("dataGroup13 (13),\n")
            data.append("dataGroup14 (14),\n")
            data.append("dataGroup15 (15),\n")
            data.append("dataGroup16 (16)}\n")
            data.append("END\n")
            fp.write(data)


    def load(self, filename):
        if isinstance(data, str):
            data = self.load(data)

            self.digest_algorithm
            self.signature_algorithm
            self.certificates
            self.signature
            self.data_group_hash


    def hash(self):
        hash = ""
        hash.join(DG1("asn1_hex_data/dg1.txt").hash())
        hash.join(DG6("asn1_hex_data/dg6.txt").hash())
        hash.join(DG10("asn1_hex_data/dg10.txt").hash())
        hash.join(EF_COM("asn1_hex_data/ef_com.txt").hash())
        hash.join(EF_GroupAccess("asn1_hex_data/ef_groupAccess.txt").hash())
        return hash
      

print(EF_SOD().hash())
