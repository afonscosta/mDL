import sys
import asn1_parser as asn1
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

class EF_COM:
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
        self.version = data['version']
        self.tag_list = data['tag_list']

    def save(self, filename):
        with open(filename, 'w+') as fp:
            hex_data = asn1.encode(self, './data_groups/configs/ef_com.json')
            #hex_data = asn1.encode(self, './configs/ef.com.json')
            fp.write(hex_data)


    def load(self, filename):
        with open(filename, 'r') as fp:
            data = asn1.decode(fp.read(), './data_groups/configs/ef_com.json')
            #data = asn1.decode(fp.read(), './configs/ef.com.json')
        return data


    def __str__(self):
        return 'Version: ' + self.version + '\n' +\
                'DG\'s available: ' + ', '.join(self.tag_list)

    def get_data(self):
        """ Devolve os dados do EF_COM.

        Retorna
        -------
        data : dict
            dicionário com os nomes das variáveis de instância como
            chaves e respetivo conteúdo como valor
        """
        data = {}
        data['version'] = self.version
        data['tag_list'] = self.tag_list
        return data

    def hash(self):
        data = self.version + self.version +\
            "".join(self.tag_list) #TODO: está bem assim? divisores?
            # self.number_of_entries + self.categories_of_vehicles (TODO: number_of_entries é preciso?)
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(data.encode())
        return digest.finalize()
