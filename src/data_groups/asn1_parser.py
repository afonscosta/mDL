import json
import bcd
import re

hex_to_char = lambda hex_code: re.escape(chr(int(hex_code,16)))
regex_between = lambda hex_code_1, hex_code_2: \
                    hex_to_char(hex_code_1) + '-' + hex_to_char(hex_code_2)

# Special characters
S = ''.join([regex_between('20', '2F'),
              hex_to_char('3A'),
              regex_between('3C', '40'),
              regex_between('5B', '60'),
              regex_between('7B', '7E'),
              regex_between('A1', 'AC'),
              regex_between('A5', 'AE'),
              regex_between('A7', 'BF')
            ])

# Numeric character
N = regex_between('30', '39')

# Alphabetic character
A = ''.join([regex_between('41', '5A'),
              regex_between('61', '7A'),
              regex_between('C0', 'D6'),
              regex_between('D8', 'F6'),
              regex_between('F8', 'FF')
            ])

# Delimiters
D = ';×÷'


def bin_to_hex(bin_text):
    """ Converte um texto em formato binário para hexadecimal.

    Parâmetros
    ----------
    bin_text : str
        texto em formato binário, que se pretende converter

    Retorna
    -------
    hex_text : str
        texto convertido para formato hexadecimal
    """
    return format(int(bin_text, 2), f'0{(len(bin_text) + 3) // 4}x')


def hex_to_bin(hex_text):
    """ Converte um texto em formato hexadecimal para binário.

    Parâmetros
    ----------
    hex_text : str
        texto em formato hexadecimal, que se pretende converter

    Retorna
    -------
    bin_text : str
        texto convertido para formato binário
    """
    return format(int(hex_text, 16), f'0{4*len(hex_text)}b')


def length(data_hex):
    """ Retorna o comprimento, em bytes, de uma string hexdecimal.
    O comprimento (n) é devolvido em formato binário (b), tal que:
        - se 0 <= n <= 127, então b = 0[bin(n,7)]
        - se 128 <= n <= 255, então b = 10000001 [bin(n,8)]
        - se 256 <= n <= 65535, então b = 10000010 [bin(n,16)]
        - senão, exceção
    Note-se que [bin(x,k)] representa o valor de x em binário,
    com k bits.

    Parâmetros
    ----------
    data_hex : str
        string com dados, no formato hexadecimal, cujo comprimento
        em bytes se pretende obter

    Retorna
    -------
    length_bin : int
        comprimento de 'data_hex' em bytes, em formato binário
    
    Levanta
    -------
    Exception
        se comprimento dos dados é superior a 65535
    """

    # Obtenção do comprimento, em bytes, da string hexadecimal
    n = len(bytes.fromhex(data_hex))

    # Conversão do comprimento para um formato binário, com 1, 2
    # ou 3 bytes, de acordo com a descrição da função
    if n >= 0 and n <= 127:
        return '0' + '{0:07b}'.format(n)
    elif n >= 128 and n <= 255:
        return '10000001' + '{0:08b}'.format(n)
    elif n >= 256 and n <= 65535:
        return '10000010' + '{0:016b}'.format(n)
    else:
        raise Exception("ERROR: Data too long.")


def extract_length(hex_text):
    """ Extrai o comprimento do início de uma string hexadecimal,
    tendo este sido gerado, em formato binário, pela função
    'length'.

    Parâmetros
    ----------
    hex_text : str
        texto em hexadecimal, cujo prefixo é o comprimento que
        se pretende extrair

    Retorna
    -------
    length : int
        comprimento extraido, em formato decimal
    
    hex_text : str
        texto hexadecimal, sem o prefixo correspondente ao
        comprimento
    
    Levanta
    -------
    Exception
        se não é encontrado um prefixo que corresponda a um
        comprimento
    """

    # Conversão dos 3 primeiros bytes do texto hexadecimal para
    # binário
    bin_text = hex_to_bin(hex_text[:6])

    # Extração do comprimento e retorno do mesmo, bem como do
    # restante texto hexadecimal
    if bin_text[0] == '0':
        return int(bin_text[1:8], 2), hex_text[2:]
    elif int(bin_text[1:8], 2) == 1:
        return int(bin_text[8:16], 2), hex_text[4:]
    elif int(bin_text[1:8], 2) == 2:
        return int(bin_text[8:24], 2), hex_text[6:]
    else:
        raise Exception("ERROR: No length found.")


