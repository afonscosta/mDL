import asn1_parser as asn1
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

class DG1:
    """
    CLasse utilizada para representar um grupo de dados 1.
    
    Atributos
    ---------
    family_name : str
        nome da família
    
    name : str
        nome do titular
    
    date_of_birth : str
        data de nascimento
    
    date_of_issue : str
        data de emissão
    
    date_of_expiry : str
        data de validade
    
    issuing_country : str
        país emissor
    
    issuing_authority : str
        autoridade emissora
    
    license_number : str
        número da licensa
    
    number_of_entries : int
        número de categorias de veículos
    
    categories_of_vehicles : list(str)
        lista de categorias de veículos/restrições/condições
    
    Métodos
    -------
    save(filename)
        Armazena os dados do DG1 num ficheiro, codificados com ASN1

    load(filename)
        Carrega os dados do DG1 de um ficheiro, codificado com ASN1
    
    __str__()
        Retorna uma string que apresenta os dados do DG1
    """
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
        self.family_name = data['family_name']
        self.name = data['name']
        self.date_of_birth = data['date_of_birth']
        self.date_of_issue = data['date_of_issue']
        self.date_of_expiry = data['date_of_expiry']
        self.issuing_country = data['issuing_country']
        self.issuing_authority = data['issuing_authority']
        self.license_number = data['license_number']
        self.number_of_entries = data['number_of_entries']
        self.categories_of_vehicles = data['categories_of_vehicles']

    def save(self, filename):
        """Armazena os dados do DG1 num ficheiro, codificados com ASN1.
        
        Parâmetros:
        -----------
        filename : str
            nome do ficheiro onde se pretende armazenar os dados
        """
        with open(filename, 'w+') as fp:
            hex_data = asn1.encode(self, './data_groups/configs/dg1.json')
            fp.write(hex_data)

    def encode(self):
        """Codificados os dados do DG1 com ASN1.
        
        Retorna:
        --------
        hex_data : str
            dados do DG1 codificados em hexadecimal
        """
        return asn1.encode(self, './data_groups/configs/dg1.json')

    def load(self, filename):
        """ Carrega os dados do DG1 de um ficheiro, codificado com ASN1.
        
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
            data = asn1.decode(fp.read(), './data_groups/configs/dg1.json')
        return data


    def __str__(self):
        """ Retorna uma string que apresenta os dados do DG1

        Retorna
        -------
        data : str
            string com os dados do DG1
        """
        return ';'.join([self.family_name,\
             self.name,\
             self.date_of_birth,\
             self.date_of_issue,\
             self.date_of_expiry,\
             self.issuing_country,\
             self.issuing_authority,\
             self.license_number,\
             str(self.number_of_entries),\
             str(self.categories_of_vehicles)])
    

    def get_data(self):
        """ Devolve os dados associados.

        Retorna
        -------
        data : dict
            dicionário com os nomes das variáveis de instância como
            chaves e respetivo conteúdo como valor
        """
        data = {}
        data['family_name'] = self.family_name
        data['name'] = self.name
        data['date_of_birth'] = self.date_of_birth
        data['date_of_issue'] = self.date_of_issue
        data['date_of_expiry'] = self.date_of_expiry
        data['issuing_country'] = self.issuing_country
        data['issuing_authority'] = self.issuing_authority
        data['license_number'] = self.license_number
        data['categories_of_vehicles'] = self.categories_of_vehicles
        return data

    def hash(self):
        """ Calcula o valor de hash dos dados do DG1.

        Retorna
        -------
        digest : str
            valor de hash
        """
        data = self.family_name + self.name +\
            self.date_of_birth + self.date_of_issue +\
            self.date_of_expiry + self.issuing_country +\
            self.issuing_authority + self.license_number +\
            "".join(self.categories_of_vehicles) #TODO: está bem assim? divisores?
            # self.number_of_entries + self.categories_of_vehicles (TODO: number_of_entries é preciso?)
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(data.encode())
        return digest.finalize()




#DATA = {'family_name': 'Smithe Williams', 'name': 'Alexander George Thomas', 'date_of_birth': '19700301', 'date_of_issue': '20020915', 'date_of_expiry': '20070930', 'issuing_country': 'JPN', 'issuing_authority': 'HOKKAIDO PREFECTURAL POLICE ASAHIKAWA AREA SAFETY PUBLIC', 'license_number': 'A290654395164273X', 'number_of_entries': 1, 'categories_of_vehicles': ['C1;20000315;20100314;S01;<=;38303030']}
#dg1 = DG1(DATA)
#dg1.save('dg1.txt')

#dg2 = DG1('dg1.txt')
#print(dg2)
