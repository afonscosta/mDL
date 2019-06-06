# Main

- [X] Init a partir de um dicionário.
- [X] Init a partir de um ficheiro.
- [X] Guardar em ficheiro
- [X] Permitir obter um dado conjunto da informação por parte do leitor mDL. (`get_data`)
- [X] Permitir definir quais os campos que têm autorização para serem partilhados. (`set_permissions`)
- [X] Autenticar a origem da informação da mDL. (`get_signature`)
    1. [X] Verificar a fidedignidade ou obter uma chave pública fidedigna.
    2. [X] Usar a chave para realizar autenticação passiva.
- [X] Verificar a integridade da informação.
    1. [X] Reading Authority (RA) usa a chave pública para verificar a assinatura (`get_signature`)
    2. [X] RA calcula o digest dos DG's que está interessado
    3. [X] Compara com os que estão no mDL (`get_digests`)
- [!] Permitir verificar a ligação entre uma mDL e o seu titular. Tabela pág. 17 doc 3 não diz nada sobre isto!
- [X] Receber request para aceder a mais info. Autorizar ou não. Fazer update das autorizações. (`request_info`)


# Data Groups (DG)

- [X] Init a partir de um dicionário.
- [X] Init a partir de um ficheiro.
- [X] Guardar em ficheiro
- [X] Carregar de ficheiro
- [X] Verificar a integridade (talvez devolver só a hash dos dados e a verificação ser feita na main).
- [X] Variável para cada campo que diz se se pode ler ou não.
- [X] Get para cada campo de dados (apenas se for autorizado).
- [ ] Set???


# EF.COM - Afonso
- pag. 37 do doc 3
- pag. 51 do doc 2
- [ ] Quais os campos?
- [ ] Fazer só a lista de versão/tags?
- Implementar só a lista de versões e tags

# EF.GroupAccess - Mafalda
- pag. 26 do doc 5
- Implementar a classe e utilização

# EF.SOD - Daniel
- pag. 21 do doc 3
- Implementar a classe
