import asn1_parser as asn1
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

class BiometricTemplate:
    def __init__(self, version, bdb_owner, bdb_type, bdb):
        self.version = version if version is not None else '0101'
        self.bdb_owner = bdb_owner
        self.bdb_type = bdb_type
        self.bdb = bdb
    
    def __str__(self):
        return '(' + ', '.join([str(self.version), str(self.bdb_owner), str(self.bdb_type), str(self.bdb)[:20] + '...']) + ')'


class DG6:
    """
    CLasse utilizada para representar um grupo de dados 6.
    
    Atributos
    ---------
    
    Métodos
    -------
    """
    def __init__(self, data):
        """ Construtor da classe DG6.

        Parâmetros
        ----------
        data : list
            lista de dicionários que representam biometric templates
        """
        if isinstance(data, str):
            data = self.load(data)
        self.biometric_templates = []
        
        for template in data['biometric_templates']:
            self.biometric_templates.append(
                BiometricTemplate(
                    template['version'],
                    template['bdb_owner'],
                    template['bdb_type'],
                    template['bdb']
                )
            )
        self.number_of_entries = data['number_of_entries']


    def save(self, filename):
        """Armazena os dados do DG6 num ficheiro, codificados com ASN1.
        
        Parâmetros:
        -----------
        filename : str
            nome do ficheiro onde se pretende armazenar os dados
        """
        with open(filename, 'w+') as fp:
            hex_data = asn1.encode(self, './data_groups/configs/dg6.json')
            fp.write(hex_data)


    def load(self, filename):
        """ Carrega os dados do DG6 de um ficheiro, codificado com ASN1.
        
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


    def __str__(self):
        """ Retorna uma string que apresenta os dados do DG1

        Retorna
        -------
        data : str
            string com os dados do DG1
        """
        return ';'.join([str(t) for t in self.biometric_templates])
    

    def get_data(self, permissions):
        """ Devolve os dados permitidos.

        Parâmetros
        ----------
        permissions : list
            lista com as tags dos elementos de dados permitidos

        Retorna
        -------
        data : dict
            dicionário com os nomes das variáveis de instância permitidas
            como chaves e respetivo conteúdo como valor
        """
        data = []
        for t in self.biometric_templates:
            data.append({'version': t.version,
                         'bdb_owner': t.bdb_owner,
                         'bdb_type': t.bdb_type,
                         'bdb': t.bdb})
        return data

    def hash(self):
        """ Calcula o valor de hash dos dados do DG1.

        Retorna
        -------
        digest : str
            valor de hash
        """
        data = "".join(t.version + t.bdb_owner + t.bdb_type + t.bdb
                        for t in self.biometric_templates)

        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(data.encode())
        return digest.finalize()

