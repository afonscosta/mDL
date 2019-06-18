from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import dg1 as DG1
import dg6 as DG6
import dg10 as DG10
import ef_com as EF_COM
import ef_groupAccess as EF_GroupAccess
import re
import asn1_parser as asn1

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
            
        self.digest_algorithms = []
        for digest_algorithm in data['signer_data']['digest_algorithms']:
            self.digest_algorithms.append(digest_algorithm)

        self.certificates = []
        for certificate in data['signer_data']['certificates']:
            self.certificates.append(certificate)

        self.signer_info.signer_id = data['signer_data']['signer_info']['signer_id']

        self.signer_info.digest_algorithm = data['signer_data']['signer_info']['digest_algorithm']

        self.signature_algorithm = data['signer_data']['signer_info']['signature_algorithm']

        self.signature = data['signer_data']['signer_info']['signature']

        self.data_group_hash = []
        for hash in data['data_group_hash']:
            self.data_group_hash[hash['data_group_number']] = hash['data_group_hash_value']


    def save(self, filename):
        """Armazena os dados do EF_SOD num ficheiro.

        Parâmetros:
        -----------
        filename : str
            nome do ficheiro onde se pretende armazenar os dados
        """
        with open(filename, 'w+') as fp:
            hex_data = asn1.encode(self, './data_groups/configs/ef_sod.json')
            fp.write(hex_data)


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
            data = asn1.decode(fp.read(), './data_groups/configs/dg6.json')
        return data


    # def hash(self):
    #     """ Calcula o valor de hash dos dados do EF_SOD.

    #         Retorna
    #         -------
    #         digest : str
    #             valor de hash
    #     """
    #     hash = ""
    #     dg1_hash = DG1("asn1_hex_data/dg1.txt").hash()
    #     self.data_group_hash[0] = dg1_hash
    #     dg6_hash = DG6("asn1_hex_data/dg6.txt").hash()
    #     self.data_group_hash[5] = dg6_hash
    #     dg10_hash = DG10("asn1_hex_data/dg10.txt").hash()
    #     self.data_group_hash[0] = dg10_hash
    #     hash.join(dg1_hash)
    #     hash.join(dg6_hash)
    #     hash.join(dg10_hash)
    #     hash.join(EF_COM("asn1_hex_data/ef_com.txt").hash())
    #     hash.join(EF_GroupAccess("asn1_hex_data/ef_groupAccess.txt").hash())
    #     return hash

    def get_digests(self, groups):

        digests = []
        
        for dg in groups:
            digests[dg] = self.data_group_hash[dg]

        return digests

    def get_signature(self, groups):

        with open("./certificate.der", "rb") as f:

            digests = self.get_digests(groups)
            payload = ""
            for digest in digests:
                payload.join(digests[digest])

            cert 

            signature = payload.sign(self., hashes.SHA256(), default_backend())

        return None