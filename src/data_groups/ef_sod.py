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
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_der_private_key
import ef_sod_parser as parser

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
            self.signed_data = self.load(data)        
        else:
            self.signed_data = parser.create_signed_data(data)

    def save(self, filename):
        """Armazena os dados do EF_SOD num ficheiro.

        Parâmetros:
        -----------
        filename : str
            nome do ficheiro onde se pretende armazenar os dados
        """
        with open(filename, 'w+') as fp:
            print(self.signed_data)
            hex_data = parser.sod_encode(self.signed_data)
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
            data = parser.sod_decode(fp.read())
        return data

    def set_digests(self, groups):
        dgh = parser.DataGroupHash()
        for n, (id, group) in enumerate(groups.items()):
            data = parser.Data()
            data['dataGroupNumber'] = id
            data['dataGroupHashValue'] = group.hash()
            # TODO: Passar digestAlgorithm ao hash
            dgh.setComponentByPosition(n, data)
        self.signed_data['dataGroupHash'] = dgh

    def get_digests(self):
        res = {}
        for group in self.signed_data['dataGroupHash']:
            res[group['dataGroupNumber']] = group['dataGroupHashValue']
        return res

    def set_signature(self):
        # TODO: ver passphrase
        with open("./key.der", "rb") as f:
            key = load_der_private_key(f.read(), password=b"passphrase", backend=default_backend())

        digest = ''.join([x['dataGroupHashValue'] for x in self.signed_data['dataGroupHash']])

        signature = None

        if self.signed_data['signatureAlgorithm'] == 'id-pk-RSA-PKCS1-v1_5-SHA256':
            signature = key.sign(
                digest.encode(),
                padding.PKCS1v15(
                    mgf=padding.MGF1(hashes.SHA256())
                ),
                hashes.SHA256()
            )
        elif self.signed_data['signatureAlgorithm'] == 'id-pk-RSA-PSS-v1_5-SHA256':
            signature = key.sign(
                digest.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        else: 
            raise Exception('ERROR: Algorithm not implemented.')
        self.signed_data['signature'] = signature

    def get_signature(self, groups):
        return self.signed_data['signature']


    def __str__(self):
        return str(self.signed_data)

with open('../certificates/certificate.der', 'rb') as f:
    certificate = f.read()

data_string = 'datagrouphash'

data = {
    'digestAlgorithm': 'id-sha256',
    'signatureAlgorithm': 'id-pk-RSA-PKCS1-v1_5-SHA256',
    'certificate': certificate.hex(),
    'signature': 'a231',
    'dataGroupHash': [
        {
            'dataGroupNumber': 1,
            'dataGroupHashValue': "a411"
        },
        {
            'dataGroupNumber': 2,
            'dataGroupHashValue': "ba41"
        }
    ]
}

ef_sod = EF_SOD(data)

ef_sod.save('ef_sod.txt')

data1 = ef_sod.load('ef_sod.txt')

print(EF_SOD(data1))