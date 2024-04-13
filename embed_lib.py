import ctypes
import platform

if platform.system() == 'Windows':
    path = 'win/'
    extension = '.dll'
else:
    path = 'lin/'
    extension = '.so'

if platform.architecture()[0] == "64bit":
    # name = 'lib-embed-x64'
    name = 'lib-embed-x64'
else:
    name = 'lib-embed-x86'
    
# load library
ffi = ctypes.cdll.LoadLibrary(path + name + extension)

'''
    OBTER_VALOR (embed_obter_valor)

        método responsável por buscar um valor contido em uma chave de um json valido
    
    OUTPUT 

        exemplo: 

        json =
            "{ 
                "key1": "value1", 
                "key2": {
                    "key21": "value21",
                    "key22": "value22",
                    "key23": "value23",
                    "key24": "value24",
                    "key25": "value25",
                }
            }"

        res1 = embed_obter_valor(json, "key1")
        logo, res1 = "value1"

        res2 = embed_obter_valor(json, "key2")
        logo, res2 = "{ "key21": "value21", "key22": "value22", "key23": "value23", "key24": "value24", "key25": "value25" }

        res23 = embed_obter_valor(json, "key2")
        logo, res23 = "value23"
'''
def obter_valor(json, key):
    fn = ffi.embed_obter_valor
    fn.restype = ctypes.c_char_p
    fn.argtypes = [ctypes.c_char_p]
    json = ctypes.c_char_p(bytes(json, 'utf-8'))
    key = ctypes.c_char_p(bytes(key, 'utf-8'))
    return fn(json, key).decode('utf-8')

'''
    CONFIGURAR (embed_configurar)

        método responsável pela configuração dos produtos embed:
            - pix (atual)
            - pos (implementação futura)
            - tef (implementação futura)
            - etc...

        deve ser chamada somente no momento do setup, ou quando houver uma atualização de informações.
        as informações são persistidas em um arquivo seguro, que durante a execução da lib consulta o que for necessário.

    INPUT

        este método conta com duas formas de entrada:
            - metaparametros: as informações são adicionadas a uma string, separadas por ';'
                ex: "X;Y;Z;1;;3" 
                obs: quando não houver valor, basta deixar o campo vazio (2)
            - json: as informações são adicionadas a uma string, no formato json
                ex: json =  
                "{
                    "configs": {
                        "produto": "X",
                        "sub_produto: "Y",
                        "infos": {
                            // informações referentes ao produto que estiver usando
                            // cada um dos produtos e sub produtos terá sua entrada personalizada neste primeiro momento...
                        }
                    }
                }"

    OUTPUT 

        a saída é uma string no formato json (sempre) e para obter as informações basta deserializar,
        ou fazer o uso do método 'embed_obter_valor'

        exemplo:

        result = "{
            "codigo": code1,
            "mensagem": "mensagem1",
            "resultado": {
                // informações de saída referentes ao produto e sub produto que estiver usando
            }
        }"
'''
def configurar(input):
    fn = ffi.embed_configurar
    fn.restype = ctypes.c_char_p
    fn.argtypes = [ctypes.c_char_p]
    input = ctypes.c_char_p(bytes(input, 'utf-8'))
    return fn(input).decode('utf-8')

'''
    INICIAR (embed_iniciar)

        método responsável pela inicialização do produto que for realizar uma operação

    INPUT

        este método conta com duas formas de entrada:
            - metaparametros: as informações são adicionadas a uma string, separadas por ';'
                ex: "prod1" 
            - json: as informações são adicionadas a uma string, no formato json
                ex: json =  
                "{
                    "iniciar": {
                        "operacao": "prod1",
                    }
                }"
        
    OUTPUT 

        a saída é uma string no formato json (sempre) e para obter as informações basta deserializar,
        ou fazer o uso do método 'embed_obter_valor'

        exemplo:

        result = "{
            "codigo": code1,
            "mensagem": "mensagem1",
            "resultado": {
                // informações de saída referentes ao produto e sub produto que estiver usando
            }
        }"
'''
def iniciar(input):
    fn = ffi.embed_iniciar
    fn.restype = ctypes.c_char_p
    fn.argtypes = [ctypes.c_char_p]
    input = ctypes.c_char_p(bytes(input, 'utf-8'))
    return fn(input).decode('utf-8')

'''
    PROCESSAR (embed_processar)

        método responsável pelo processamento das operações desenvolvidas para os produtos. 
        este método deve ser chamado para iniciar o processamento e depois em alguns casos
        em loop para consultar status, realizar outras operações até que o retorno seja dado
        como concluido

    INPUT

        este método conta com duas formas de entrada:
        - metaparametros: as informações são adicionadas a uma string, separadas por ';'
            ex: "operacao1;X;Y;Z" 
        - json: as informações são adicionadas a uma string, no formato json
            ex: json =  
            "{
                "processar": {
                    "operacao": "operacao1",
                    "valor1": "X",
                    "valor2": "Y",
                    "valor3": "Z"
                }
            }"

    OUTPUT 

        a saída é uma string no formato json (sempre) e para obter as informações basta deserializar,
        ou fazer o uso do método 'embed_obter_valor'

        exemplo:

        result = "{
            "codigo": code1,
            "mensagem": "mensagem1",
            "resultado": {
                // informações de saída referentes ao produto e sub produto que estiver usando
            }
        }"
'''
def processar(input):
    fn = ffi.embed_processar
    fn.restype = ctypes.c_char_p
    fn.argtypes = [ctypes.c_char_p]
    input = ctypes.c_char_p(bytes(input, 'utf-8'))
    return fn(input).decode('utf-8')

'''
    FINALIZAR (embed_finalizar)

        método responsável por realizar a finalização do processamento do produto em uso
    
    OUTPUT 

        a saída é uma string no formato json (sempre) e para obter as informações basta deserializar,
        ou fazer o uso do método 'embed_obter_valor'

        exemplo:

        result = "{
            "codigo": code1,
            "mensagem": "mensagem1",
            "resultado": {
                // informações de saída referentes ao produto e sub produto que estiver usando
            }
        }"
'''
def finalizar(input):
    fn = ffi.embed_finalizar
    fn.restype = ctypes.c_char_p
    fn.argtypes = [ctypes.c_char_p]
    input = ctypes.c_char_p(bytes(input, 'utf-8'))
    return fn(input).decode('utf-8')
