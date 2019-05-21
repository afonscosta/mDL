from data_groups import dg1
from data_groups import dg6
from data_groups import dg10
from data_groups import ef_com
from data_groups import ef_groupAccess
from data_groups import ef_sod

class mDL:
    def __init__(self, data=None):
        """
        Parâmetros
        ----------
        data : dict
            dicionário com os nomes das variáveis de instância como chaves
            e respetivo conteúdo como valor
        """
        if not data:
            self.load()
        else:
            self.dg1 = dg1.DG1(data['dg1'])
            self.dg6 = dg6.DG6(data['dg6'])
            #self.dg10 = dg10.DG10(data['dg10'])
            self.ef_com = ef_com.EF_COM(data['ef_com'])
            self.ef_groupAccess = ef_groupAccess.EF_GroupAccess(data['ef_groupAccess'])
            #self.ef_sod = ef_sod.EF_SOD(data['ef_sod'])

    def load(self):
        """ Carrega os dados do mDL dos ficheiros respetivos, codificados com ASN1.
        
        Retorna
        -------
        data : dict
            dicionário com os nomes dos grupos de dados como chaves
            e respetivo conteúdo como valor
        """
        self.dg1 = dg1.DG1('./data_groups/asn1_hex_data/dg1.txt')
        self.dg6 = dg6.DG6('./data_groups/asn1_hex_data/dg6.txt')
        #self.dg10 = dg10.DG10('./data_groups/asn1_hex_data/dg10.txt')
        self.ef_com = ef_com.EF_COM('./data_groups/asn1_hex_data/ef_com.txt')
        self.ef_groupAccess = ef_groupAccess.EF_GroupAccess('./data_groups/asn1_hex_data/ef_groupAccess.txt')
        #self.ef_sod = ef_sod.EF_SOD('./data_groups/asn1_hex_data/ef_sod.txt')

    def save(self):
        self.dg1.save('./data_groups/asn1_hex_data/dg1.txt')
        self.dg6.save('./data_groups/asn1_hex_data/dg6.txt')
        #self.dg10.save('./data_groups/asn1_hex_data/dg10.txt')
        self.ef_com.save('./data_groups/asn1_hex_data/ef_com.txt')
        self.ef_groupAccess.save('./data_groups/asn1_hex_data/ef_groupAccess.txt')
        #self.ef_sod.save('./data_groups/asn1_hex_data/ef_sod.txt')
        #return data

    def set_permissions(self, allow):
        self.ef_groupAccess.set_permissions(allow)
    
    def get_data(self):
        result = {}
        if self.ef_groupAccess.is_allowed(1):
            result[1] = self.dg1.get_data()
        if self.ef_groupAccess.is_allowed(6):
            result[6] = self.dg6.get_data()
        #if self.ef_groupAccess.is_allowed(10):
        #    result[10] = self.dg10.get_data()
        return str(result)
    
    def get_data_hex(self):
        result = ''
        if self.ef_groupAccess.is_allowed(1):
            result += self.dg1.encode()
        if self.ef_groupAccess.is_allowed(6):
            result += self.dg6.encode()
        #if self.ef_groupAccess.is_allowed(10):
        #    result += self.dg10.get_data()
        return result

    def auth_source(self):
        pass

    def connect_info_with_owner(self):
        pass

    def verify_integraty(self):
        pass

    def allow_info(self):
        pass

    def request_info(self):
        # Autorizar ou não
        # Fazer update das autorizações
        pass


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
        'categories_of_vehicles': ['C1;20000315;20100314;S01;<=;38303030','C1;20000315;20100314;S01;<=;38303030']
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
    'ef_groupAccess': {
        1: '61',
        10: '62'
    },
    'ef_com': {
        'version': '0100',
        'tag_list': ['61', '75', '62']
    }
}

mdl = mDL(DATA)
mdl.save()
#mdl.dg1.set_permissions(['family_name', 'categories_of_vehicles'])
#print(mdl.dg1.hash())

mdl_loaded = mDL()
print('- All DG1:', mdl_loaded.dg1, sep="\n")
print('\n- All DG6:', mdl_loaded.dg6, sep="\n")
print('\n- All COM:', mdl_loaded.ef_com, sep="\n")
print('\n- All GroupAccess:', mdl_loaded.ef_groupAccess, sep="\n")
print('\n- Allowed:', mdl_loaded.get_data(), sep="\n")
print('\n- Allowed HEX:', mdl_loaded.get_data_hex(), sep="\n")

# TODO: Dúvidas DG6
# - Imagens muito grandes dão exceção 'Data too long', por causa da função length, que admite um tamanho máximo de 65535 bytes (Especificação para o ASN1).
# - Não está implementada a codificação da imagem de acordo com o ISO 19794-5 (https://www.sis.se/api/document/preview/913943/). Necessário?
# - Necessário implementar o armazenamento da imagem cifrada (tag='7F2E')?
# - Deve-se validar o type e owner format (Se existem)? E deve-se implementar para vários formatos?