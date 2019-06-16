from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from . import dg1
from . import dg6
from . import dg10
from . import ef_com
from . import ef_groupAccess
import re

SHA256 = "id-sha256,\nparameters nullParameters"

class EF_SOD:

    def __init__(self, data):
        """
        Parâmetros
        ----------
        data : dict
            dicionário com os nomes das variáveis de instância como chaves
            e respetivo conteúdo como valor
        """
        if isinstance(data, str):
            data = self.load(data)

        self.digest_algorithm = data['digest_algorithm']
        self.signature_algorithm = data['signature_algorithm']
        self.certificates = data['certificates']
        self.signature = data['signature']
        self.data_group_hash = data['data_group_hash']


    def save(self, filename):
        """Armazena os dados do EF_SOD num ficheiro.

        Parâmetros:
        -----------
        filename : str
            nome do ficheiro onde se pretende armazenar os dados
        """
        with open(filename, 'w+') as fp:
            data = "SignedData ::= SEQUENCE {\n"
            data.append("certificates [0] IMPLICIT ")
            if self.certificates.length > 0:
                for cert in self.certificates:
                    data.append(cert + "\n")
            data.append(" OPTIONAL,\n")

            data.append("DigestAlgorithm ::= " + self.digest_algorithm + "\n")
            data.append("DataGroupHash ::= SEQUENCE {\n")
            i = 0
            for hash in self.data_group_hash:
                data.append("dataGroupNumber " + str(self.data_group_hash.index(hash))",\n")
                data.append("dataGroupHashValue " + hash + "}\n")
            fp.write(data)


    def load(self, filename):
        """ Carrega os dados do EF_SOD de um ficheiro.
        
        Parâmetros
        ----------
        filename : str
            nome do ficheiro a partir do qual se pretende obter os dados
        
        Retorna
        -------
        data : dict
            dicionário com os nomes das variáveis de instância como chaves
            e respetivo conteúdo como valor
        """
        with open(filename, 'r') as fp:
            filedata = fp.read()

        data['digest_algorithm'] = re.search("DigestAlgorithm ::= (.+)\n", filedata).group(1)
        # data['signature_algorithm'] 

        
        data['certificates'] = []
        cert_check = re.search("certificates [0] IMPLICIT (.|[\n])* OPTIONAL,\n", filedata)
        if cert_check:
            certs = cert_check.group(1)
            i = 0
            for line in certs.splitlines():
                data['certificates'][i].append(line)
                if re.search("-----END CERTIFICATE-----", line) :
                    i = i + 1

        #data['signature'] = re.search

        data['data_group_hash'] = []
        dghash_check = re.search("DataGroupHash ::= SEQUENCE {(.|\n)}", filedata)
        if dghash_check: 
            dghashes = dghash_check.group(1)
            dg = -1
            dg_hash = ''
            for line in dghashes.splitlines():
                is_number = re.search('dataGroupNumber (\d+),\n', line):
                if is_number:
                    dg = int(is_number.group(1))
                is_hash = re.search('dataGroupHashValue (.+),\n', line):
                if is_hash:
                    dg_hash = is_hash.group(1)
                    data['data_group_hash'][dg - 1] = dg_hash
                    dg = -1
                    dg_hash = ''


        return data

""" Calcula o valor de hash dos dados do EF_SOD.

        Retorna
        -------
        digest : str
            valor de hash
        """
    def hash(self):
        hash = ""
        dg1_hash = DG1("asn1_hex_data/dg1.txt").hash()
        self.data_group_hash[0] = dg1_hash
        dg6_hash = DG6("asn1_hex_data/dg6.txt").hash()
        self.data_group_hash[5] = dg6_hash
        dg10_hash = DG10("asn1_hex_data/dg10.txt").hash()
        self.data_group_hash[0] = dg10_hash
        hash.join(dg1_hash)
        hash.join(dg6_hash)
        hash.join(dg10_hash)
        hash.join(EF_COM("asn1_hex_data/ef_com.txt").hash())
        hash.join(EF_GroupAccess("asn1_hex_data/ef_groupAccess.txt").hash())
        return hash
      

print(EF_SOD().hash())