def data_to_hex(data, encode):
    """ Converte dados para um formato hexadecimal, com determinada
    codificação.

    Parâmetros
    ----------
    data : str/int
        string ou inteiro que se pretende converter para
        hexadecimal
    
    encode : str
        string que especifica a codificação a utilizar

    Retorna
    -------
    content:
        conteúdo de 'data', convertido para hexadecimal
    
    Levanta
    -------
    Exception
        se dados de input apresentam um tipo diferente de int
        ou str
    """

    # Codificação BCD
    if encode and encode.upper() == 'BCD':
        if isinstance(data, str) and data.isdigit():
            content = bin_to_hex(bcd.int_to_bcd(int(data)))
        elif isinstance(data, int):
            content = bin_to_hex(bcd.int_to_bcd(data))
        else:
            raise Exception('ERROR: Data format unknown.')
    
    # Sem codificação
    elif encode and encode.upper() == 'NO_ENCODE':
        if isinstance(data, str):
            content = data
        elif isinstance(data, int):
            content = str(data)
        else:
            raise Exception('ERROR: Data format unknown.')
    
    # Codificação das categorias
    elif encode and encode.upper() == 'CATEGORIES_ENCODE':
        try:
            # C1;20000315;20100314;S01;<=;38303030
            fields = data.split(';')
            splitter = ';'.encode('latin-1').hex()
            content = fields[0].encode('latin-1').hex() + splitter +\
                      fields[1] + splitter +\
                      fields[2] + splitter +\
                      fields[3].encode('latin-1').hex() + splitter +\
                      fields[4].encode('latin-1').hex() + splitter +\
                      fields[5]
        except:
            raise Exception('ERROR: Wrong categories format.')
    
    # Codificação por defeito
    else:
        if isinstance(data, str):
            content = data.encode().hex()
        elif isinstance(data, int):
            content = format(data, '02x')
        else:
            raise Exception('ERROR: Data format unknown.')

    return content


def hex_to_data(hex_data, encode, decode):
    """ Converte dados codificados em hexadecimal para o formato
    original.

    Parâmetros
    ----------
    hex_data : str
        string hexadecimal, cujo conteúdo original se pretende
        recuperar
    
    encode : str
        string que especifica a codificação utilizada
    
    decode : str
        string que especifica o tipo de dados original

    Retorna
    -------
    content : str/int
        conteúdo de 'hex_data', convertido para o seu formato
        original
    
    Levanta
    -------
    Exception
        se formato de categorias está incorreto
    """
    
    # Codificação BCD
    if encode and encode.upper() == 'BCD':
        if decode and decode.upper() == 'INT':
            content = bcd.bcd_to_int(hex_to_bin(hex_data))
        else:
            content = str(bcd.bcd_to_int(hex_to_bin(hex_data)))
    
    # Sem codificação
    elif encode and encode.upper() == 'NO_ENCODE':
        if decode and decode.upper() == 'INT':
            content = int(hex_data)
        else:
            content = hex_data
    
    # Codificação das categorias
    elif encode and encode.upper() == 'CATEGORIES_ENCODE':
        try:
            # C1;20000315;20100314;S01;<=;38303030
            hex_fields = hex_data.split(';'.encode('latin-1').hex())
            content = bytes.fromhex(hex_fields[0]).decode('latin-1') + ';' +\
                      hex_fields[1] + ';' +\
                      hex_fields[2] + ';' +\
                      bytes.fromhex(hex_fields[3]).decode('latin-1') + ';' +\
                      bytes.fromhex(hex_fields[4]).decode('latin-1') + ';' +\
                      hex_fields[5]
        except:
            raise Exception('ERROR: Wrong categories format.')
    
    # Codificação por defeito
    else:
        if decode and decode.upper() == 'INT':
            content = int(hex_data, 16)
        else:
            content = bytes.fromhex(hex_data).decode()

    return content


def hex_to_tlv(hex_content, config):
    """ Adiciona os prefixos referentes à tag e/ou ao comprimento
    de determinado conteúdo hexadecimal ao mesmo, de acordo com a
    configuração associada.

    Parâmetros
    ----------
    hex_content : str
        conteúdo ao qual se pretende adicionar tag e/ou
        comprimento
    
    config : dict
        configuração que indica tag e comprimento, caso
        exista, do 'hex_content'
    
    Retorna
    -------
    hex_result : str
        conteúdo no formato TLV (Tag, Length, Value)
    """

    hex_tlv = ''

    # Tag
    if 'tag' in config:
        hex_tlv += config['tag']
    # Length
    if 'length' in config:
        if config['length'] == 'var':
            hex_tlv += bin_to_hex(length(hex_content))
    # Value
    hex_tlv += hex_content
    
    return hex_tlv


