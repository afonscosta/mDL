# some_file.py
import sys
sys.path.insert(0, '../')
import asn1_parser as asn1
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

def int_to_hex(integer):
    hex_text = format(integer, 'x')
    if len(hex_text) % 2 == 1:
        hex_text = '0' + hex_text
    return hex_text

def hex_to_int(hex_text):
    return int(hex_text, 16)

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
        self.tags = {
            '60': 'ALL',
            '5F01': 'version',
            '5C': 'tag_list',
        }


    def save(self, filename):
        with open(filename, 'w+') as fp:
            hex_data = asn1.encode(self, './data_groups/configs/ef.com.json')
            #hex_data = asn1.encode(self, './configs/ef.com.json')
            fp.write(hex_data)


    def load(self, filename):
        with open(filename, 'r') as fp:
            data = asn1.decode(fp.read(), './data_groups/configs/ef.com.json')
            #data = asn1.decode(fp.read(), './configs/ef.com.json')
        return data


    def __str__(self):
        return ';'.join([
            self.version,\
            str(self.tag_list)])
    

    def get_data(self, permissions):
        data = {}
        for tag in permissions:
            allowed_attr = self.tags[tag]
            if allowed_attr == 'ALL':
                data['version'] = self.version
                data['tag_list'] = self.tag_list
            else:
                data[allowed_attr] = getattr(self, allowed_attr)
        return data

    def hash(self):
        data = self.version + self.version +\
            "".join(self.tag_list) #TODO: está bem assim? divisores?
            # self.number_of_entries + self.categories_of_vehicles (TODO: number_of_entries é preciso?)
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(data.encode())
        return digest.finalize()




#DATA = {'version': '0100', 'tag_list': ['61', '75', '62']}
#ef_com1 = EF_COM(DATA)
#ef_com1.save('ef_com.txt')

#ef_com2 = EF_COM('ef_com.txt')
#print(ef_com2)
