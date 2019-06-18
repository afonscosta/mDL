import sys 
sys.path.append('../')
import dg1 as DG1
import dg6 as DG6
import dg10 as DG10
import ef_com as EF_COM
import ef_groupAccess as EF_GroupAccess
import re
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_der_private_key
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
            
        self.digest_algorithm = data['digest_algorithm']
        self.signature_algorithm = data['signature_algorithm']
        self.certificate = data['certificate']
        self.signature = data['signature']
        self.data_group_hash = []

        for hash in data['data_group_hash']:
            self.data_group_hash.append(hash)
            # self.data_group_hash[hash['data_group_number']] = hash['data_group_hash_value']

        # self.digest_algorithms = []
        # for digest_algorithm in data['signer_data']['digest_algorithms']:
        #     self.digest_algorithms.append(digest_algorithm)

        # self.certificates = []
        # for certificate in data['signer_data']['certificates']:
        #     self.certificates.append(certificate)

        # self.signer_info.signer_id = data['signer_data']['signer_info']['signer_id']

        # self.signer_info.digest_algorithm = data['signer_data']['signer_info']['digest_algorithm']

        # self.signature_algorithm = data['signer_data']['signer_info']['signature_algorithm']

        # self.signature = data['signer_data']['signer_info']['signature']

        # self.data_group_hash = []
        # for hash in data['data_group_hash']:
        #     self.data_group_hash[hash['data_group_number']] = hash['data_group_hash_value']


    def save(self, filename):
        """Armazena os dados do EF_SOD num ficheiro.

        Parâmetros:
        -----------
        filename : str
            nome do ficheiro onde se pretende armazenar os dados
        """
        with open(filename, 'w+') as fp:
            hex_data = asn1.encode(self, './configs/ef_sod.json')#'./data_groups/configs/ef_sod.json')
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
            data = asn1.decode(fp.read(), './configs/ef_sod.json') #'./data_groups/configs/ef_sod.json')
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

        with open("./key.der", "rb") as f:
            key = load_der_private_key(f.read(), password=b"passphrase", backend=default_backend())

        payload = ""
        for digest in self.data_group_hash:
            payload.join(digest[digest])

        signature = payload.sign(key, hashes.SHA256(), default_backend())

        return None


    def __str__(self):
        return self.digest_algorithm + '\n' + self.signature_algorithm + '\n' + \
            self.certificate + '\n' + self.signature + '\n' + str(self.data_group_hash)

with open('../certificates/certificate.der', 'rb') as f:
    certificate = f.read()

data_string = 'datagrouphash'

data = {
    'digest_algorithm': 'id-sha256',
    'signature_algorithm': 'id-pk-RSA-PKCS1-v1_5-SHA256',
    'certificate': certificate.hex(),
    'signature': 'assinatura',
    'data_group_hash': [
        {
            'data_group_number': 1,
            'data_group_hash_value': "digest1"
        },
        {
            'data_group_number': 2,
            'data_group_hash_value': "digest2"
        }
    ]
}

ef_sod = EF_SOD(data)

ef_sod.save('ef_sod.txt')

data1 = ef_sod.load('ef_sod.txt')

print(EF_SOD(data1))