def tlv_to_data(hex_string, config):
    """ Remove os prefixos referentes à tag e/ou ao comprimento
    de determinada string hexadecimal, de acordo com a
    configuração associada.

    Parâmetros
    ----------
    hex_string : str
        string da qual se pretende remover prefixo com tag
        e/ou comprimento, bem como extrair o conteúdo
        associado
    
    config : dict
        configuração que indica tag e comprimento, caso
        exista, do prefixo da 'hex_string'
    
    Retorna
    -------
    content : str
        conteúdo da string recebida como argumento, sem
        o prefixo com a tag e o tamanho
    
    rest : str
        resto da string, não abrangida pela tag e tamanho
        referidos
    
    Levanta
    -------
    Exception
        se é esperado encontrar determinada tag e esta não constitui
        o prefixo da string hexadecimal
    """

    # Remover Tag
    if 'tag' in config:
        if hex_string.lower().startswith(config['tag'].lower()):
            hex_string = hex_string[len(config['tag']):]
        else:
            raise Exception('ERROR: Unexpected tag.')
    # Remover Length
    if 'length' in config:
        if config['length'] == 'var':
            l, hex_string = extract_length(hex_string)
        else:
            l = int(config['length'])
        bytes_string = bytes.fromhex(hex_string)

        # Retornar o conteúdo abrangido pelo Length e o resto da string
        return (bytes_string[:l]).hex(), (bytes_string[l:]).hex()
    
    # Se não existe Length, não há conteúdo associado
    return None, hex_string


def verify_category(category):
    """ Verifica a validade de uma categoria de veículos.

    Parâmetros
    ----------
    category : str
        categoria de veículos a validar
    
    Retorna
    -------
    validity : boolean
        True, se a categoria é válida; False, caso contrário
    """

    # Componentes da categoria
    code_category = r'[' + A + N + r']{1,2}'
    date_of_issue = r'[' + N + r']{8}'
    date_of_expiry = r'[' + N + r']{8}'
    code = r'[' + A + N + S + r']{1,5}'
    sign = r'[' + S + r']{1,2}'
    value = r'[' + N + r']+'

    # Padrão que caracteriza uma categoria
    pattern = r'^' + code_category + r';' + date_of_issue + r';' + date_of_expiry + r';' + code + r';' + sign + r';' + value + r'$'

    # Validação da categoria recebida como argumento
    return (True if re.match(pattern, category, re.UNICODE) else False)


def validate_constraints(data, config, last_key):
    """ Verifica a validade de dados através de restrições implementadas
    com expressões regulares ou funções.

    Parâmetros
    ----------
    data : any
        dados cuja validade se pretende averiguar
    
    config : dict
        configuração associada aos dados, que contém as restrições,
        apresentadas como expressões regulares ou funções
    
    last_key : str
        chave associada à configuração recebida (informativo)
    
    Levanta
    -------
    Exception
        se a restrição não é verificada nos dados
    """

    # Valida restrição com expressões regulares
    if 'constraints' in config:
        if not re.match(r'^' + config['constraints'].replace('$A', A)
                                                    .replace('$N', N)
                                                    .replace('$S', S)
                                                    .replace('$D', D)
                        + r'$',
                        str(data),
                        flags=re.UNICODE):
            raise Exception(f'ERROR: Field {last_key} cannot take the value "{data}".')
    
    # Valida restrição com funções
    if 'constraints_func' in config:
        if not eval(config['constraints_func'].replace('$DATA', f'"{data}"')):
            raise Exception(f'ERROR: Field {last_key} cannot take the value "{data}".')


