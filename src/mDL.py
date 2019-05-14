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
            #self.dg6 = dg6.DG6(data['dg6'])
            #self.dg10 = dg10.DG10(data['dg10'])
            #self.bcd = bcd.BCD(data['bcd'])
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
        #self.dg6 = dg6.DG6('./data_groups/asn1_hex_data/dg6.txt')
        #self.dg10 = dg10.DG10('./data_groups/asn1_hex_data/dg10.txt')
        #self.bcd = bcd.BCD('./data_groups/asn1_hex_data/bcd.txt')
        self.ef_com = ef_com.EF_COM('./data_groups/asn1_hex_data/ef_com.txt')
        self.ef_groupAccess = ef_groupAccess.EF_GroupAccess('./data_groups/asn1_hex_data/ef_groupAccess.txt')
        #self.ef_sod = ef_sod.EF_SOD('./data_groups/asn1_hex_data/ef_sod.txt')

    def save(self):
        self.dg1.save('./data_groups/asn1_hex_data/dg1.txt')
        #self.dg6.save('./data_groups/asn1_hex_data/dg6.txt')
        #self.dg10.save('./data_groups/asn1_hex_data/dg10.txt')
        #self.bcd.save('./data_groups/asn1_hex_data/bcd.txt')
        self.ef_com.save('./data_groups/asn1_hex_data/ef_com.txt')
        self.ef_groupAccess.save('./data_groups/asn1_hex_data/ef_groupAccess.txt')
        #self.ef_sod.save('./data_groups/asn1_hex_data/ef_sod.txt')
        #return data


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
        'categories_of_vehicles': ['C1;20000315;20100314;S01;<=;38303030']
    },
    'ef_groupAccess': {
        1: ['5F20', '7F63'],
        10: ['62']
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
print('\n- All COM:', mdl_loaded.ef_com, sep="\n")
print('\n- All GroupAccess:', mdl_loaded.ef_groupAccess, sep="\n")
print('\n- Allowed DG1:', mdl_loaded.dg1.get_data(mdl_loaded.ef_groupAccess.get_permissions(1)), sep="\n")
