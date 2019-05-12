import asn1_parser as asn1

class EF_GroupAccess:
    def __init__(self, data):
        """
        """
        if isinstance(data, str):
            self.allowed_data_groups = self.load(data)['allowed_data_groups']
        else:
            self.allowed_data_groups = {}
            for dg, tags in data.items():
                self.allowed_data_groups[dg] = tags

    def save(self, filename):
        """Armazena os dados do GroupAccess num ficheiro, codificados com ASN1.
        
        Parâmetros:
        -----------
        filename : str
            nome do ficheiro onde se pretende armazenar os dados
        """
        with open(filename, 'w+') as fp:
            hex_data = asn1.encode(self, './data_groups/configs/ef_groupAccess.json')
            fp.write(hex_data)


    def load(self, filename):
        """ Carrega os dados do GroupAccess de um ficheiro, codificado com ASN1.
        
        Parâmetros
        ----------
        filename : str
            nome do ficheiro a partir do qual se pretende obter os dados
        
        Retorna
        -------
        data : dict
            dicionário com os nomes dos data groups como chaves e uma lista do
            respetivo conteúdo cujo acesso é permitido como valor
        """
        with open(filename, 'r') as fp:
            data = asn1.decode(fp.read(), './data_groups/configs/ef_groupAccess.json')
        return data
    

    def __str__(self):
        """ Retorna uma string que apresenta os dados do GroupAccess

        Retorna
        -------
        data : str
            string com os dados do GroupAccess
        """
        return ' | '.join([ 'DG' + str(dg) + ' (' + ', '.join(tags) + ')'
                            for dg, tags in self.allowed_data_groups.items()])

    def set_permissions(self, allowed):
        """ Estabelece os campos que têm autorização para serem lidos.

        Parâmetros
        ----------
        allowed : dict
            dicionário com os números dos data groups como chaves e uma lista das
            tags cujo acesso ao conteúdo é permitido como valor
        """
        self.allowed_data_groups = {}
        for dg, tags in allowed.items():
            self.allowed_data_groups[dg] = tags
    
    def get_permissions(self, dg):
        """ Obtém as tags cujo acesso é permitido, de um determinado data group.

        Parâmetros
        ----------
        dg : int
            identificador do data group

        Retorna
        -------
        tags : list
            lista das tags do grupo de dados 'dg', cujo acesso ao conteúdo é
            permitido
        """
        return self.allowed_data_groups[dg]