def asn1_encode(data_group, config, last_key = None):
    """ Codifica um objeto, de acordo com o standard ASN1, tendo em
    conta a configuração recebida como argumento.

    Parâmetros
    ----------
    data_group : class instance
        instância de objeto cujas variáveis se pretende codificar
    
    config : dict
        configuração do objeto, que especifica tags, comprimentos
        e restrições a aplicar e validar
    
    last_key : str
        chave da configuração recebida como argumento
    
    Retorna
    -------
    hex_result : str
        resultado de codificar o 'data_group'
    """
    hex_result = ''
    data = None
    content = None

    # Se existe conteúdo codifica-o
    if 'content' in config:
        content = ''
        for c in config['content']:
            content += asn1_encode(data_group, config['content'][c], c)
    # Se não, obtém o conteúdo da respetiva variável do 'data_group'
    else:
        data = getattr(data_group, last_key)
    
    # Se é lista, valida restrições e codifica cada elemento da variável
    if 'size_list' in config:
        for elem in data:
            validate_constraints(elem, config, last_key)
            hex_result += hex_to_tlv(data_to_hex(elem, config.get('encode', None)), config)
    # Se não, caso tenha variável, calida-a e codifica-a; o resultado codificado
    # é armazenado como TLV
    else:
        if data:
            validate_constraints(data, config, last_key)
            content = data_to_hex(data, config.get('encode', None))
        hex_result = hex_to_tlv(content, config)

    return hex_result


def asn1_decode(hex_string, config, last_key = None):
    """ Descodifica uma string hexadecimal, de acordo com o standard ASN1,
    tendo em conta a configuração recebida como argumento.

    Parâmetros
    ----------
    hex_string : str
        string hexadecimal que se pretende descodificar, para obter
        os dados do objeto original
    
    config : dict
        configuração do objeto, que especifica tags, comprimentos
        e restrições a aplicar e validar
    
    last_key : str
        chave da configuração recebida como argumento
    
    Retorna
    -------
    data : dict
        dados do objeto original
    
    rest : str
        resto da string hexadecimal, ao qual a configuração não se
        aplica
    
    Levanta
    -------
    Exception
        se string hexadecimal a descodificar não apresenta o formato correto
    """
    data_group_result = ''
    data = dict()
    rest = ''

    # Se tem tag ou comprimento, extrai o conteúdo associado
    if 'tag' in config or 'length' in config:
        hex_content, rest = tlv_to_data(hex_string, config)

    # Se tem conteúdo, descodifica cada elemento associado
    if 'content' in config:
        for c in config['content']:
            data_tmp, hex_content = asn1_decode(hex_content, config['content'][c], c)
            data.update(data_tmp)
        # Se sobrar conteúdo, codificação está incorreta
        if hex_content:
            raise Exception('ERROR: Data length is higher than expected.')
    # Se não, descodifica a variável, valida-a e adiciona-a aos dados
    else:
        data_tmp = hex_to_data(hex_content, config.get('encode', None), config.get('decode', None))
        validate_constraints(data_tmp, config, last_key)

        if 'size_list' in config:
            if last_key in data:
                data[last_key].append(data_tmp)
            else:
                data[last_key] = [data_tmp]
        else:
            data[last_key] = data_tmp

    return data, rest


def encode(data_group, config_filename):
    """ Codifica um objeto, de acordo com o standard ASN1, tendo em conta
    determinado ficheiro de configuração.

    Parâmetros
    ----------
    data_group : class instance
        instância de objeto cujas variáveis se pretende codificar
    
    config_filename : str
        nome do ficheiro de configuração (json) do objeto, que
        especifica tags, comprimentos e restrições a aplicar e
        validar
    
    Retorna
    -------
    asn1_encode : str
        resultado de codificar o 'data_group'
    """
    # Parse do ficheiro de configuração
    with open(config_filename) as fp:
        config = json.load(fp)

    # Codificação do objeto
    return asn1_encode(data_group, config)


def decode(hex_string, config_filename):
    """ Descodifica uma string hexadecimal, de acordo com o standard ASN1,
    tendo em conta determinado ficheiro de configuração.

    Parâmetros
    ----------
    hex_string : str
        string hexadecimal que se pretende descodificar, para obter
        o objeto original
    
    config_filename : str
        nome do ficheiro de configuração (json) do objeto, que
        especifica tags, comprimentos e restrições a aplicar e
        validar
    
    Retorna
    -------
    data : dict
        dados do objeto original
    
    Levanta
    -------
    Exception
        se string hexadecimal a descodificar não apresenta o formato correto
    """

    # Parse do ficheiro de configuração
    with open(config_filename) as fp:
        config = json.load(fp)
    
    # Descodificação da string hexadecimal e retorno dos dados originais
    data, hex_string = asn1_decode(hex_string, config)
    if hex_string:
        raise Exception('ERROR: Data length is higher than expected.')
    
    return data
