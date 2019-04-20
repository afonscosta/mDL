from data_groups import dg1
from data_groups import dg6
from data_groups import dg10
from data_groups import bcd
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
            self.dg10 = dg10.DG10(data['dg10'])
            self.bcd = bcd.BCD(data['bcd'])
            self.ef_com = ef_com.EF_COM(data['ef_com'])
            self.ef_groupAccess = ef_groupAccess.EF_GroupAccess(data['ef_groupAccess'])
            self.ef_sod = ef_sod.EF_SOD(data['ef_sod'])

    def load(self):
        """ Carrega os dados do mDL dos ficheiros respetivos, codificados com ASN1.
        
        Retorna
        -------
        data : dict
            dicionário com os nomes dos grupos de dados como chaves
            e respetivo conteúdo como valor
        """
        self.dg1 = dg1.DG1('./data_groups/configs/dg1.json')
        self.dg6 = dg6.DG6('./data_groups/configs/dg6.json')
        self.dg10 = dg10.DG10('./data_groups/configs/dg10.json')
        self.bcd = bcd.BCD('./data_groups/configs/bcd.json')
        self.ef_com = ef_com.EF_COM('./data_groups/configs/ef_com.json')
        self.ef_groupAccess = ef_groupAccess.EF_GroupAccess('./data_groups/configs/ef_groupAccess.json')
        self.ef_sod = ef_sod.EF_SOD('./data_groups/configs/ef_sod.json')

    def save(self):
        self.dg1.save('dg1.txt')
        self.dg6.save('dg6.txt')
        self.dg10.save('dg10.txt')
        self.bcd.save('bcd.txt')
        self.ef_com.save('ef_com.txt')
        self.ef_groupAccess.save('ef_groupAccess.txt')
        self.ef_sod.save('ef_sod.txt')
        return data


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
